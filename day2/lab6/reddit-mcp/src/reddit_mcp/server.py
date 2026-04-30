"""Minimal Reddit MCP server using public .json endpoints (no auth)."""

from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

USER_AGENT = "reddit-mcp/0.1 (by /u/local-mcp-user)"
BASE = "https://www.reddit.com"
TIMEOUT = 15.0

mcp = FastMCP("reddit-mcp")


async def _get(path: str, params: dict[str, Any] | None = None) -> Any:
    url = f"{BASE}{path}"
    async with httpx.AsyncClient(
        headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT, follow_redirects=True
    ) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return r.json()


def _post_summary(data: dict) -> dict:
    d = data.get("data", data)
    return {
        "id": d.get("id"),
        "title": d.get("title"),
        "author": d.get("author"),
        "subreddit": d.get("subreddit"),
        "score": d.get("score"),
        "num_comments": d.get("num_comments"),
        "created_utc": d.get("created_utc"),
        "permalink": f"{BASE}{d.get('permalink', '')}" if d.get("permalink") else None,
        "url": d.get("url"),
        "selftext": (d.get("selftext") or "")[:500],
    }


def _comment_tree(node: dict, depth: int = 0, max_depth: int = 5) -> dict | None:
    if node.get("kind") != "t1":
        return None
    d = node.get("data", {})
    replies = []
    raw_replies = d.get("replies")
    if isinstance(raw_replies, dict) and depth < max_depth:
        for child in raw_replies.get("data", {}).get("children", []):
            c = _comment_tree(child, depth + 1, max_depth)
            if c:
                replies.append(c)
    return {
        "author": d.get("author"),
        "score": d.get("score"),
        "body": d.get("body"),
        "replies": replies,
    }


@mcp.tool()
async def search_reddit(query: str, limit: int = 10, sort: str = "relevance") -> list[dict]:
    """Search all of Reddit. sort: relevance|hot|top|new|comments."""
    data = await _get("/search.json", {"q": query, "limit": limit, "sort": sort})
    return [_post_summary(c) for c in data.get("data", {}).get("children", [])]


@mcp.tool()
async def search_subreddit(
    subreddit: str, query: str, limit: int = 10, sort: str = "relevance"
) -> list[dict]:
    """Search within a specific subreddit."""
    data = await _get(
        f"/r/{subreddit}/search.json",
        {"q": query, "limit": limit, "sort": sort, "restrict_sr": "1"},
    )
    return [_post_summary(c) for c in data.get("data", {}).get("children", [])]


@mcp.tool()
async def get_subreddit_posts(
    subreddit: str, sort: str = "hot", limit: int = 10
) -> list[dict]:
    """List posts from a subreddit. sort: hot|new|top|rising."""
    data = await _get(f"/r/{subreddit}/{sort}.json", {"limit": limit})
    return [_post_summary(c) for c in data.get("data", {}).get("children", [])]


@mcp.tool()
async def get_post(
    subreddit: str, post_id: str, comment_limit: int = 50, max_depth: int = 5
) -> dict:
    """Get a post's full content plus its comment tree.

    post_id is the base36 id (e.g. '1abcxyz'). subreddit is the name without 'r/'.
    """
    data = await _get(
        f"/r/{subreddit}/comments/{post_id}.json",
        {"limit": comment_limit, "depth": max_depth},
    )
    if not isinstance(data, list) or len(data) < 2:
        return {"error": "unexpected response"}
    post_children = data[0].get("data", {}).get("children", [])
    post = _post_summary(post_children[0]) if post_children else {}
    comments = []
    for c in data[1].get("data", {}).get("children", []):
        node = _comment_tree(c, 0, max_depth)
        if node:
            comments.append(node)
    return {"post": post, "comments": comments}


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
