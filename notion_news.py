import os
import feedparser
from notion_client import Client
from datetime import datetime

# =====================
# Configuration
# =====================
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["DATABASE_ID"]
RSS_URL = os.getenv("RSS_URL", "http://export.arxiv.org/rss/astro-ph.CO")
K = int(os.getenv("K", 5))
SOURCE = os.getenv("SOURCE", "arXiv astro-ph.CO")

notion = Client(auth=NOTION_TOKEN)

# =====================
# Functions
# =====================
def test_database_connection():
    """Check if we can access the Notion database and print YES or NO."""
    try:
        db = notion.databases.retrieve(database_id=DATABASE_ID)
        print("✅ YES - Connected to database:", db["id"])
        response = notion.databases.query(database_id=DATABASE_ID, page_size=1)
        count = len(response.get("results", []))
        print(f"📊 Database currently has {count}+ pages")
        return True
    except Exception as e:
        print("❌ NO - Cannot connect to database:", e)
        import traceback
        traceback.print_exc()
        return False

def fetch_existing_titles():
    """Fetch existing titles from the Notion database."""
    titles = set()
    has_more = True
    start_cursor = None
    
    try:
        while has_more:
            query_params = {
                "database_id": DATABASE_ID,
                "page_size": 100
            }
            if start_cursor:
                query_params["start_cursor"] = start_cursor
            
            response = notion.databases.query(**query_params)
            results = response.get("results", [])
            
            for r in results:
                title_prop = r["properties"].get("Title", {}).get("title", [])
                if title_prop:
                    titles.add(title_prop[0]["text"]["content"])
            
            has_more = response.get("has_more", False)
            start_cursor = response.get("next_cursor")
            
        print(f"📋 Found {len(titles)} existing titles in database")
            
    except Exception as e:
        print(f"❌ Error querying database: {e}")
        import traceback
        traceback.print_exc()
    
    return titles

def add_entry(entry):
    """Add a new article to the Notion database."""
    try:
        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "Title": {"title": [{"text": {"content": entry.title}}]},
                "URL": {"url": entry.link},
                "Date": {"date": {"start": datetime(*entry.published_parsed[:6]).isoformat()}},
                "Source": {"select": {"name": SOURCE}},
            },
        )
        print(f"  ✅ Added: {entry.title[:80]}...")
        return True
    except Exception as e:
        print(f"  ❌ Failed to add entry: {e}")
        return False

def trim_database():
    """Archive oldest entries if more than K."""
    try:
        response = notion.databases.query(
            database_id=DATABASE_ID,
            sorts=[{"property": "Date", "direction": "ascending"}],
            page_size=100
        )
    except Exception as e:
        print(f"❌ Error querying database for trim: {e}")
        return
    
    pages = response.get("results", [])
    to_archive = len(pages) - K
    
    if to_archive > 0:
        print(f"🧹 Archiving {to_archive} old entries...")
        for i in range(to_archive):
            try:
                page = pages[i]
                title_prop = page["properties"].get("Title", {}).get("title", [])
                title = title_prop[0]["text"]["content"] if title_prop else "Unknown"
                
                notion.pages.update(page_id=page["id"], archived=True)
                print(f"  📦 Archived: {title[:60]}...")
            except Exception as e:
                print(f"  ❌ Failed to archive page: {e}")
    else:
        print(f"✅ Database has {len(pages)} entries (max: {K}), no archiving needed")

def main():
    print("=" * 60)
    print(f"🚀 Starting Notion News Sync (K={K})")
    print("=" * 60)
    
    connected = test_database_connection()
    if not connected:
        print("❌ Stopping execution")
        return
    
    print(f"\n📰 Fetching RSS feed: {RSS_URL}")
    feed = feedparser.parse(RSS_URL)
    
    if not feed.entries:
        print("⚠️  No entries found")
        return
    
    print(f"✅ Found {len(feed.entries)} entries")
    
    print("\n📋 Fetching existing titles...")
    existing = fetch_existing_titles()
    
    print(f"\n✨ Processing top {K} entries...")
    new_count = 0
    for i, entry in enumerate(feed.entries[:K], 1):
        if entry.title not in existing:
            print(f"[{i}/{K}] New entry:")
            if add_entry(entry):
                new_count += 1
        else:
            print(f"[{i}/{K}] Already exists: {entry.title[:60]}...")
    
    if new_count > 0:
        print(f"\n🎉 Added {new_count} new entries!")
    else:
        print(f"\n✅ No new entries")
    
    print("\n🧹 Trimming database...")
    trim_database()
    
    print("\n✅ Done!")

if __name__ == "__main__":
    main()
