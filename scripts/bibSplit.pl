#! /usr/bin/perl -n
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
  
  my $itemTitle = '""';
  if(/"title"\:("(?:[^"\\]++|\\.)*+")/) {
    $itemTitle = $1;
  } else {
    print STDERR "Cannot find title for key \"$key\" in line: $_\n";
  }

  my $itemAbstract = '""';
  if(/"abstract"\:("(?:[^"\\]++|\\.)*+")/) {
    $itemAbstract = $1;
  } else {
    print STDERR "Cannot find abstract for key \"$key\" in line: $_\n";
  }

  my $itemDate = '""';
  if(/"isoDateString"\:("(?:[^"\\]++|\\.)*+")/) {
    $itemDate = $1;
  } else {
    print STDERR "Cannot find isoDateString for key \"$key\" in line: $_\n";
  }

  my $itemAuthors = '';
  if(/"authorsFormatted"\:\s*\[(.*?)\]/) {
    my $authors_str = $1;
    my @authors;
    while ($authors_str =~ /"(.*?)"/g) {
      push @authors, $1;
    }
    if (@authors) {
      $itemAuthors = "\n";
      foreach my $author (@authors) {
        $itemAuthors .= "  - \"$author\"\n";
      }
      $itemAuthors =~ s/\n$//; # Remove trailing newline
    } else {
      $itemAuthors = '""';
      print STDERR "Cannot parse authors for key \"$key\" in line: $_\n";
    }
  } else {
    $itemAuthors = '""';
    print STDERR "Cannot find authors for key \"$key\" in line: $_\n";
  }

  $handle = undef;
  my $itemmd = "$bibDir/$key.md";
  open($handle, ">", $itemmd) || die "$0: cannot open $itemmd in write-open mode: $!";
  print $handle <<ENDITEM;
---
title: $itemTitle
date: $itemDate
authors: $itemAuthors
publication:
abstract: $itemAbstract
abstract_short:
tags:
url_source:
zotero_url: "https://www.zotero.org/groups/2914042/items/$key"
---

{{< bibItem key="$key" >}}
ENDITEM
  close $handle || die "$0: close of file $itemmd failed: $!";
  
}
