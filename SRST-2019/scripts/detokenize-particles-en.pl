while($line=<>){ 
$line =~s/ are not / aren't /ig;
$line =~s/ can not / cannot /ig;
$line =~s/ can not / can't /ig;
$line =~s/ de les / des /ig;
$line =~s/ do not / don't /ig;
$line =~s/ h ad / had /ig;
$line =~s/ should not / shouldn't /ig;
$line =~s/ will not / won't /ig;
print $line; }
