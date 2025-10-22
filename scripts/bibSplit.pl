#! /usr/bin/perl -n
use JSON::PP qw(decode_json encode_json);
use Encode qw(encode);  

BEGIN 
{ 
  $bibDir = $ENV{'BIBLIOGRAPHY_DIR'};
  $bibItemsDir = $ENV{'BIBITEMS_DIR'};
}
my $item = $_;

/"key"\:"([A-Za-z0-9]{8})"/ || print STDERR "Cannot find key in line: $_\n";
my $key = $1;
/"target"\:"([A-Za-z0-9]{8})"/ || print STDERR "Cannot find target for key \"$key\" in line: $_\n";
my $target = $1;
if ($key eq $target) {  # only top level entries
  my $handle = undef;
  my $itemjson = "$bibItemsDir/$key.json";
  open($handle, ">", $itemjson) || die "$0: cannot open $itemjson in write-open mode: $!";
  print $handle $item;
  close $handle || die "$0: close of file $itemjson failed: $!";


my $obj = eval { decode_json($item) } or do { warn "Bad JSON for $key\n"; next; };
delete $obj->{children};

my $type = $obj->{type} // '';

my $itemTitle = '""';
if (defined $obj->{title} && $obj->{title} ne '') {
  $itemTitle = encode('ASCII', encode_json($obj->{title}));   # => "The \"editor\" ..."
}
my $itemAbstract = '""';
if (defined $obj->{abstract} && $obj->{abstract} ne '') {
  $itemAbstract = encode('ASCII', encode_json($obj->{abstract}));   # => "The \"editor\" ..."
}
my $itemDate     = defined $obj->{isoDateString} ? $obj->{isoDateString} : '';

  my $itemAuthors = '';
  if (ref($obj->{authorsFormatted}) eq 'ARRAY' && @{$obj->{authorsFormatted}}) {
    $itemAuthors = "\n";
    for my $a (@{$obj->{authorsFormatted}}) {
      my $quoted = encode_json($a // '');
      $itemAuthors .= "  - $quoted\n";
    }
    $itemAuthors =~ s/\n$//;  # strip trailing newline
  }

# optional fields - ones used vary by value of type
  my $applicationNumber = defined $obj->{applicationNumber} ? qq{"$obj->{applicationNumber}"} : '""';
  my $assignee = defined $obj->{assignee} ? qq{"$obj->{assignees}"} : '""';
  my $blogTitle = defined $obj->{blogTitle} ? qq{"$obj->{blogTitle}"} : '""';
  my $conferenceName = defined $obj->{conferenceName} ? qq{"$obj->{conferenceName}"} : '""';
  my $filingDate = defined $obj->{filingDate} ? qq{"$obj->{filingDate}"} : '""';
  my $issue = defined $obj->{issue} ? qq{"$obj->{issue}"} : '""';
  my $issueDate = defined $obj->{issueDate} ? qq{"$obj->{issueDate}"} : '""';
  my $issuingAuthority = defined $obj->{issuingAuthority} ? qq{"$obj->{issuingAuthority}"} : '""';
  my $pages = defined $obj->{pages} ? qq{"$obj->{pages}"} : '""';
  my $patentNumber = defined $obj->{patentNumber} ? qq{"$obj->{patentNumber}"} : '""';
  my $place = defined $obj->{place} ? qq{"$obj->{place}"} : '""';
  my $proceedingsTitle = defined $obj->{proceedingsTitle} ? qq{"$obj->{proceedingsTitle}"} : '""';
  my $publisher = defined $obj->{publisher}        ? qq{"$obj->{publisher}"}        : '""';
  my $publicationTitle = defined $obj->{publicationTitle} ? qq{"$obj->{publicationTitle}"} : '""';
  my $reportNumber = defined $obj->{reportNumber} ? qq{"$obj->{reportNumber}"} : '""';
  my $reportType = defined $obj->{reportType} ? qq{"$obj->{reportType}"} : '""';
  my $university = defined $obj->{university} ? qq{"$obj->{university}"} : '""';
  my $volume = defined $obj->{volume} ? qq{"$obj->{volume}"} : '""';



my $extraFields = '';
if ($type eq 'paper-conference') { 
  $extraFields = "conference_name: $conferenceName\nplace: $place\nproceedings_title: $proceedingsTitle\npublisher: $publisher\npages: $pages\n";
} elsif ($type eq 'article-journal' || $itemTypeVal eq 'article_magazine') {
  $extraFields = "publication_title: $publicationTitle\nvolume: $volume\nissue: $issue\npages: $pages\n";
} elsif ($type eq 'article') {
  $extraFields = "publisher: $publisher\n";
} elsif ($type eq 'book') {
  $extraFields = "publisher: $publisher\nplace: $place\n";
} elsif ($type eq 'report') {
  $extraFields = "publisher: $publisher\nreport_number: $reportNumber\nreport_type: $reportType\n";
} elsif ($type eq 'thesis') {
  $extraFields = "university: $university\nplace: $place\n";
} elsif ($type eq 'blogPost') {
  $extraFields = "blog_title: $blogTitle\n";
} elsif ($type eq 'patent') {
  $extraFields = "assignee: $assignee\napplication_number: $applicationNumber\nfiling_date: $filingDate\nissuing_authority: $issuingAuthority\npatent_number: $patentNumber\n";
}

  $handle = undef;
  my $itemmd = "$bibDir/$key.md";
  open($handle, ">", $itemmd) || die "$0: cannot open $itemmd in write-open mode: $!";
  print $handle <<ENDITEM;
---
title: $itemTitle
date: $itemDate
type: bibliography
item_type: $type
authors: $itemAuthors
abstract: $itemAbstract

$extraFields
tags:
url_source:
zotero_url: "https://www.zotero.org/groups/2914042/items/$key"
---

ENDITEM
  close $handle || die "$0: close of file $itemmd failed: $!";
  
}
