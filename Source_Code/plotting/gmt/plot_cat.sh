PS_MEDIA=$1
output=$2
region=$3
projection=$4
boundary=$5
position=$6
cat_filepath=$7

gmtset PS_MEDIA             = $PS_MEDIA 
gmtset FONT_ANNOT_PRIMARY= 7p,Helvetica,black
gmtset FONT_ANNOT_SECONDARY= 6p,Helvetica,black
gmtset FONT_LABEL= 8p,Helvetica,black

out="${output}.ps"

psbasemap -K $region $projection $boundary $position > $out

pscoast -O -K -R -J -W0.5 >> $out

awk '{ print $4,$3 }' $cat_filepath > tmp.xy
psxy -O -R -J tmp.xy -Sc.01 -Gred >> $out

rm tmp*
psconvert $out -Tf
rm $out
open "${output}.pdf"
