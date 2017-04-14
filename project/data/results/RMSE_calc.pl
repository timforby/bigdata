#For the sake of keeping this correct i just copy this in my results files and run them as a perl program

# A simple implementation of the RMSE calculation used for the Netflix Prize
use strict;
use warnings;
my $numValues = 0;
my $sumSquaredValues = 0;
while (<DATA>) {
    my ($rating,$prediction) = split(/\,/);
    my $delta = $rating - $prediction;
    if ($rating != 0){
    	$numValues++;
	}
    $sumSquaredValues += $delta*$delta;
	printf "%.5f\n", sqrt($sumSquaredValues/$numValues);

}
# Let perl do the truncation to 0.0001
#printf "%d pairs RMSE: %.5f\n", $numValues, sqrt($sumSquaredValues/$numValues);

# Some example data rating & prediction data
# NOTE: This is NOT in the proper prize format
__DATA__