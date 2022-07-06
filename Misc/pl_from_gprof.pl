#!/usr/bin/perl -w
# Courtesy robert.nielsen@everest.com

use strict;
use Data::Dumper;

$Data::Dumper::Purity = 1;
$Data::Dumper::Terse  = 1;

undef $/;
my $in = <STDIN>;
my ($flat, $call_graph, $index_str) = split /\cL/, $in;
my $root = {};

$flat =~ s/^\s*[Ff]lat\s+profile:\s+.*?\s+time\s+seconds\s+seconds\s+calls\s+[Tt]s\/call\s+[Tt]s\/call\s+name\s*\n//s;
my $line;
my $flat_profile = [];
foreach $line (split /\n/, $flat)
{
    if($line =~ m/\s*(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.*)\s*/)
    {
	my $entry = { 'time' => "$1", 'cum_sec' => "$2", 'self_sec' => "$3", 'calls' => "$4", 'self_sec_per_call' => "$5", 'total_sec_per_call' => "$6" , 'name' => "$7" };
	push @$flat_profile, $entry;
    }
    else
    {
    }
}
$$root{flat_profile} = $flat_profile;

$index_str =~ s/^\s*[Ii]ndex\s+by\s+function\s+name\s*//s;
$index_str =~ s/\s*(\[\d+\])/\n$1/g;
$index_str =~ s/^\n+//;

my %index = map { /^(\[\d+\])\s*(.*?)\s*$/ or die; ($1, $2) } split(/\n/, $index_str);

$main::block = qr{
                    \<
                    (?:
                       (?> [^<>]+ )         # Non-framing without backtracking
                       |
                       (?{ $main::block }) # Group with matching framing
                    )*
                    \>
                 }x;
my ($key, $val);
while(($key, $val) = each(%index))
{
    $val =~ s/$main::block/<>/g;
    $index{$key} = $val;
}

#print Dumper \%index;
$$root{index} = \%index;

$call_graph =~ s/^.*?index\s+%\s+time\s+self\s+children\s+called\s+name\n//s;

my @entry = split /-+-\n/, $call_graph;
my $file = [];
my $lines;
my $result = [];

foreach $lines (@entry)
{
    my $result_entry = [];
    my @lines = split /\n/, $lines;
    my $line;
    foreach $line (@lines)
    {
	if($line =~ m/(\[\d+\])\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.*?)\s+(\[\d+\])/)
	{
	    my $entry = { 'time' => "$2", 'self' => "$3", 'children' => "$4", 'called' => "$5", 'name' => "$6", 'index' => "$7" };
	    $$entry{name} =~ s/$main::block/<>/g;
	    push @$result_entry, $entry;
	    #print Dumper $entry;
	}
	elsif($line =~ m/\s+(\S+)\s+(\S+)\s+(\S+)\s+(.*?)\s+(\[\d+\])/)
	{
	    my $entry = {                 'self' => "$1", 'children' => "$2", 'called' => "$3", 'name' => "$4", 'index' => "$5" };
	    $$entry{name} =~ s/$main::block/<>/g;
	    push @$result_entry, $entry;
	    #print Dumper $entry;
	}
	else
	{
	}
    }
    push @$result, $result_entry;
}
$$root{call_graph} = $result;
print Dumper $root;
