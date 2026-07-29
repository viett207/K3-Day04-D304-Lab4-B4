from __future__ import annotations

from typing import Any

from tools._shared import TIMEOUT, err, _twitter_get, _tweets_from


def search_tweets(query: str = "", search_type: str = "Latest", limit: int = 5) -> dict[str, Any]:
    try:
        data = _twitter_get("/search.php", {"query": query, "search_type": search_type})
        return {"tool": "search_tweets", "query": query, "search_type": search_type, "items": _tweets_from(data, limit)}
    except Exception as exc:
        return err("search_tweets", exc)


