#!/usr/bin/env bash

set -e

GROUP_ID=2914042

items=""

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

    # Recurse into subcollections
    while read subcollection_key; do
        add_items_from_collection $subcollection_key
    done < <(curl -s "https://api.zotero.org/groups/$GROUP_ID/collections/$collection_key/collections" | jq -r '.[].key')
}

root_collection="FSK5IX4F"
if [[ $# -eq 0 ]] ; then
  add_items_from_collection $root_collection
else
  items=$(<$1)
fi

# echo "$items" > 00-rawItems-pre-needed.json

while read neededUrl; do
    item=$(curl -s "$neededUrl?include=data,csljson&v=3")
	items=$(jq -s 'add' <<< "[$item]$items")
done < <(jq -r 'include "./bib-fns";getNeededUrls|.[]' <<< "$items")


echo "Got $(jq '. | length' <<< "$items") items"

# Piece-wise processing for debugging:
# echo "$items" > 0-rawItems.json

items=$(jq 'map(.csljson * .data)' <<< "$items")
# echo "$items" > 1-mapped.json
items=$(jq 'include "./bib-fns";map(if has("note") then .note |= unwrapDiv else . end)' <<< "$items")
# echo "$items" > 2-cleanDiv.json
#find and eliminate duplicate .key entries
groupedByKey=$(jq 'group_by(.key)' <<< "$items")
dupIDs=$(jq 'map(select(length>1) | .[0])' <<< "$groupedByKey")
# echo "$dupIDs" > dupIDs.json
#remove duplicates
items=$(jq 'map(.[0]) | sort_by(.date)' <<< "$groupedByKey")
# echo "$items" > 3-noDupSorted.json
# consolidate URL into url field
items=$(jq 'include "./bib-fns";map(if nonBlankKey("URL") then setpath(["url"]; .URL) | del(.URL) else . end)' <<< "$items")
# echo "$items" > consolidated.json

items=$(jq 'include "./bib-fns";map(getTargetInfo)' <<< "$items")
# echo "$items" > withTargetInfo.json

# now use children items to amend the info for the parentItem
allFixupInfo=$(jq 'group_by(.target)|map(sort_by(.parentItem))' <<< "$items")
# echo "$allFixupInfoGrouped" > allFixupInfoGrouped.json
# embed children into their parentItem (children field). Then delete items that Zotero indicated as such.
items=$(jq 'map(if has(1) then (first + {children: .[1:]}) else first end)|map(select(.deleted|not))' <<< "$allFixupInfo")
# echo "$items" > itemsNestedChildren.json

# echo "Got $(jq '. | length' <<< "$items") clean, top-level items"
items=$(jq 'include "./bib-fns";map(applyChildrenAmendments)' <<< "$items")
# echo "$items" > updatedItems.json

# absNote=$(jq 'include "./bib-fns";map(select((nonBlankKey("abstract") or nonBlankKey("abstractNote")) and (.abstract != .abstractNote)) | {key: .key, title: .title, abstract: .abstract, abstractNote: .abstractNote})' <<< "$items")
# echo "$absNote" > absNoteMismatch.json
# remove redundant .abstractNote fields
items=$(jq 'include "./bib-fns";map(cleanAbstracts)' <<< "$items")
# echo "$items" > abstractsCleaned.json
noURL=$(jq 'include "./bib-fns";map(select(blankKey("url")))' <<< "$items")
# echo "$noURL" > noURL.json
finalCount=$(jq '. | length' <<< "$items")
# Remove .children arrays, if any. Save space.
items=$(jq 'map(del(.children))' <<< "$items")
# Group by year
items=$(jq 'group_by(.issued."date-parts"[0][0])' <<< "$items")
# echo "$items" > 4-grouped.json
items=$(jq 'map({ (.[0].issued."date-parts"[0][0] // "Undated" | tostring): . })' <<< "$items")
# echo "$items" > 5-Undated.json
items=$(jq 'map(to_entries)' <<< "$items")
# echo "$items" > 6-entries.json
items=$(jq 'flatten(1)' <<< "$items")
# echo "$items" > 7-flattened.json
items=$(jq 'group_by(.key)' <<< "$items")
# echo "$items" > 8-groupedByKey.json
items=$(jq 'include "./bib-fns";map(reconstituteGroupedEntries) | from_entries' <<< "$items")
# echo "$items" > 9-final.json


echo "Outputting CSL JSON"
echo "$finalCount entries"
echo "$items" > "$(dirname "$0")/../static/data/bibliography.json"
