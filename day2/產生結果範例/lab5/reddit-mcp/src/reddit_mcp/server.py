from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from .reddit import RedditClient

mcp = FastMCP("reddit-mcp")
_client: RedditClient | None = None


def _get_client() -> RedditClient:
    global _client
    if _client is None:
        _client = RedditClient()
    return _client


@mcp.tool()
async def search(query: str, sort: str = "relevance", time: str = "all", limit: int = 25) -> list[dict[str, Any]]:
    """Search across all of Reddit.

    sort: relevance | hot | top | new | comments
    time: hour | day | week | month | year | all
    """
    return await _get_client().search(query=query, sort=sort, time=time, limit=limit)


@mcp.tool()
async def search_subreddit(
    subreddit: str, query: str, sort: str = "relevance", time: str = "all", limit: int = 25
) -> list[dict[str, Any]]:
    """Search within a specific subreddit."""
    return await _get_client().search_subreddit(
        subreddit=subreddit, query=query, sort=sort, time=time, limit=limit
    )


@mcp.tool()
async def get_subreddit_posts(
    subreddit: str, sort: str = "hot", time: str = "day", limit: int = 25
) -> list[dict[str, Any]]:
    """List posts from a subreddit.

    sort: hot | new | top | rising | controversial (time applies to top/controversial)
    time: hour | day | week | month | year | all
    """
    return await _get_client().get_subreddit_posts(
        subreddit=subreddit, sort=sort, time=time, limit=limit
    )


@mcp.tool()
async def get_post(post_id: str, comment_limit: int = 20, max_depth: int = 3) -> dict[str, Any]:
    """Fetch a post with its comment tree. Accepts a post id or a full reddit URL."""
    return await _get_client().get_post(post_id=post_id, comment_limit=comment_limit, max_depth=max_depth)


@mcp.tool()
async def get_user(username: str) -> dict[str, Any]:
    """Fetch a Reddit user's public profile."""
    return await _get_client().get_user(username=username)


@mcp.tool()
async def get_user_posts(
    username: str, sort: str = "new", time: str = "all", limit: int = 25
) -> list[dict[str, Any]]:
    """List posts submitted by a user. sort: new | hot | top | controversial."""
    return await _get_client().get_user_posts(username=username, sort=sort, time=time, limit=limit)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
