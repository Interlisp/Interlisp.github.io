#!/usr/bin/env bash

set -e

rawItemsFile=false
debugFiles=false
tagFiles=false
typeFiles=true
curlFiles=false
# The collection files will be created only if directly querying Zotero API.
collectionFiles=false

# removeChildrenFromFinalFile=false

showInfoLevel=2     
#  0: NO showInfo messages.
#  1: high level general info messages.
#  2: warning-type messages.
#  3: 
#  4: 
#  5: detailed general info messages.
#  6: 
#  7: 
#  8: individual processing steps (most of which may generate a debug File -- see $debugFiles)
#  9: very detailed general info messages.
# 10: extremely detailed messages (e.g., calls to curl, etc.)

function showInfo() {
    # The $1 is the level for this message ($showInfoLevel must be >= this)
    # The $2 is the message string
    if [[ $showInfoLevel -ge $1 ]] ; then
      echo "$2"
    fi
}

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
    local collection_item=$(jq -r "map(select(.key==\"$collection_key\"))|.[0]" <<< "$collections")
    showInfo 5 "====================================="
    showInfo 5 "collection_item: $collection_item"
    local collection_name=$(jq -r '.name' <<< "$collection_item")
    local deleted=$(jq -r '.deleted // false' <<< "$collection_item")
    showInfo 5 "collection.deleted: $deleted"
    local numItems=$(jq -r '.numItems' <<< "$collection_item")
    if [[ $deleted = "true" ]] ; then
      showInfo 2 "Skipping deleted collection $collection_key: $collection_name"
      return
    elif [[ numItems -eq 0 ]] ; then
      showInfo 2 "Empty collection $collection_key: $collection_name"
    else
      showInfo 1 "Getting collection $collection_key: $collection_name"
    local start=0
    local limit=100
    while :; do
          showInfo 10 "curl of $collection_key at start $start"
        local this_page=$(curl -s "https://api.zotero.org/groups/$GROUP_ID/collections/$collection_key/items?include=data,csljson&start=$start&limit=$limit&v=3")
          local item_count=$(jq '. | length' <<< "$this_page")
          showInfo 10 "curl returned $item_count items"
          if [[ $item_count > 0 ]] ; then
            if $curlFiles ; then
              local pageFile=$( printf "curl/%s-%02d.json" $collection_key $(( $start / $limit )) )
              echo "$this_page" > "$pageFile"
            fi
        items=$(jq -s 'add' <<< "$this_page$items")
            showInfo 10 "items updated"
            start=$(($start + $item_count))
          fi
          # Break when we don't get the full $limit of items
          # (it's still possible to do one redundant curl if collection has exact multiple of $limit items)
          [[ $item_count -ge $limit ]] || break
    done
    fi

    local numCollections=$(jq -r '.numCollections' <<< "$collection_item")
    if [[ $numCollections -gt 0 ]] ; then
      showInfo 5 "Getting subcollections of $collection_key: $collection_name"
      local subcollections=$(curl -s "https://api.zotero.org/groups/$GROUP_ID/collections/$collection_key/collections" | jq -r 'map(.data+.meta)')
      collections=$(jq -s 'add' <<< "$collections$subcollections")

    # Recurse into subcollections
    while read subcollection_key; do
        add_items_from_collection $subcollection_key
    done < <(jq -r '.[].key' <<< "$subcollections")
    fi
}

