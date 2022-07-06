#!/usr/bin/perl -w
# Courtesy robert.nielsen@everest.com

use strict;
use Data::Dumper;

$Data::Dumper::Purity = 1;
$Data::Dumper::Terse  = 1;

undef $/;
my $in = eval <STDIN>;
#print Dumper $in;
my $out = [];
my $call_graph_tbl = {};

my $entry;
foreach $entry (@{$$in{call_graph}})
{
    my $seq = [[], undef, []];
    my $current_index = 0;
    my $line;
    foreach $line (@$entry)
    {
	if(defined $$line{time})
	{
	    $$seq[1] = $$line{index};
	    $current_index = 2;
	}
	else
	{
	    push @{$$seq[$current_index]}, $$line{index};
	}
	$$call_graph_tbl{$$line{index}} = $$line{name};
    }
    push @$out, $seq;
}
#print Dumper $out;
#print Dumper $call_graph_tbl;
#print Dumper $$in{index};

my $tbl = {};
foreach $entry (@$out)
{
    my $parents  = $$entry[0];
    my $func     = $$entry[1];
    my $func_sig = $$in{index}{$func};
    my $children = $$entry[2];

    my $parent;
    foreach $parent (@$parents)
    {
	my $parent_sig = $$call_graph_tbl{$parent};
	if(defined $$in{index}{$parent})
	{
	    $parent_sig = $$in{index}{$parent};
	}
	my $key = "\"$parent_sig\" -> \"$func_sig\"";
	$$tbl{$key} = undef;
    }

    my $child;
    foreach $child (@$children)
    {
	my $child_sig = $$in{index}{$child};
	my $key = "\"$func_sig\" -> \"$child_sig\"";
	$$tbl{$key} = undef;
    }
}
print "digraph g\n";
print "{\n";
print "  graph [rankdir=LR, rotate=90, page=\"11,17\", size=\"10,16\"];\n";
print "  graph [ratio=compress, mclimit=10];\n";
print "  node  [shape=plaintext];\n";
my ($key, $undef);
while(($key, $undef) = each(%$tbl))
{
    print "  $key;\n";
}
print "}\n";
