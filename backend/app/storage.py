import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
POSTS_FILE = DATA_DIR / "posts.json"


def ensure_storage() -> None:
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    if not POSTS_FILE.exists():
        POSTS_FILE.write_text("[]\n", encoding="utf-8")


def read_posts() -> list[dict[str, Any]]:
    ensure_storage()
    return json.loads(POSTS_FILE.read_text(encoding="utf-8"))


def append_post(post: dict[str, Any]) -> dict[str, Any]:
    posts = read_posts()
    posts.insert(0, post)
    POSTS_FILE.write_text(json.dumps(posts, indent=2) + "\n", encoding="utf-8")
    return post
