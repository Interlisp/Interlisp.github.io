#!/usr/bin/env bash

set -e

rawItemsFile=false
debugFiles=false
tagFiles=false
typeFiles=false
# The collection files will be created only if directly querying Zotero API.
collectionFiles=false

dfn="00"
function debugFileName() {
    # The $1 is the file NAME string (without the number prefix or extension)
    # The $2 is the previous instance of the generated debugFileName
    # and the "count" is in the leading 2 characters.
    local cfn=$2
    # increment the count before using it.
    # (The leading 1 and the - 100 are so a leading 0 doesn't set octal parsing)
    echo $( printf "%02d-%s.json" $(( ("1${cfn:0:2}" - 100) + 1)) $1 )
}

GROUP_ID=2914042

items=""
collections=""

function add_items_from_collection () {
    local collection_key="$1"
    echo "Getting collection $collection_key"
    local start=0
    local limit=100
    while :; do
        local this_page=$(curl -s "https://api.zotero.org/groups/$GROUP_ID/collections/$collection_key/items?include=data,csljson&start=$start&limit=$limit&v=3")
        items=$(jq -s 'add' <<< "$this_page$items")
        start=$(($start + $limit))

        # Break when we don't get any more items
        [[ $(jq '. | length' <<< "$this_page") > 0 ]] || break
    done

    local subcollections=$(curl -s "https://api.zotero.org/groups/$GROUP_ID/collections/$collection_key/collections" | jq -r '.[].data|{key, name, parentCollection}' | jq -s '.')
    collections=$(jq -s 'add' <<< "$subcollections$collections")

    # Recurse into subcollections
    while read subcollection_key; do
        add_items_from_collection $subcollection_key
    done < <(jq -r '.[].key' <<< "$subcollections")
}

