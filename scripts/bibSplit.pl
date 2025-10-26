#! /usr/bin/perl -n
use JSON::PP qw(decode_json encode_json);
use Encode qw(decode encode is_utf8);  
use Unicode::Normalize qw(NFC);

# Cleanup text fields
sub sanitize_text {
  my ($s) = @_;
  return '' unless defined $s;

  # Ensure decoded characters
  $s = decode('UTF-8', $s, Encode::WARN) unless is_utf8($s);

  # Repair mojibake (e.g., "â" -> "’") if available
  eval {
    require Encode::FixLatin;
    $s = Encode::FixLatin::fix_latin($s);
  };

  # Normalize and clean
  $s = NFC($s);                       # normalize accents/combining marks
  $s =~ s/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F\x{80}-\x{9F}]//g;  # drop C0/C1 controls
  $s =~ s/\x{00A0}/ /g;               # NBSP -> space
  $s =~ s/\r\n?/ /g;                 # normalize newlines

  return $s;
}

BEGIN 
{ 
  $bibDir = $ENV{'BIBLIOGRAPHY_DIR'};
  $bibItemsDir = $ENV{'BIBITEMS_DIR'};
}
my $item = $_;
my $json = eval { decode_json($item) } or do { warn "Bad JSON line: $_\n"; next; };

my $key = $json->{key};
my $target = $json->{target} || print STDERR "Cannot find target for key \"$key\" in line: $_\n";

