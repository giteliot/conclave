import pandas as pd
import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any
import sys


ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OR_KEY")
MODEL = "google/gemini-2.5-flash-preview"
PROMPTS_DIR = "./data/prompts"

def get_cardinal_vote(cardinal: str, candidates: list, round: int, last_result: str, api_key: str) -> str:
    # Read the cardinal's persona prompt
    prompt_file = f"{PROMPTS_DIR}/{cardinal['Rank']}.txt"
    if not os.path.exists(prompt_file):
        raise FileNotFoundError(f"No prompt found for {cardinal}")
    
    with open(prompt_file, "r") as f:
        persona_prompt = f.read()

    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/yourusername/conclave",
        "Content-Type": "application/json"
    }
    
    system_prompt = f"""You are cardinal {cardinal['Name']}.
    {persona_prompt}"""

    user_prompt = f"""It is now round {round} of the papal conclave. 
    {last_result}
    It's now time to vote for the next pope. 
    Write down the name, and EXCLUSIVELY THE NAME, among the following candidates: {', '.join(sorted(candidates, key=lambda _: os.urandom(4)))}
    If you write anthing except the name, God himself will send you to hell. 

    Your vote:
    """

    response = requests.post(
        ENDPOINT,
        headers=headers,
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.7,
        }
    )
    return response.json()['choices'][0]['message']['content']

def process_cardinal_vote(cardinal: Dict[str, Any], candidates: list, round: int, last_result: str, api_key: str) -> None:
    """Process a single cardinal's vote and save it to a file."""
    output_file = f"./data/votes/round_{round}/{cardinal['Rank']}.txt"
    if os.path.exists(output_file):
        return
    vote = get_cardinal_vote(cardinal, candidates, round, last_result, api_key)
    with open(output_file, "w") as f:
        f.write(vote)

def main(round: int):
    assert API_KEY is not None, "OpenRouter API key is not set"
    
    df = pd.read_csv("./data/cardinals.csv")
    df = df[-df["Name"].str.contains("\*")]     
    available_cardinals = df.Name.tolist()
    
    os.makedirs(f"./data/votes/round_{round}", exist_ok=True)

    if round > 1:
        with open(f"./data/results_round_{round-1}.txt", "r") as f:
            result = f"The result of the previous round is:\n{f.read()}"
    elif round > 2:
        with open(f"./data/results_round_{round-2}.txt", "r") as f:
            result += f"And the result of the round before the last is:\n{f.read()}"
    else:
        result = ""
    
    # Number of parallel workers
    N = 3  # You can adjust this number based on your needs
    
    with ThreadPoolExecutor(max_workers=N) as executor:
        # Submit all tasks
        future_to_cardinal = {
            executor.submit(process_cardinal_vote, cardinal.to_dict(), available_cardinals, round, result, API_KEY): cardinal['Name']
            for _, cardinal in df.iterrows()
        }
        
        # Process completed tasks as they finish
        for future in as_completed(future_to_cardinal):
            cardinal_name = future_to_cardinal[future]
            try:
                future.result()
                print(f"Completed processing {cardinal_name}")
            except Exception as e:
                print(f"Error processing {cardinal_name}: {str(e)}")

if __name__ == "__main__":
    
    round_number = int(sys.argv[1])
    
    main(round_number)