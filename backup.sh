RUN_NUMBER=$1

mkdir ./data/backups/run_$RUN_NUMBER
mkdir ./data/backups/run_$RUN_NUMBER/votes

mv ./data/votes ./data/backups/run_$RUN_NUMBER/votes
mv ./data/results_round_* ./data/backups/run_$RUN_NUMBER/

