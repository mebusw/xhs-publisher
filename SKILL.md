---
name: xhs-publisher
description: automatically publish article, images or videos to xiaohongshu.com with playwright
---


## Usage

1. Activate virtual env with `pyenv activate xhs-playwright`
2. run `scripts/auto-publish-with-playwright.py` giving article title, content, images and/or videos



## Usage Examples

### Re-login to Xiaohongshu
```bash
source ~/.pyenv/versions/xhs-playwright/bin/activate  
python3 scripts/auto-publish-with-playwright.py login 
```

## Publish an article
```bash
source ~/.pyenv/versions/xhs-playwright/bin/activate  
python3 scripts/auto-publish-with-playwright.py login_to_publish \
  --title "标题" \
  --content "正文内容" \
  --images img1.jpg img2.jpg \
  --slow-mode
```
