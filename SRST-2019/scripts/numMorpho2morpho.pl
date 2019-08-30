#!/usr/bin/perl

$prevLemmaFeats = "";
$lemmaFeatsForm = "";
$max = -1;

while(<>)
{
    if($_ =~ /^ *(\d+) +([^\t]+)\t([^\t]+)\t([^\t]+)\n$/)
    {
	$occourences = $1;
	$lemma = $2;
	$feats = $3;
	$form = $4;
	if($prevLemmaFeats ne "")
	{
	    if($prevLemmaFeats ne ($lemma . "\t" . $feats))
	    {
		print $lemmaFeatsForm;
		$prevLemmaFeats = $lemma . "\t" . $feats;
		$lemmaFeatsForm = $lemma . "\t" . $feats . "\t" . $form . "\n";
		$max = $occourences;
	    }
	    else
	    {
		if( $occourences > $max)
		{
		    #$prevLemmaFeats = $lemma . "\t" . $feats;
		    $lemmaFeatsForm = $lemma . "\t" . $feats . "\t" . $form . "\n";
		    $max = $occourences;
		}
	    }
	}
	else
	{
	    $prevLemmaFeats = $lemma . "\t" . $feats;
	    $lemmaFeatsForm = $lemma . "\t" . $feats . "\t" . $form . "\n";
	    $max = $occourences;
	}
    }
}
