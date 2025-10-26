# Module of JQ functions for manipulating JSON returned from Zotero API

def dbg($label; $value):
    . as $in
    | (($label + ": " + ($value | tojson)) | debug)    # prints to stderr
    | $in;                                             # return original value

def nonBlankKey($keyName): 
  has($keyName) and (.[$keyName] | tostring | length >= 1);

def blankKey($keyName): 
  (has($keyName) and (.[$keyName] | tostring | length >= 1)) | not;

def unwrapDiv:
  sub("^<div.+?>(?<body>.*)</div>$"; "\(.body)"; "gm");

def moveURL_to_url:
  select(nonBlankKey("URL")) | (setpath(["url"]; .URL) | del(.URL)) // .;

def raise_issued_date_parts:
  if nonBlankKey("issued") and (.issued | nonBlankKey("date-parts")) then setpath(["issuedDateParts"]; .issued."date-parts"[0]) else . end;

def pad2: tostring | if length==1 then "0"+. else . end;

def issued_iso_string:
  if nonBlankKey("issued") and (.issued | nonBlankKey("date-parts")) then 
    setpath(["isoDateString"]; 
    (.issued["date-parts"][0]) as $p | ($p[0]|tostring) + "-" + (($p[1]? // 1)|pad2) + "-" + (($p[2]? // 1)|pad2))
  else 
    . 
  end;

def format_person_name:
      if (has("family") and .family != null and (.family|tostring|length)>0) then
        .family
        + ( if (has("given") and .given != null and (.given|tostring|length)>0)
            then ", " + (.given|tostring)
            else "" end )
      elif (has("lastName") and .lastName != null) then
        .lastName
        + ( if (has("firstName") and .firstName != null and (.firstName|tostring|length)>0)
            then ", " + (.firstName|tostring)
            else "" end )
      elif (has("name") and .name != null) then
        .name
      else
        empty
  end;

# Build ["Family, Given", "Family2, Given2", ...] string array from .author array.
# Falls back to other common shapes (name / firstName+lastName). Skips empty parts.
def author_string_list:
  ( .author // [] )
#  | dbg("author_string_list.count"; length)
  | map(format_person_name);

# If you want the field added into each item:
def add_author_string:
  if (.author) then . + { authorsFormatted: (author_string_list) } end;
  
# Likewise for editors
def editor_string_list:
  ( .editor // [] )
#  | dbg("editor_string_list.count"; length)
  | map(format_person_name);

# If you want the field added into each item:
def add_editor_string:
  if (.editor) then. + { editorsFormatted: (editor_string_list) } end;

def make_DOI_to_url($doi):
  if ($doi | startswith("https:")) then $doi else "https://doi.org/" + ($doi | ltrimstr("/")) end ;

def cleanAbstracts:
  if blankKey("abstract") and nonBlankKey("abstractNote") then
    setpath(["abstract"]; .abstractNote) | del(.abstractNote) 
  elif blankKey("abstractNote") or (nonBlankKey("abstract") and (.abstract == .abstractNote)) then 
    del(.abstractNote) 
  else
    .
  end;

def getTargetInfo:
  {target: (.parentItem // .key)} + .;
  
def reconstituteGroupedEntries:  # assumes that array of all entries in a group (effectively by year) is the input
  if length == 1 then .[0] else ( { key: (.[0].key), value: (map(.value ) | flatten(1) ) } ) end | .value |= sort_by(.title);
  
def updateParentUrl:
    . as $parent 
    | (.children | map(select(nonBlankKey("url")) | .url)) as $childurls
    # For now, use first child url to set for blank parent url
    | if ($childurls | length >= 1) then
        #only 1
        if blankKey("url") then         # parent has no url
          . * {url: $childurls[0]}
        else
          .                              # For now, don't do anything here
        end
      else                               # For now, don't do anything here, either
      # none or many
        .
      end;

def applyChildrenAmendments:
  if (.children | length < 1) then 
    . 
  else
    updateParentUrl
#    . as $parent |
#    if (blankKey("url")) then 
#      .children 
#      | map(select()) as $url | .url |= $url 
#    else 
#      .children 
#         | map(select()) as $url | .url |= $url 
#      .
#    end;
  end;
  
def getNeededUrls:  # assumes that array of all current items is the input
    map(.key) as $keys                      # extract all existing keys and keep 'em handy
  | map(                                 # collect all of the "up" link urls and their keys
        .links.up.href                  # get the "up" link url
        | select(. != null)             # only if there IS an up url
        | [(split("/")|last), .])        # make an array with the key, and the url; an entry in the collected array
  | map(                                # for each key/url pair
        .[0] as $k                         # get the key
        | select(($keys | all(. != $k)))   # if this key isn't already in the $keys
        | .[1]?)                          # include this url in this collected array
;

# def intersection(x;y):
#   if (y|length) == 0 then
#     []
#   else (x|unique) as $x
#     | $x - ($x - y)
#   end;
  
def semiflatten:  # assumes that only one item is the input
    . as $item
  | (keys - ["csljson","data"]) as $topKeys
  | ((.csljson // {}) * .data) as $inner
  | (($inner | keys) - ["key","version"]) as $innerKeys
  | (  ($topKeys | map(. as $tKey | {"key": $tKey, "value": ($item | getpath([$tKey]))}))
     + ($innerKeys | map(. as $iKey | {"key": $iKey, "value": ($inner | getpath([$iKey]))})) )
  | from_entries;
    
def bibItem:  # assumes that only one item is the input
    . as $item
  | (keys - ["key","title","target"]) as $tailKeys
  | {"key": .key, "title": .title, "target": .target } + ($tailKeys | map(. as $tKey | {"key": $tKey, "value": ($item | getpath([$tKey]))}) | from_entries);


def removeEmptyKeys:
    with_entries(select(.value != "" and .value != null and .value != [] and .value != {}));