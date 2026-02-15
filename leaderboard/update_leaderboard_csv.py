import os
import json
import pandas as pd
from pathlib import Path

LEADERBOARD_PATH = Path("leaderboard/leaderboard.csv")
SUBMISSIONS_PATH = Path("submissions/inbox")

def find_latest_submission():
    """
    Find the only submission folder in:
    submissions/inbox/<team>/<run_id>/
    """
    teams = list(SUBMISSIONS_PATH.glob("*/*"))
    if not teams:
        raise Exception("No team folders found in submissions/inbox")

    # Assume one PR = one submission
    team_folder = teams[0]

    runs = list(team_folder.glob("*"))
    if not runs:
        raise Exception("No run_id folders found")

    return runs[0]  # submissions/inbox/team/run_id

def main():
    score = float(os.environ["SCORE"])

    submission_path = find_latest_submission()
    metadata_path = submission_path / "metadata.json"

    if not metadata_path.exists():
        raise Exception("metadata.json not found")

    with open(metadata_path) as f:
        metadata = json.load(f)

    team = metadata.get("team", "unknown")
    model_type = metadata.get("model", "unknown")
    model_name = metadata.get("model_name", "unknown")
    new_row = {
        "timestamp_utc": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "team": team,
        "model": model_type,
        "score": score
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
    main()


