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
# xitems=$(jq 'sort_by(.data.date)' <<< "$items")
# echo "$xitems" > sorted.json
# xitems=$(jq 'map(.csljson)' <<< "$xitems")
# echo "$xitems" > mapped.json
# xitems=$(jq 'group_by(.issued."date-parts"[0][0])' <<< "$xitems")
# echo "$xitems" > grouped.json
# xitems=$(jq 'map({ (.[0].issued."date-parts"[0][0] // "Undated" | tostring): . })' <<< "$xitems")
# echo "$xitems" > mapped2.json
# xitems=$(jq -s 'add' <<< "$xitems")
# echo "$xitems" > added.json

items=$(jq '
    sort_by(.data.date)
    | map(.csljson)
    | group_by(.issued."date-parts"[0][0])
    | map({ (.[0].issued."date-parts"[0][0] // "Undated" | tostring): . })' <<< "$items")
# The 'add' dropped entries unless jq invoked in "--slurp' mode
items=$(jq -s 'add' <<< "$items")

echo "Outputting CSL JSON"
echo "$items" > "$(dirname "$0")/../data/bibliography.json"
