

## Social Media Scraping (R169, 2026-04-20)

Tool: tools/social_scraper.py

```python
from social_scraper import scrape_social_media, save_scraped_data

data = scrape_social_media("weibo", "keyword", max_posts=10)
save_scraped_data(data, "output.json")
```

Functions:
- scrape_social_media(platform, keyword, max_posts): Scrape data
- extract_post_data(post_element): Extract post data
- save_scraped_data(data, output_path): Save to JSON

Platforms: weibo, zhihu, xiaohongshu
Data: title, content, likes, comments, author, timestamp

[skill_mapping]
category: web_automation
skill: social_scraper
tools: social_scraper.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('web_automation_sop.md')
```
