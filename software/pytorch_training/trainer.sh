switches=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15)
datasets=("unsw")
features=("best_7_features")
batch_size=32
epochs_cicids=10
epochs_other=30
scarsity_level_cicids=0.005
scarsity_level_unsw=0.01

sumduration=0
counter=0

for i in ${!switches[@]};
do
    start=$SECONDS
    for j in ${!datasets[@]};
    do
        for n in ${!features[@]};
        do
            if [ "${datasets[$j]}" = "cicids" ] 
            then
                python3 trainer.py --node_number="${switches[$i]}" --batch_size="$batch_size" --dataset="${datasets[$j]}" --epochs $epochs_cicids --type_features="${features[$n]}" --scarsity_level $scarsity_level_cicids
            else
                python3 trainer.py --node_number="${switches[$i]}" --batch_size="$batch_size" --dataset="${datasets[$j]}" --epochs $epochs_other --type_features="${features[$n]}"  --scarsity_level $scarsity_level_unsw
            fi
        done
    duration=$((SECONDS - start))
    sumduration=$((sumduration+duration))
    counter=$((counter+1))
    done
done

avgduration=$(echo "$sumduration/$counter" | bc -l)
echo avgduration: ${avgduration}