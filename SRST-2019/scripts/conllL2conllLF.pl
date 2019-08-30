#!/usr/bin/perl

$fileMORPHO=$ARGV[0];#"it-results-srst18.morpho";
$fileCONLL =$ARGV[1];#"it-ud-test-srst18.conll";

open(MFILE, "$fileMORPHO");
open(CFILE, "$fileCONLL");     

%lfd2form = {};

while($mline = <MFILE>)
{
#    print "line=" . $mline;
    if($mline =~ /^([^\t]+)\t([^\t]+)\t([^\t]+)\n$/)
    {
	$key = $1 . "," .  $2;
	$value = $3;
	$lfd2form{$key} = $value;
	#print "$key------->$value\n";
    }
}
close(MFILE);

while($cline = <CFILE>)
{
    if($cline =~ /^([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\n$/)
    {
	$number = $1;
	$form   = $2;
	$lemma  = $3;    
	$uPoS = $4;
	$xPoS = $5;
	$feats = $6;
	$parent   = $7;
	$relation = $8;    
	$end1 = $9;
	$end2 = $10;

	
	if($feats ne "\_")
	{
	    $features = $feats;
	    $features =~ s/\|/,/g;
	    $entry = $form . ",uPoS=$uPoS," . "xPoS=$xPoS," . "rel=$relation," .  $features;
	    #print "entry=" . $entry . "\n";
	    
	    $realForm = $lfd2form{$entry}; #TOCHECK
	    #print "realForm=" . $realForm . "\n";
	
	}
	else
	{
	    $realForm = $form;
	}
	print $number . "\t". $realForm . "\t". $form . "\t".  $uPoS . "\t". $xPoS . "\t". $feats . "\t". $parent . "\t". $relation . "\t". $end1 . "\t". $end2 . "\n";
    }	     
    else
    {
	print $cline;
    }
}
close(CFILE);
