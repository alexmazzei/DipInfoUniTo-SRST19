#!/usr/bin/perl

while(<>)
{

    if(!($_ =~ /^\d+\-\d+/ || $_ =~  /^\#/ ))
    {
	print $_;
    }
}
