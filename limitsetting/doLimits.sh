#!/bin/bash

#Needs to be run from CMSSW_7_1_5/src/HiggsAnalysis/CombinedLimit/scripts/


RUNDIR=/home/users/siconglu/Run_Directory/CMSSW_8_1_0/src
#INDIR=${RUNDIR}/WH_MET_limitsetting/cards_40fb_v8
#OUTDIR=${RUNDIR}/WH_MET_limitsetting/scan40fbv9
#declare -a samples=(`cat $INDIR/points_tchwh.txt`)
#_3jets
INDIR=${RUNDIR}/WH_MET_limitsetting/cards_test_04_13
OUTDIR=${RUNDIR}/WH_MET_limitsetting/scan_test_04_13
declare -a samples=(`cat cards/points_tchwh.txt`)

#The samples is the filenames that is stored in points_tchwh.txt.
cp combineCards.py $INDIR/.
cd $INDIR
cmsenv
#need to combine cards from multiple signal regions if necessary
for i in "${samples[@]}"
do
  echo $i
  if [ ! -e "$INDIR/datacard_all_$i.txt" ]; then
    python combineCards.py "$INDIR/datacard_"*"_$i.txt" > "$INDIR/datacard_all_$i.txt"  
  fi
done

cd /home/users/siconglu/WH_MET/limitsetting/
if [ ! -d "$OUTDIR" ]; then
  mkdir -p "$OUTDIR"
  mkdir -p "$OUTDIR/log"
fi

pushd .
cp make_rValues.C "$OUTDIR"
cp makeLimitTable.C "$OUTDIR"
cp make_contour.C "$OUTDIR"
cp smooth.C "$OUTDIR"
cp xsec_susy_13tev.root  "$OUTDIR"
cd "$OUTDIR"
cmsenv

for i in "${samples[@]}"
do
  echo "Running command: combine -M Asymptotic -n "$i" "$INDIR/datacard_all_$i.txt" > "log/limit_$i.txt" 2>&1"
  combine -M Asymptotic -n "$i" "$INDIR/datacard_all_$i.txt" > "log/limit_$i.log" 2>&1
  mv "higgsCombine"$i".Asymptotic.mH120.root" "limit_"$i".root"
  MODEL=$(echo "$i"|awk -F- 'split($1,a,"_")&&$0=a[1]') #because awk
  MASS1=$(echo "$i"|awk -F- 'split($1,a,"_")&&$0=a[2]')
  MASS2=$(echo "$i"|awk -F- 'split($1,a,"_")&&$0=a[3]')
  root -b -q "make_rValues.C(\"$MODEL\",$MASS1,$MASS2)" > /dev/null 2>&1
  #" >/dev/null 2>&1 is redirect the output of your program to /dev/null. Include both the Standard Error and Standard Out."
done

root -b -q "smooth.C(\"$MODEL\")" #FIXME
root -b -q "make_contour.C(\"$MODEL\")"
root -b -q makeLimitTable.C > table.txt 2>&1

rm make_rValues.C
rm makeLimitTable.C
rm roostats*
popd
