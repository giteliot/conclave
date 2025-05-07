import pandas as pd
import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any

ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OR_KEY")
MODEL = "google/gemini-2.5-flash-preview"
PROMPTS_DIR = "./data/prompts"
os.makedirs(PROMPTS_DIR, exist_ok=True)

def get_cardinal_info(cardinal: dict, api_key: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/yourusername/conclave",
        "Content-Type": "application/json"
    }
    
    system_prompt = """You are a Vatican expert. Provide comprehensive information about this cardinal, including:
- Their background and education
- Key positions held
- Notable contributions to the Church
- Theological views and stances
- Relationships with other cardinals and popes
- Public statements and actions
- Current role and influence
Format the response as a detailed persona prompt that could be used to simulate this cardinal's behavior and knowledge."""
    
    user_prompt = f"""Cardinal {cardinal['Name']}:
- Born: {cardinal['Born']}
- Country: {cardinal['Country']}
- Order: {cardinal['Order']}
- Appointed by: {cardinal['Consistory']}
- Current Office: {cardinal['Office']}
Please provide comprehensive persona prompt about this cardinal."""

    response = requests.post(
        ENDPOINT,
        headers=headers,
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 2000,
            "temperature": 0.1,
        }
    )
    return response.json()['choices'][0]['message']['content']

def process_cardinal(cardinal: Dict[str, Any], api_key: str) -> None:
    """Process a single cardinal and save their prompt to a file."""
    output_file = f"{PROMPTS_DIR}/{cardinal['Rank']}.txt"
    if os.path.exists(output_file):
        return
    prompt = get_cardinal_info(cardinal, api_key)
    with open(output_file, "w") as f:
        f.write(prompt)

def main():
    assert API_KEY is not None, "OpenRouter API key is not set"
    
    # Number of parallel workers
    N = 3  # You can adjust this number based on your needs
    
    df = pd.read_csv("./data/cardinals.csv")
    
    # Create a thread pool with N workers
    with ThreadPoolExecutor(max_workers=N) as executor:
        # Submit all tasks
        future_to_cardinal = {
            executor.submit(process_cardinal, cardinal.to_dict(), API_KEY): cardinal['Name']
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
    main()

