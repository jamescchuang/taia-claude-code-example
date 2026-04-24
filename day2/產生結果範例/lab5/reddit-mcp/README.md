# reddit-mcp

Zero-auth Reddit MCP server. Uses Reddit's public `.json` endpoints — no API key, no OAuth.

## Tools

| Tool | Purpose |
|---|---|
| `search` | Search across all of Reddit |
| `search_subreddit` | Search within a specific subreddit |
| `get_subreddit_posts` | List posts by hot / new / top / rising |
| `get_post` | Fetch a post + comment tree |
| `get_user` | Fetch a user profile |
| `get_user_posts` | List a user's submissions |

## Install & run

```bash
cd day2/lab5/reddit-mcp
uv sync
uv run reddit-mcp
```

## Wire into Claude Code

At project root `day2/lab5/.mcp.json`:

```json
{
  "mcpServers": {
    "reddit": {
      "command": "uv",
      "args": ["--directory", "reddit-mcp", "run", "reddit-mcp"]
    }
  }
}
```

Restart Claude Code in `day2/lab5/` and the `reddit` server will appear.

## Notes

- Reddit rate-limits unauthenticated requests. If you hit 429s, slow down or add an OAuth layer.
- `sort` for search: `relevance | hot | top | new | comments`. `time`: `hour | day | week | month | year | all`.
