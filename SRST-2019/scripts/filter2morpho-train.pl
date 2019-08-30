#!/usr/bin/perl

$test = 0;

while(<>)
{

    if(!($_ =~ /^\d+\-\d+/ || $_ =~  /^\#/ || $_ eq "\n"))
    {
	#print $_;
	$_ =~ /^([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)$/;
	$uPoS = $4;
	$xPoS = $5;
	$rel = $8;
	if($test == 0)
	{ 
	    $lemma = $3;
	    $form =  $2;
	}
	else
	{
	    $lemma = $2;
	    $form = $3;
	}
	$features = $6;
	
	#print ">>>>>" . $features . "<\n";
	if($features ne "\_")
	{
	    $features =~ s/(\|?)original\_id=\d+//;
	    $features =~ s/lin=(\+|\-)\d+//;
	    $features =~ s/\|/,/g;
	    $out = "$lemma\t" . "uPoS=$uPoS," . "xPoS=$xPoS," . "rel=$rel," . $features . "\t" . $form . "\n";
	    $out =~ s/,,/,/g;
	    $out =~ s/\t,/\t/g;
	    $out =~ s/,\t/\t/g;
	    print $out;
	} 
    }
    #print "\n";
}