root_collection="FSK5IX4F"
if [[ $# -eq 0 ]] ; then
  # Initialize with the root collection.
  collections=$(curl -s "https://api.zotero.org/groups/$GROUP_ID/collections/$root_collection" | jq -s -r 'map(.data+.meta)')
  add_items_from_collection $root_collection
  if $collectionFiles ; then
    echo "$collections" > collections.json
  fi
  showInfo 1 "$(jq '. | length' <<< "$collections") collections"

  while read neededUrl; do
    showInfo 10 "curl of $neededUrl"
    item=$(curl -s "$neededUrl?include=data,csljson&v=3")
    showInfo 10 "curl returned"
	items=$(jq -s 'add' <<< "[$item]$items")
    showInfo 10 "items updated"
  done < <(jq -r 'include "./bib-fns";getNeededUrls|.[]' <<< "$items")

  if $collectionFiles ; then
  grouped_collections=$(jq 'group_by(.parentCollection)' <<< "$collections")
  # This is not yet fully hierarchically nested.
    echo "$grouped_collections" > grouped_collections.json
  fi
  # Only if we got the raw items from the Zotero API
  if $rawItemsFile ; then
    echo "$items" > 00-rawItems.json
  fi
else
  items=$(<$1)
fi

showInfo 1 "Got $(jq '. | length' <<< "$items") items"

# Piece-wise processing for debugging:
items=$(jq 'include "./bib-fns";map(semiflatten)' <<< "$items")
showInfo 8 "Elevate fields in .csljson and .data to the item level."
if $debugFiles ; then
  dfn=$(debugFileName "semiflattened" $dfn)
  echo "$items" > "$dfn"
fi
items=$(jq 'include "./bib-fns";map(if has("note") then .note |= unwrapDiv else . end)' <<< "$items")
showInfo 8 "Clean up note field (extract from HTML div)."
if $debugFiles ; then
  dfn=$(debugFileName "cleanDiv" $dfn)
  echo "$items" > "$dfn"
fi

showInfo 8 "Find duplicate .key entries"
groupedByKey=$(jq 'group_by(.key)' <<< "$items")
if $debugFiles ; then
  dupIDs=$(jq 'map(select(length>1) | {key: .[0].key, items: .})' <<< "$groupedByKey")
  numDupKeys=$(jq '. | length' <<< "$dupIDs")
  if [[ "$numDupKeys" -ne 0 ]] ; then
    numDupEntries=$(jq 'map(.items | length) | add' <<< "$dupIDs")
    showInfo 2 "$numDupKeys keys have multiple occurrences totalling $numDupEntries entries"
  fi
  dfn=$(debugFileName "dupIDs" $dfn)
  echo "$dupIDs" > "$dfn"
fi

#remove duplicates
items=$(jq 'map(.[0]) | sort_by(.date)' <<< "$groupedByKey")
showInfo 8 "Remove Duplicates"
if $debugFiles ; then
  dfn=$(debugFileName "noDupSorted" $dfn)
  echo "$items" > "$dfn"
fi

# Remove library, links, and meta objects; and some fields from entries
# (These are not used any further on, so simplify.)
items=$(jq 'map(del(.["library", "links", "meta", "accessed", "accessDate", "dateAdded", "dateModified"]))' <<< "$items")
showInfo 8 "Remove library, links, and meta objects and some unnecessary fields"
if $debugFiles ; then
  dfn=$(debugFileName "noLibraryLinksMeta" $dfn)
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
showInfo 8 "Consolidate URL to url (upper vs. lower case)"
if $debugFiles ; then
  dfn=$(debugFileName "urlConsolidated" $dfn)
  echo "$items" > "$dfn"
fi

# Use DOI to create url where needed and available
items=$(jq 'include "./bib-fns";map(if (blankKey("url") and nonBlankKey("DOI")) then setpath(["url"]; make_DOI_to_url(.DOI)) else . end)' <<< "$items")
showInfo 8 "Use DOI to construct URL if needed"
if $debugFiles ; then
  dfn=$(debugFileName "DOI-url" $dfn)
  echo "$items" > "$dfn"
fi

items=$(jq 'include "./bib-fns";map(getTargetInfo)' <<< "$items")

# now use children items to amend the info for the parentItem
childrenGroupedByParent=$(jq 'group_by(.target)|map(sort_by(.parentItem))' <<< "$items")
showInfo 8 "Collect children grouped by parent"
if $debugFiles ; then
  dfn=$(debugFileName "childrenGroupedByParent" $dfn)
  echo "$childrenGroupedByParent" > "$dfn"
fi

showInfo 8 "Embed Children into their parentItem (children field)."
items=$(jq 'map(if has(1) then (first + {children: .[1:]}) else first end)' <<< "$childrenGroupedByParent")
if $debugFiles ; then
  dfn=$(debugFileName "itemsWithNestedChildren" $dfn)
  echo "$items" > "$dfn"
fi

showInfo 5 "Delete items that Zotero indicated as such."
beforeCount=$(jq '. | length' <<< "$items")
items=$(jq 'map(select(.deleted|not))' <<< "$items")
afterCount=$(jq '. | length' <<< "$items")
showInfo 5 "Removed $(( $beforeCount - $afterCount )) items marked as deleted."

showInfo 1 "Got $(jq '. | length' <<< "$items") clean, top-level items"
items=$(jq 'include "./bib-fns";map(applyChildrenAmendments)' <<< "$items")
showInfo 8 "Update Parent items from their Children"
if $debugFiles ; then
  dfn=$(debugFileName "updatedItemsFromChildren" $dfn)
  echo "$items" > "$dfn"
fi
absNote=$(jq 'include "./bib-fns";map(select((nonBlankKey("abstract") or nonBlankKey("abstractNote")) and (.abstract != .abstractNote)) | {key: .key, title: .title, abstract: .abstract, abstractNote: .abstractNote})' <<< "$items")
showInfo 8 "Check abstract vs. abstractNote mismatch"
if $debugFiles ; then
  dfn=$(debugFileName "absNoteMismatch" $dfn)
  echo "$absNote" > "$dfn"
fi
absNoteMismatchCount=$(jq '. | length' <<< "$absNote")
if [[ "$absNoteMismatchCount" -eq 1 ]] ; then
  showInfo 2 "Warn: 1 entry with mismatch between abstract and abstractNote fields"
elif [[ "$absNoteMismatchCount" -ne 0 ]] ; then
  showInfo 2 "Warn: $absNoteMismatchCount entries with mismatch between abstract and abstractNote fields"
fi

# remove redundant .abstractNote fields
items=$(jq 'include "./bib-fns";map(cleanAbstracts)' <<< "$items")
showInfo 8 "Remove redundant abstractNote fields"
if $debugFiles ; then
  dfn=$(debugFileName "abstractsCleaned" $dfn)
  echo "$items" > "$dfn"
fi
if $typeFiles ; then
  types=$(jq 'map({key, title, type, itemType}) | group_by(.type) | map({type:.[0].type, itemTypes:(group_by(.itemType)|map({itemType:.[0].itemType, items:map({title, key})}))})' <<<"$items")
  echo "$types" > finalTitleKeyTypeInfo.json
fi
if $debugFiles ; then
  noURL=$(jq 'include "./bib-fns";map(select(blankKey("url")))' <<< "$items")
  dfn=$(debugFileName "noURL" $dfn)
  echo "$noURL" > "$dfn"
fi
finalCount=$(jq '. | length' <<< "$items")

items=$(jq 'include "./bib-fns";map(issued_iso_string)' <<< "$items")

items=$(jq 'include "./bib-fns";map(add_author_string)' <<< "$items")
# if $removeChildrenFromFinalFile; then
#   # Remove .children arrays, if any. Save space.
#   items=$(jq 'map(del(.children))' <<< "$items")
#   showInfo 8 "Remove .children arrays from final items"
#   if $debugFiles ; then
#     dfn=$(debugFileName "withoutChildrenArray" $dfn)
#     echo "$items" > "$dfn"
#   fi
# fi

# Do this here, instead of keeping a copy of the current value of $items, just to do this later.
jq -c 'include "./bib-fns";.[] | bibItem' <<< "$items" > bibliography-items-by-line.json
# jq  'include "./bib-fns";map(bibItem)' <<< "$items" > 000-bibliography-items-by-line.json

# Group by year
items=$(jq 'group_by(.issued."date-parts"[0][0])' <<< "$items")
items=$(jq 'map({ (.[0].issued."date-parts"[0][0] // "Undated" | tostring): . })' <<< "$items")
showInfo 8 "Group by year"
if $debugFiles ; then
  dfn=$(debugFileName "groupedByYear" $dfn)
  echo "$items" > "$dfn"
fi

items=$(jq 'include "./bib-fns";map(to_entries) | flatten(1) | group_by(.key) | map(reconstituteGroupedEntries) | from_entries' <<< "$items")
if $debugFiles ; then
  dfn=$(debugFileName "final" $dfn)
  echo "$items" > "$dfn"
fi

showInfo 1 "Generating individual Bibliography entries' .md files"
BIBLIOGRAPHY_DIR="./../content/en/history/bibliography"
export BIBLIOGRAPHY_DIR
BIBITEMS_DIR="./../static/data/bibItems"
export BIBITEMS_DIR

# Ensure target directories exist
mkdir -p "$BIBLIOGRAPHY_DIR" "$BIBITEMS_DIR"

./bibSplit.pl bibliography-items-by-line.json 2>bibSplit.err
# Cleanup (uncomment once working)
# rm bibliography-items-by-line.json

showInfo 1 "Outputting CSL JSON"
showInfo 1 "$finalCount entries"
echo "$items" > "$(dirname "$0")/../static/data/bibliography.json"
