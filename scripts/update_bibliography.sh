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
        local this_page=$(curl -s "https://api.zotero.org/groups/$GROUP_ID/collections/$collection_key/items/top?include=data,csljson&start=$start&limit=$limit&v=3")
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
add_items_from_collection $root_collection

echo "Got $(jq '. | length' <<< "$items") items"

# Piece-wise processing for debugging:
items=$(jq 'sort_by(.data.date)' <<< "$items")
# echo "$items" > sorted.json
items=$(jq 'map(.csljson)' <<< "$items")
# echo "$items" > mapped.json
items=$(jq 'group_by(.issued."date-parts"[0][0])' <<< "$items")
# echo "$items" > grouped.json
items=$(jq 'map({ (.[0].issued."date-parts"[0][0] // "Undated" | tostring): . })' <<< "$items")
# echo "$items" > mapped2.json
items=$(jq 'map(to_entries)' <<< "$items")
# echo "$items" > entries.json
items=$(jq 'flatten(1)' <<< "$items")
# echo "$items" > flattened.json
items=$(jq 'group_by(.key)' <<< "$items")
# echo "$items" > groupedByKey.json
items=$(jq 'map(if length == 1 then .[0] else ( { key: (.[0].key), value: (map(.value ) | flatten(1)) } ) end) | from_entries' <<< "$items")
# echo "$items" > xx.json


echo "Outputting CSL JSON"
echo "$items" > "$(dirname "$0")/../data/bibliography.json"