root_collection="FSK5IX4F"
if [[ $# -eq 0 ]] ; then
  # Initialize with the root collection.
  collections=$(curl -s "https://api.zotero.org/groups/$GROUP_ID/collections/top" | jq -r '.[].data|{key, name, parentCollection}' | jq -s '.' | jq "map(select(.key==\"$root_collection\"))")
  add_items_from_collection $root_collection
  if $collectionFiles ; then
    echo "$collections" > collections.json
  fi
  echo "$(jq '. | length' <<< "$collections") collections"

  while read neededUrl; do
    item=$(curl -s "$neededUrl?include=data,csljson&v=3")
	items=$(jq -s 'add' <<< "[$item]$items")
  done < <(jq -r 'include "./bib-fns";getNeededUrls|.[]' <<< "$items")

  grouped_collections=$(jq 'group_by(.parentCollection)' <<< "$collections")
  # This is not yet fully hierarchically nested.
  if $collectionFiles ; then
    echo "$grouped_collections" > grouped_collections.json
  fi
  # Only if we got the raw items from the Zotero API
  if $rawItemsFile ; then
    echo "$items" > 00-rawItems.json
  fi
else
  items=$(<$1)
fi

echo "Got $(jq '. | length' <<< "$items") items"

# Piece-wise processing for debugging:
items=$(jq 'include "./bib-fns";map(semiflatten)' <<< "$items")
if $debugFiles ; then
  dfn=$(debugFileName "semiflattened" $dfn)
  echo "$items" > "$dfn"
fi
items=$(jq 'include "./bib-fns";map(if has("note") then .note |= unwrapDiv else . end)' <<< "$items")
if $debugFiles ; then
  dfn=$(debugFileName "cleanDiv" $dfn)
  echo "$items" > "$dfn"
fi
#find and eliminate duplicate .key entries
groupedByKey=$(jq 'group_by(.key)' <<< "$items")
if $debugFiles ; then
  dupIDs=$(jq 'map(select(length>1) | {key: .[0].key, items: .})' <<< "$groupedByKey")
  dfn=$(debugFileName "dupIDs" $dfn)
  echo "$dupIDs" > "$dfn"
fi

#remove duplicates
items=$(jq 'map(.[0]) | sort_by(.date)' <<< "$groupedByKey")
if $debugFiles ; then
  dfn=$(debugFileName "noDupSorted" $dfn)
  echo "$items" > "$dfn"
fi
if $typeFiles ; then
  types=$(jq 'map({key, title, type, itemType}) | group_by(.type) | map({type:.[0].type, itemTypes:(group_by(.itemType)|map({itemType:.[0].itemType, items:map({title, key})}))})' <<<"$items")
  echo "$types" > titleKeyTypeInfo.json
  types=$(jq 'group_by(.type) | map({type:.[0].type, itemTypes:(group_by(.itemType)|map({itemType:.[0].itemType, items:.}))})' <<<"$items")
  echo "$types" > fullTypeInfo.json
fi
if $tagFiles ; then
  tags=$(jq 'map(.tags) | flatten | map(.tag) | unique' <<<"$items")
  echo "$tags" > tags.json
fi
# consolidate URL into url field
items=$(jq 'include "./bib-fns";map(if nonBlankKey("URL") then setpath(["url"]; .URL) | del(.URL) else . end)' <<< "$items")
if $debugFiles ; then
  dfn=$(debugFileName "consolidated" $dfn)
  echo "$items" > "$dfn"
fi

# Use DOI to create url where needed and available
items=$(jq 'include "./bib-fns";map(if (blankKey("url") and nonBlankKey("DOI")) then setpath(["url"]; make_DOI_to_url(.DOI)) else . end)' <<< "$items")
if $debugFiles ; then
  dfn=$(debugFileName "DOI-url" $dfn)
  echo "$items" > "$dfn"
fi

items=$(jq 'include "./bib-fns";map(getTargetInfo)' <<< "$items")
if $debugFiles ; then
  dfn=$(debugFileName "withTargetInfo" $dfn)
  echo "$items" > "$dfn"
fi

# now use children items to amend the info for the parentItem
allFixupInfo=$(jq 'group_by(.target)|map(sort_by(.parentItem))' <<< "$items")
if $debugFiles ; then
  dfn=$(debugFileName "allFixupInfo" $dfn)
  echo "$allFixupInfo" > "$dfn"
fi
# embed children into their parentItem (children field). Then delete items that Zotero indicated as such.
items=$(jq 'map(if has(1) then (first + {children: .[1:]}) else first end)|map(select(.deleted|not))' <<< "$allFixupInfo")
if $debugFiles ; then
  dfn=$(debugFileName "itemsNestedChildren" $dfn)
  echo "$items" > "$dfn"
fi

echo "Got $(jq '. | length' <<< "$items") clean, top-level items"
items=$(jq 'include "./bib-fns";map(applyChildrenAmendments)' <<< "$items")
if $debugFiles ; then
  dfn=$(debugFileName "updatedItems" $dfn)
  echo "$items" > "$dfn"
fi
absNote=$(jq 'include "./bib-fns";map(select((nonBlankKey("abstract") or nonBlankKey("abstractNote")) and (.abstract != .abstractNote)) | {key: .key, title: .title, abstract: .abstract, abstractNote: .abstractNote})' <<< "$items")
if $debugFiles ; then
  dfn=$(debugFileName "absNoteMismatch" $dfn)
  echo "$absNote" > "$dfn"
fi
# remove redundant .abstractNote fields
items=$(jq 'include "./bib-fns";map(cleanAbstracts)' <<< "$items")
if $debugFiles ; then
  dfn=$(debugFileName "abstractsCleaned" $dfn)
  echo "$items" > "$dfn"
fi
if $typeFiles ; then
  types=$(jq 'map({key, title, type, itemType}) | group_by(.type) | map({type:.[0].type, itemTypes:(group_by(.itemType)|map({itemType:.[0].itemType, items:map({title, key})}))})' <<<"$items")
  echo "$types" > finalTitleKeyTypeInfo.json
fi
noURL=$(jq 'include "./bib-fns";map(select(blankKey("url")))' <<< "$items")
if $debugFiles ; then
  dfn=$(debugFileName "noURL" $dfn)
  echo "$noURL" > "$dfn"
fi
finalCount=$(jq '. | length' <<< "$items")
# # Remove .children arrays, if any. Save space.
# items=$(jq 'map(del(.children))' <<< "$items")
# if $debugFiles ; then
    # dfn=$(debugFileName "withoutChildrenArray")
    # echo "$items" > "$dfn"
# fi
# Group by year
items=$(jq 'group_by(.issued."date-parts"[0][0])' <<< "$items")
if $debugFiles ; then
  dfn=$(debugFileName "grouped" $dfn)
  echo "$items" > "$dfn"
fi
items=$(jq 'map({ (.[0].issued."date-parts"[0][0] // "Undated" | tostring): . })' <<< "$items")
if $debugFiles ; then
  dfn=$(debugFileName "Undated" $dfn)
  echo "$items" > "$dfn"
fi
items=$(jq 'map(to_entries)' <<< "$items")
if $debugFiles ; then
  dfn=$(debugFileName "entries" $dfn)
  echo "$items" > "$dfn"
fi
items=$(jq 'flatten(1)' <<< "$items")
if $debugFiles ; then
  dfn=$(debugFileName "flattened" $dfn)
  echo "$items" > "$dfn"
fi
items=$(jq 'group_by(.key)' <<< "$items")
if $debugFiles ; then
  dfn=$(debugFileName "groupedByKey" $dfn)
  echo "$items" > "$dfn"
fi
items=$(jq 'include "./bib-fns";map(reconstituteGroupedEntries) | from_entries' <<< "$items")
if $debugFiles ; then
  dfn=$(debugFileName "final" $dfn)
  echo "$items" > "$dfn"
fi


echo "Outputting CSL JSON"
echo "$finalCount entries"
echo "$items" > "$(dirname "$0")/../static/data/bibliography.json"
