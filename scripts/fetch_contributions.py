import json
import os
import re
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

USERNAME = "NileshSwain2005"

def fetch_contributions():
    url = f"https://github.com/users/{USERNAME}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    print(f"Fetching contribution calendar for '{USERNAME}'...")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch contributions from GitHub. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Map tooltips by target ID for multi-pass extraction
    tooltips = {}
    for tool_tip in soup.find_all("tool-tip"):
        for_id = tool_tip.get("for")
        if for_id:
            tooltips[for_id] = tool_tip.text.strip()

    days_data = []
    total_contributions = 0

    # Locate all contribution cells (support both <td> and <rect> elements)
    cells = soup.find_all(["td", "rect"], class_=re.compile(r"ContributionCalendar-day"))

    for cell in cells:
        date_str = cell.get("data-date")
        if not date_str:
            continue

        count = 0
        level = int(cell.get("data-level", 0))

        # Method 1: Check explicit data-count attribute
        if cell.has_attr("data-count"):
            count = int(cell["data-count"])
        else:
            # Method 2: Check matching tool-tip element
            cell_id = cell.get("id")
            tooltip_text = tooltips.get(cell_id, "") or cell.get("aria-label", "")
            
            if tooltip_text:
                match = re.search(r"(\d+)\s+contribution", tooltip_text, re.IGNORECASE)
                if match:
                    count = int(match.group(1))
                elif "no contribution" in tooltip_text.lower():
                    count = 0

        total_contributions += count
        days_data.append({
            "date": date_str,
            "count": count,
            "level": level
        })

    # Sort chronologically
    days_data.sort(key=lambda x: x["date"])

    # Calculate Streaks
    current_streak = 0
    longest_streak = 0
    temp_streak = 0

    today_str = datetime.now().strftime("%Y-%m-%d")
    yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    past_days = [d for d in days_data if d["date"] <= today_str]

    for day in past_days:
        if day["count"] > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0

    # Calculate Current Active Streak
    for day in reversed(past_days):
        if day["date"] in [today_str, yesterday_str] and day["count"] == 0:
            continue
        if day["count"] > 0:
            current_streak += 1
        else:
            break

    payload = {
        "username": USERNAME,
        "updated_at": datetime.now().isoformat(),
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "days": days_data
    }

    os.makedirs("data", exist_ok=True)
    output_file = "data/contributions.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Successfully fetched {len(days_data)} days of data.")
    print(f"Total Contributions: {total_contributions} | Current Streak: {current_streak} days | Longest Streak: {longest_streak} days")
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    fetch_contributions()