# Conclave

A simulation of a papal conclave using AI to model cardinal voting behavior.

## Prerequisites

- Python 3.x
- OpenRouter API key

## Setup

1. Export your OpenRouter API key:
```bash
export OR_KEY="your-api-key-here"
```

2. Install required Python packages:
```bash
pip install pandas requests
```

## Usage

The simulation runs in three main steps:

1. First, run the scraper to generate cardinal personas:
```bash
python scrape.py
```

2. For each round of voting, run the election script:
```bash
python elect.py <round_number>
```

3. After each round, check the results:
```bash
python check_votes.py <round_number>
```

Alternatively, you can run the entire conclave simulation at once using:
```bash
python run.py
```

## How it Works

1. `scrape.py` generates detailed persona prompts for each cardinal based on their background and history.

2. `elect.py` simulates a round of voting where each cardinal casts their vote based on their persona and the current state of the conclave.

3. `check_votes.py` tallies the votes and determines if a pope has been elected (requires 2/3 majority).

## Data Structure

- `./data/prompts/` - Contains generated persona prompts for each cardinal
- `./data/votes/round_X/` - Contains individual votes for each round
- `./data/results_round_X.txt` - Contains the results summary for each round
