"""
Reddit Data Bulk Downloader — Arctic Shift API (Chunk-Save Version)
====================================================================
- Saves every 1000 comments to disk as it goes (crash-safe)
- Stops automatically at MAX_COMMENTS limit
- Resumes from where it left off if interrupted
- Posts already downloaded? Set SKIP_POSTS = True

Run:
    .venv\Scripts\python.exe scripts\download_reddit_data.py
"""

import requests
import json
import time
import os
from datetime import datetime

# CONFIG
SUBREDDIT    = "soccer"
START_DATE   = "2022-11-01"
END_DATE     = "2022-12-20"
BATCH_SIZE   = 100
DELAY        = 0.5
MAX_COMMENTS = 5000
SAVE_EVERY   = 1000
SKIP_POSTS   = True
BASE_URL     = "https://arctic-shift.photon-reddit.com/api"

def date_to_utc(date_str):
    return int(datetime.strptime(date_str, "%Y-%m-%d").timestamp())

def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    size_mb = os.path.getsize(filename) / 1_000_000
    print(f"   Saved {len(data):,} records to {filename} ({size_mb:.1f} MB)")

def download_posts(subreddit, after_ts, before_ts):
    all_posts = []
    after = after_ts
    batch_num = 0
    print(f"\nDownloading POSTS from r/{subreddit}...")

    while True:
        batch_num += 1
        url = (f"{BASE_URL}/posts/search?subreddit={subreddit}"
               f"&after={after}&before={before_ts}&limit={BATCH_SIZE}&sort=asc")
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            batch = resp.json().get("data", [])
        except Exception as e:
            print(f"   Error (batch {batch_num}): {e} retrying in 5s...")
            time.sleep(5)
            continue

        if not batch:
            print("   Posts done.")
            break

        all_posts.extend(batch)
        print(f"   Batch {batch_num}: +{len(batch)} | Total: {len(all_posts):,}")
        after = batch[-1]["created_utc"] + 1

        if len(batch) < BATCH_SIZE:
            print("   Last batch. Posts done.")
            break
        time.sleep(DELAY)

    return all_posts

def download_comments(subreddit, after_ts, before_ts):
    all_comments = []
    after = after_ts
    batch_num = 0
    comments_file = f"comments_{subreddit}.json"

    # Resume from existing file if it exists
    if os.path.exists(comments_file):
        with open(comments_file, "r", encoding="utf-8") as f:
            all_comments = json.load(f)
        after = all_comments[-1]["created_utc"] + 1
        print(f"\nResuming: {len(all_comments):,} comments already saved")
    else:
        print(f"\nDownloading COMMENTS from r/{subreddit}...")

    print(f"   Stopping at {MAX_COMMENTS:,} comments")

    while True:
        if MAX_COMMENTS and len(all_comments) >= MAX_COMMENTS:
            print(f"\n   Reached limit of {MAX_COMMENTS:,} comments. Stopping.")
            break

        batch_num += 1
        url = (f"{BASE_URL}/comments/search?subreddit={subreddit}"
               f"&after={after}&before={before_ts}&limit={BATCH_SIZE}&sort=asc")

        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            batch = resp.json().get("data", [])
        except Exception as e:
            print(f"   Error (batch {batch_num}): {e} retrying in 5s...")
            time.sleep(5)
            continue

        if not batch:
            print("   No more comments. Done.")
            break

        all_comments.extend(batch)
        after = batch[-1]["created_utc"] + 1
        print(f"   Batch {batch_num}: +{len(batch)} | Total: {len(all_comments):,}")

        # Save checkpoint every SAVE_EVERY comments
        if len(all_comments) % SAVE_EVERY < BATCH_SIZE:
            save_json(all_comments, comments_file)
            print(f"   Checkpoint saved!")

        if len(batch) < BATCH_SIZE:
            print("   Last batch. Comments done.")
            break

        time.sleep(DELAY)

    # Final save
    save_json(all_comments, comments_file)
    return all_comments


if __name__ == "__main__":
    after_ts  = date_to_utc(START_DATE)
    before_ts = date_to_utc(END_DATE)

    # POSTS
    posts_file = f"posts_{SUBREDDIT}.json"
    if SKIP_POSTS:
        if os.path.exists(posts_file):
            with open(posts_file, "r", encoding="utf-8") as f:
                posts = json.load(f)
            print(f"Skipping posts - already have {len(posts):,} in {posts_file}")
        else:
            print("SKIP_POSTS=True but posts file not found. Downloading...")
            posts = download_posts(SUBREDDIT, after_ts, before_ts)
            save_json(posts, posts_file)
    else:
        posts = download_posts(SUBREDDIT, after_ts, before_ts)
        save_json(posts, posts_file)

    # COMMENTS
    comments = download_comments(SUBREDDIT, after_ts, before_ts)

    print("\n" + "="*50)
    print("DOWNLOAD COMPLETE")
    print(f"   Posts:    {len(posts):,}")
    print(f"   Comments: {len(comments):,}")
    print("="*50)