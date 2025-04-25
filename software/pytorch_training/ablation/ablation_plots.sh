#layers=("88882" "88442" "84442")
layers=("84442")
sumduration=0
counter=0

for i in ${!layers[@]};
do
    start=$SECONDS
    python3 ablation_plots.py --NN_structure ${layers[$i]}
    duration=$(( SECONDS - start ))
    sumduration=$((sumduration+duration))
    counter=$((counter+1))

done

avgduration=$(echo "$sumduration/$counter" | bc -l)
echo avgduration: ${avgduration}