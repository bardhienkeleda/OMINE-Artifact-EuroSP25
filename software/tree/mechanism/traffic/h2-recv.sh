
#!/bin/bash

# Default values
NUM_HOPS=5
PATH_VALUE=1
HOST="h4"

# Allowed values
VALID_HOSTS=("h2" "h3" "h4")

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --num-hops) 
            if [[ "$2" != "5" && "$2" != "9" ]]; then
                echo "Error: --num-hops can only be 5 or 9."
                exit 1
            fi
            NUM_HOPS="$2"; shift ;;
        --host) 
            if [[ ! " ${VALID_HOSTS[@]} " =~ " ${2} " ]]; then
                echo "Error: Invalid host '${2}'. Allowed values: h2, h3, h4."
                exit 1
            fi
            HOST="$2"; shift ;;
        *) 
            echo "Unknown parameter passed: $1"
            exit 1 ;;
    esac
    shift
done

# Output the selected values
echo "Host: $HOST"
echo "Number of hops: $NUM_HOPS"

# Execute the Python script with the selected options
python h2-recv.py --host "$HOST" --num-hops "$NUM_HOPS"
