---
name: reddit-claudecode-popular
description: 列出本週 r/claudecode 留言數最多的 5 篇文章。當使用者詢問 r/claudecode 近期熱門討論、最多留言的文章、本週熱門貼文，或 Claude Code subreddit 上的熱門話題時，使用此 skill。觸發詞包括「本週熱門」「最多留言」「r/claudecode 熱門」「popular this week」「top posts in claudecode」等。
---

# reddit-claudecode-popular

抓取 r/claudecode 本週留言數最多的前 5 篇文章，並以表格呈現。

## 執行步驟

1. 呼叫 `mcp__reddit__reddit_get_subreddit_posts`，參數：
   - `subreddit`: `claudecode`
   - `category`: `top`
   - `time_filter`: `week`
   - `limit`: `25`

2. 依 `num_comments` 由高到低排序，取前 5 筆。

3. 輸出 markdown 表格：

| 排名 | 文章標題 | 作者 | 留言數 | 讚數 |
|------|---------|------|--------|------|

欄位格式：
- **排名**：`#1` ~ `#5`
- **文章標題**：`[title](https://www.reddit.com{permalink})` 超連結
- **作者**：`u/{author}`
- **留言數**：`num_comments` 原始值
- **讚數**：`score` 加千分位逗號（例如 `1,885`）

只輸出表格，不要加其他說明文字。
