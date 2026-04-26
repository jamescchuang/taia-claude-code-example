from __future__ import annotations

from typing import Any

import httpx

BASE = "https://www.reddit.com"
UA = "reddit-mcp/0.1 by u/anonymous"
TIMEOUT = 15.0


class RedditClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            headers={"User-Agent": UA},
            timeout=TIMEOUT,
            follow_redirects=True,
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        url = f"{BASE}{path}"
        r = await self._client.get(url, params=params)
        r.raise_for_status()
        return r.json()

    @staticmethod
    def _post_summary(child: dict) -> dict:
        d = child.get("data", {})
        return {
            "id": d.get("id"),
            "title": d.get("title"),
            "author": d.get("author"),
            "subreddit": d.get("subreddit"),
            "score": d.get("score"),
            "upvote_ratio": d.get("upvote_ratio"),
            "num_comments": d.get("num_comments"),
            "created_utc": d.get("created_utc"),
            "permalink": f"{BASE}{d.get('permalink','')}",
            "url": d.get("url"),
            "is_self": d.get("is_self"),
            "selftext": (d.get("selftext") or "")[:500],
            "flair": d.get("link_flair_text"),
        }

    @staticmethod
    def _listing_posts(listing: dict) -> list[dict]:
        data = listing.get("data", {}) if isinstance(listing, dict) else {}
        return [RedditClient._post_summary(c) for c in data.get("children", []) if c.get("kind") == "t3"]

    @staticmethod
    def _walk_comments(children: list, max_depth: int, depth: int = 0) -> list[dict]:
        out: list[dict] = []
        if depth >= max_depth:
            return out
        for c in children:
            if c.get("kind") != "t1":
                continue
            d = c.get("data", {})
            replies = d.get("replies")
            reply_children: list = []
            if isinstance(replies, dict):
                reply_children = replies.get("data", {}).get("children", [])
            out.append({
                "id": d.get("id"),
                "author": d.get("author"),
                "score": d.get("score"),
                "created_utc": d.get("created_utc"),
                "body": d.get("body"),
                "replies": RedditClient._walk_comments(reply_children, max_depth, depth + 1),
            })
        return out

    async def search(self, query: str, sort: str = "relevance", time: str = "all", limit: int = 25) -> list[dict]:
        data = await self._get(
            "/search.json",
            {"q": query, "sort": sort, "t": time, "limit": limit, "type": "link"},
        )
        return self._listing_posts(data)

    async def search_subreddit(
        self, subreddit: str, query: str, sort: str = "relevance", time: str = "all", limit: int = 25
    ) -> list[dict]:
        data = await self._get(
            f"/r/{subreddit}/search.json",
            {"q": query, "restrict_sr": 1, "sort": sort, "t": time, "limit": limit},
        )
        return self._listing_posts(data)

    async def get_subreddit_posts(
        self, subreddit: str, sort: str = "hot", time: str = "day", limit: int = 25
    ) -> list[dict]:
        sort = sort.lower()
        if sort not in {"hot", "new", "top", "rising", "controversial"}:
            sort = "hot"
        params: dict[str, Any] = {"limit": limit}
        if sort in {"top", "controversial"}:
            params["t"] = time
        data = await self._get(f"/r/{subreddit}/{sort}.json", params)
        return self._listing_posts(data)

    async def get_post(self, post_id: str, comment_limit: int = 20, max_depth: int = 3) -> dict:
        pid = post_id.strip()
        if pid.startswith("http"):
            # extract id from a reddit URL like /comments/<id>/...
            parts = [p for p in pid.split("/") if p]
            try:
                idx = parts.index("comments")
                pid = parts[idx + 1]
            except (ValueError, IndexError):
                raise ValueError(f"cannot parse post id from url: {post_id}")
        data = await self._get(f"/comments/{pid}.json", {"limit": comment_limit, "depth": max_depth})
        post_listing, comment_listing = data[0], data[1]
        posts = self._listing_posts(post_listing)
        if not posts:
            raise ValueError(f"post not found: {pid}")
        post = posts[0]
        # include full selftext for the focused post
        raw = post_listing["data"]["children"][0]["data"]
        post["selftext"] = raw.get("selftext") or ""
        comments = self._walk_comments(comment_listing.get("data", {}).get("children", []), max_depth)
        return {"post": post, "comments": comments}

    async def get_user(self, username: str) -> dict:
        data = await self._get(f"/user/{username}/about.json")
        d = data.get("data", {})
        return {
            "name": d.get("name"),
            "id": d.get("id"),
            "created_utc": d.get("created_utc"),
            "link_karma": d.get("link_karma"),
            "comment_karma": d.get("comment_karma"),
            "total_karma": d.get("total_karma"),
            "is_mod": d.get("is_mod"),
            "is_gold": d.get("is_gold"),
            "verified": d.get("verified"),
            "has_verified_email": d.get("has_verified_email"),
        }

    async def get_user_posts(self, username: str, sort: str = "new", time: str = "all", limit: int = 25) -> list[dict]:
        params: dict[str, Any] = {"sort": sort, "limit": limit}
        if sort == "top":
            params["t"] = time
        data = await self._get(f"/user/{username}/submitted.json", params)
        return self._listing_posts(data)
