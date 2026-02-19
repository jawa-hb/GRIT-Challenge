import os
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

LEADERBOARD_PATH = Path("leaderboard/leaderboard.csv")

def main(score, submission_path, metadata_path):
    score = float(score)
    submission_path = Path(submission_path)
    metadata_path = Path(metadata_path)

    if not metadata_path.exists():
        raise Exception("metadata.json not found")

    with open(metadata_path) as f:
        metadata = json.load(f)

    team = metadata.get("team", "unspecified")
    model_type = metadata.get("model", "unspecified")
    notes = metadata.get("notes", "nothing")

    new_row = {
        "timestamp_utc": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "team": team,
        "model": model_type,
        "score": score,
        "notes": notes
    }

    # Create leaderboard if it doesn't exist
    if LEADERBOARD_PATH.exists():
        df = pd.read_csv(LEADERBOARD_PATH)
    else:
        df = pd.DataFrame(columns=new_row.keys())

    # Only add new submission if participant not already in leaderboard
    if team not in df['team'].values:
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Sort ascending by score
    df = df.sort_values("score", ascending=True).reset_index(drop=True)

    # Competition ranking: ties share rank, next ranks skipped
    df['rank'] = df['score'].rank(method='min', ascending=True).astype(int)

    # Save updated leaderboard
    df.to_csv(LEADERBOARD_PATH, index=False)
    print("Leaderboard updated successfully.")


if __name__ == "__main__":
    main(
        score=os.environ["SCORE"],
        submission_path=sys.argv[1],
        metadata_path=sys.argv[2]
    )
