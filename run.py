import subprocess
import os
import time

def check_for_pope(round_num):
    results_file = f"./data/results_round_{round_num}.txt"
    if not os.path.exists(results_file):
        return False
    
    with open(results_file, 'r') as f:
        content = f.read()
        return "We have a new pope!" in content

def main():
    round_num = 1
    
    while True:
        print(f"\nStarting round {round_num}...")
        
        # Run elect.py
        print("Running elect.py...")
        subprocess.run(["python", "elect.py", str(round_num)], check=True)
        
        # Run check_votes.py
        print("Running check_votes.py...")
        subprocess.run(["python", "check_votes.py", str(round_num)], check=True)
        
        # Check if a pope has been elected
        if check_for_pope(round_num):
            print(f"\nA pope has been elected in round {round_num}!")
            break
        
        print(f"No pope elected in round {round_num}. Continuing to next round...")
        round_num += 1
        time.sleep(1)  # Small delay between rounds

if __name__ == "__main__":
    main() 