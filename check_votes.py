import os
from collections import Counter
from typing import List, Tuple
import sys


def main(round: int) -> List[Tuple[str, int, float]]:
    # Construct the path to the votes directory for this round
    votes_dir = f"./data/votes/round_{round}"
    
    # Initialize counter for votes
    vote_counts = Counter()
    
    # Read all vote files
    for filename in os.listdir(votes_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(votes_dir, filename), 'r') as f:
                vote = f.read().strip().replace('\n', '').replace('\r', '')
                vote_counts[vote] += 1
    
    # Calculate total votes
    total_votes = sum(vote_counts.values())
    
    # Create list of tuples (name, votes, percentage)
    results = []
    for name, votes in vote_counts.most_common():
        percentage = (votes / total_votes) * 100
        results.append((name, votes, percentage))
    
    return results

if __name__ == "__main__":
    current_round = int(sys.argv[1])
    results = main(current_round)
    other_votes = 0
    # Print results in a formatted way
    out = f"Result of round {current_round}\n"

    for name, votes, percentage in results:
        if votes > 4:
            out += f"{name}: {votes} votes ({percentage:.1f}%)\n"
        else:
            other_votes += 1
    out += f"Also {other_votes} other cardinals got less than 5 votes.\n"

    if results and results[0][2] > 66:  
        out += f"\nWe have a new pope! {results[0][0]} has been elected with {results[0][2]:.1f}% of the votes."
    else:
        out += "\nNo candidate has reached the required 2/3 majority. The conclave continues."

    with open(f"./data/results_round_{current_round}.txt", "w") as f:
        f.write(out)
    print(out)