#!/usr/bin/perl

while($line = <>)
{

    if($line =~ /^(\d+)\-(\d+)\t([^\t]+)\t/ )
    {
	#print $line;
	$rh =  lc($3);
	$lh ="";
	for ($i =0 ; $i <= $2-$1 ; $i++)
	     {	
		 #print 
		 $line = <>;		 
		 $line =~ /^(\d+)\t([^\t]+)\t/;
		 $lh .= lc($2) . " ";		 
	     }
	$lh =~ s/ $//;
	print "\$line \=\~s\/ $lh \/ $rh \/ig;\n"

    }
}

