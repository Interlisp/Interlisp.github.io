#! /usr/bin/perl -n
BEGIN 
{ 
  $bibDir = $ENV{'BIBLIOGRAPHY_DIR'};
  $bibItemsDir = $ENV{'BIBITEMS_DIR'};
}
my $item = $_;
/"key"\:"([A-Za-z0-9]{8})"/ || print "Cannot find key in line: $_\n";
my $key = $1;
/"target"\:"([A-Za-z0-9]{8})"/ || print "Cannot find target for key \"$key\" in line: $_\n";
my $target = $1;
if ($key eq $target) {  # only top level entries
  my $handle = undef;
  my $itemjson = "$bibItemsDir/$key.json";
  open($handle, ">", $itemjson) || die "$0: cannot open $itemjson in write-open mode: $!";
  print $handle $item;
  close $handle || die "$0: close of file $itemjson failed: $!";
  
  /"title"\:("(?:[^"\\]++|\\.)*+")/ || print "Cannot find title for key \"$key\" in line: $_\n";
  my $itemTitle = $1;
  $handle = undef;
  my $itemmd = "$bibDir/$key.md";
  open($handle, ">", $itemmd) || die "$0: cannot open $itemmd in write-open mode: $!";
  print $handle <<ENDITEM;
---
title: $itemTitle
weight: 5 
type: docs
---

{{< bibItem key="$key" >}}
ENDITEM
  close $handle || die "$0: close of file $itemmd failed: $!";
  
}
