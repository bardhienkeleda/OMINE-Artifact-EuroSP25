datasets=("kdd" "unsw" "cicids")
features=("simple" "mid" "simple_mid_features" "best_7_features")
switches=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15)

sumduration=0
counter=0

for i in ${!datasets[@]};
do
    start=$SECONDS
    for j in ${!features[@]};
    do
        for n in in ${!switches[@]};
        do
            python3 tester.py --test_batch 2500 --data="${datasets[$i]}" --node_number="${switches[$n]}" --feature_type="${features[$j]}"
        done
    done
    duration=$((SECONDS - start))
    sumduration=$((sumduration+duration))
    counter=$((counter+1))
done

avgduration=$(echo "$sumduration/$counter" | bc -l)
echo avgduration: ${avgduration}