if ($key eq $target) {  # only top level entries
  my $handle = undef;
  my $itemjson = "$bibItemsDir/$key.json";
  open($handle, ">:encoding(UTF-8)", $itemjson) || die "$0: cannot open $itemjson in write-open mode: $!";
  print $handle $item;
  close $handle || die "$0: close of file $itemjson failed: $!";


  my $obj = eval { decode_json($item) } or do { warn "Bad JSON for $key\n"; next; };
  delete $obj->{children};

  my $type = $obj->{type} // '';

  # Titles can have colons and other special characters.  Place YAML keyword on one line
  # and follow it with the title indented on subsequent line
  my $itemTitle = sanitize_text($obj->{title} // '');
  my $title = $itemTitle eq '' ? "title: ''" : "title: |\n  $itemTitle\n";

  # Abstracts can be multi-line and  contain multiple paragraphs.  Place YAML keyword on
  # one line and follow it with the abstract indented on subsequent lines.
  my $abs = sanitize_text($obj->{abstract} // '');
  # a hack for bulleted lists in the abstracts (use markdown there)
  # won't work for nested lists.
  $abs =~ s/\n?\n\N{U+2022}/\n*/g;
  my $indented = join('', map { "  $_\n" } split(/\n/, $abs));
  my $abstract = $indented eq '' ? "abstract: ''" : "abstract: |\n$indented";

  my $itemDate = defined $obj->{isoDateString} ? $obj->{isoDateString} : '';

  my $itemAuthors = '';
  if (ref($obj->{authorsFormatted}) eq 'ARRAY' && @{$obj->{authorsFormatted}}) {
    $itemAuthors = "\n";
    for my $a (@{$obj->{authorsFormatted}}) {
      my $quoted = encode_json($a // '');
      $itemAuthors .= "  - $quoted\n";
    }
    $itemAuthors =~ s/\n$//;  # strip trailing newline
  }

  my $itemEditors = '';
  if (ref($obj->{editorsFormatted}) eq 'ARRAY' && @{$obj->{editorsFormatted}}) {
    $itemEditors = "\n";
    for my $a (@{$obj->{editorsFormatted}}) {
      my $quoted = encode_json($a // '');
      $itemEditors .= "  - $quoted\n";
    }
    $itemEditors =~ s/\n$//;  # strip trailing newline
  }
  
  my $urlSource = defined $obj->{url} ? $obj->{url} : '';

  # optional fields - ones used vary by value of type
  my $applicationNumber = defined $obj->{applicationNumber} ? qq{"$obj->{applicationNumber}"} : '""';
  my $assignee = defined $obj->{assignee} ? qq{"$obj->{assignees}"} : '""';
  my $blogTitle = defined $obj->{blogTitle} ? qq{"$obj->{blogTitle}"} : '""';
  my $bookTitle = defined $obj->{bookTitle} ? qq{"$obj->{bookTitle}"} : '""';
  my $conferenceName = defined $obj->{conferenceName} ? qq{"$obj->{conferenceName}"} : '""';
  my $encyclopediaTitle = defined $obj->{encyclopediaTitle} ? qq{"$obj->{encyclopediaTitle}"} : '""';
  my $filingDate = defined $obj->{filingDate} ? qq{"$obj->{filingDate}"} : '""';
  my $issue = defined $obj->{issue} ? qq{"$obj->{issue}"} : '""';
  my $issueDate = defined $obj->{issueDate} ? qq{"$obj->{issueDate}"} : '""';
  my $issuingAuthority = defined $obj->{issuingAuthority} ? qq{"$obj->{issuingAuthority}"} : '""';
  my $itemType = defined $obj->{itemType} ? $obj->{itemType} : '';
  my $numberOfVolumes = defined $obj->{numberOfVolumes} ? qq{"$obj->{numberOfVolumes}"} : '""';
  my $pages = defined $obj->{pages} ? qq{"$obj->{pages}"} : '""';
  my $patentNumber = defined $obj->{patentNumber} ? qq{"$obj->{patentNumber}"} : '""';
  my $place = defined $obj->{place} ? qq{"$obj->{place}"} : '""';
  my $proceedingsTitle = defined $obj->{proceedingsTitle} ? qq{"$obj->{proceedingsTitle}"} : '""';
  my $publisher = defined $obj->{publisher}        ? qq{"$obj->{publisher}"}        : '""';
  my $publicationTitle = defined $obj->{publicationTitle} ? qq{"$obj->{publicationTitle}"} : '""';
  my $reportNumber = defined $obj->{reportNumber} ? qq{"$obj->{reportNumber}"} : '""';
  my $reportType = defined $obj->{reportType} ? qq{"$obj->{reportType}"} : '""';
  my $series = defined $obj->{series} ? qq{"$obj->{series}"} : '""';
  my $seriesNumber = defined $obj->{seriesNumber} ? qq{"$obj->{seriesNumber}"} : '""';
  my $seriesTitle = defined $obj->{seriesTitle} ? qq{"$obj->{seriesTitle}"} : '""';
  my $studio = defined $obj->{studio} ? qq{"$obj->{studio}"} : '""';
  my $university = defined $obj->{university} ? qq{"$obj->{university}"} : '""';
  my $videoRecordingFormat = defined $obj->{videoRecordingFormat} ? qq{"$obj->{videoRecordingFormat}"} : '""';
  my $volume = defined $obj->{volume} ? qq{"$obj->{volume}"} : '""';
  my $websiteTitle = defined $obj->{websiteTitle} ? qq{"$obj->{websiteTitle}"} : '""';
  my $websiteType = defined $obj->{websiteType} ? qq{"$obj->{websiteType}"} : '""';

  my $extraFields = '';
  if ($type eq 'paper-conference') { 
   $extraFields = "conference_name: $conferenceName\nplace: $place\nproceedings_title: $proceedingsTitle\npublisher: $publisher\npages: $pages\n";
  } elsif ($type eq 'article-journal' || $type eq 'article-magazine') {
    $extraFields = "publication_title: $publicationTitle\nvolume: $volume\nissue: $issue\npages: $pages\n";
  } elsif ($type eq 'article') {
    $extraFields = "publisher: $publisher\n";
  } elsif ($type eq 'book') {
    $extraFields = "publisher: $publisher\nplace: $place\n";
  } elsif ($type eq 'report') {
    $extraFields = "publisher: $publisher\nreport_number: $reportNumber\nreport_type: $reportType\n";
  } elsif ($type eq 'thesis') {
    $extraFields = "university: $university\nplace: $place\n";
  } elsif ($type eq 'post-weblog') {
    $extraFields = "blog_title: $blogTitle\n";
  } elsif ($type eq 'patent') {
    $extraFields = "assignee: $assignee\napplication_number: $applicationNumber\nfiling_date: $filingDate\nissuing_authority: $issuingAuthority\npatent_number: $patentNumber\n";
  } elsif ($type eq 'motion_picture') {
    $extraFields = "studio: $studio\nvideo_recording_format: $videoRecordingFormat\nseries_title: $seriesTitle\nvolume: $volume\nnumber_of_volumes: $numberOfVolumes\n";
  } elsif ($type eq 'chapter') {
    $extraFields = "book_title: $bookTitle\npublisher: $publisher\nseries: $series\nseries_number: $seriesNumber\npages: $pages\n";
  } elsif ($type eq 'personal_communication') {
    $extraFields = "communication_type: $itemType\n";
  } elsif ($type eq 'webpage') {
  $extraFields = "website_title: $websiteTitle\nwebsite_type: $websiteType\n";
  } elsif ($type eq 'entry-encyclopedia') {
    $extraFields = "encyclopedia_title: $encyclopediaTitle\n";
  } else {
    print STDERR "Warning: unhandled type \"$type\" for key \"$key\"\n";
  }

  # Todo: Remove writing the json file once we're happy with the markdown files
  $handle = undef;
  my $itemmd = "$bibDir/$key.md";
  open($handle, ">:encoding(UTF-8)", $itemmd) || die "$0: cannot open $itemmd in write-open mode: $!";
  print $handle <<ENDITEM;
---
$title
date: $itemDate
type: bibliography
item_type: $type
authors: $itemAuthors
editors: $itemEditors
$abstract

$extraFields
tags:
url_source: $urlSource
zotero_url: "https://www.zotero.org/groups/2914042/items/$key"
---

ENDITEM
  close $handle || die "$0: close of file $itemmd failed: $!";
}
