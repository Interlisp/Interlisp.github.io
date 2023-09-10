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
# echo "$items" > 0-rawItems.json
items=$(jq 'map(.csljson * .data)' <<< "$items")
# echo "$items" > 1-mapped.json

items=$(jq 'map(if has("note") then .note |= sub("^<div.+?>(?<body>.*)</div>$"; "\(.body)"; "gm") else . end)' <<< "$items")
# echo "$items" > 2-cleanDiv.json
#find and eliminate duplicate .id entries
groupedByID=$(jq 'group_by(.id)' <<< "$items")
dupIDs=$(jq 'map(select(length>1) | .[0])' <<< "$groupedByID")
# echo "$dupIDs" > dupIDs.json
#remove duplicates
items=$(jq 'map(.[0]) | sort_by(.date)' <<< "$groupedByID")
# echo "$items" > 3-noDupSorted.json
finalCount=$(jq '. | length' <<< "$items")
# onlyURL=$(jq 'map(if ((has("url") and (.url | tostring | length)) | not) and (has("URL") and (.URL | tostring | length)) then . else empty end)' <<< "$items")
# echo "$onlyURL" > onlyURL.json
# consolidate URL into url key
# consolidated=$(jq 'map(if (has("URL") and (.URL | tostring | length)) then setpath(["url"]; .URL) | del(.URL) else . end)' <<< "$items")
# echo "$consolidated" > consolidated.json
# noURL=$(jq 'map(if (has("url") and (.url | tostring | length >= 1)) then empty else . end) | . // empty' <<< "$items")
# echo "$noURL" > noURL.json
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
items=$(jq 'map(if length == 1 then .[0] else ( { key: (.[0].key), value: (map(.value ) | flatten(1)) } ) end) | from_entries' <<< "$items")
# echo "$items" > 9-final.json


echo "Outputting CSL JSON"
echo "$finalCount entries"
echo "$items" > "$(dirname "$0")/../data/bibliography.json"
