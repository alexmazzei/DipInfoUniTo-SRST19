while($line=<>){ 
$line =~s/ à le / au /ig;
$line =~s/ À le / au /ig;
$line =~s/ à lequel / auquel /ig;
$line =~s/ à les / aux /ig;
$line =~s/ À les / aux /ig;
$line =~s/ à lesquelles / auxquelles /ig;
$line =~s/ à lesquels / auxquels /ig;
$line =~s/ de le / du /ig;
$line =~s/ de lequel / duquel /ig;
$line =~s/ de les / des /ig;
$line =~s/ de lesquelles / desquelles /ig;
$line =~s/ des plans / des /ig;
print $line; }
