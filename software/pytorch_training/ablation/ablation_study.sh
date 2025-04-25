#layers=("16 16 8 8 2" "8 8 8 8 2" "8 8 4 4 2" "8 4 4 4 2")
layers=("8 4 4 4 2")
epochs=(10 20 30)
batch_size=(32)
learning_rate=(0.001 0.0025 0.01)
number_features=7
data_sampling=0.8

sumduration=0
counter=0

for i in ${!layers[@]};
do
    for j in ${!epochs[@]};
    do 
        for k in ${!learning_rate[@]};
        do
            start=$SECONDS
            python3 ablation_study.py --layers ${layers[$i]} --batch_size="${batch_size}" --epochs="${epochs[$j]}" --learning_rate="${learning_rate[$k]}" --data_sampling="${data_sampling}" 
            duration=$(( SECONDS - start ))
            sumduration=$((sumduration+duration))
            counter=$((counter+1))
        done
    done

done

avgduration=$(echo "$sumduration/$counter" | bc -l)
echo avgduration: ${avgduration}