#!/usr/bin/perl

$templateFile = $ARGV[0];
$resultFile   = $ARGV[1];
$increment    = $ARGV[2];

open(TFILE, "$templateFile");


while ($line = <TFILE>)
{
 #print "DEBUG:: " . $line; 
    
    if($line =~ /id = (\d+)$/)
    {
     #print "DEBUG:: " . $line;
     $number = $1;	
     $shift = $number + $increment;   
     $g = "=" . $shift . "\$";
     $cmd = "grep -A2 \"$g\" $resultFile | tail -n2";
     #print "DEBUG:: CMD=" . $cmd . "\n";
     print "# sent_id =$number\n";
     print `$cmd`; 
    }
}

