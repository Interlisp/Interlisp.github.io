#! /usr/bin/perl -n
BEGIN { $bibDir = $ENV{'BIBLIOGRAPHY_DIR'}; print "bibDir: $bibDir\n";}
my $item = $_;
/"key"\:"([A-Za-z0-9]{8})"/ || print "Cannot find key on line: $_\n";
my $key = $1;
/"title"\:("(?:[^"\\]++|\\.)*+")/ || print "Cannot find title for key \"$key\" on line: $_\n";
my $itemTitle = $1;
/"target"\:"([A-Za-z0-9]{8})"/ || print "Cannot find target for key \"$key\" on line: $_\n";
my $target = $1;
if ($key eq $target) {  # only top level entries
  # print "KEY: $key TITLE:$itemTitle\n";
  my $handle = undef;
  my $itemfn = "$bibDir/$key.md";
  open($handle, ">", $itemfn) || die "$0: cannot open $itemfn in write-open mode: $!";
  print $handle <<ENDITEM;
{"title": $itemTitle, 
 "weight": "5", 
 "type": "docs", 
 "params": {"bibItem": $item}
}

{{< bibItem >}}
ENDITEM
  close $handle || die "$0: close of file $itemfn failed: $!";
}
else
{
  # print "KEY: $key TARGET: $target TITLE:$itemTitle\n";
}
