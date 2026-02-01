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

## Publish an article with images
```bash
source ~/.pyenv/versions/xhs-playwright/bin/activate  
python3 scripts/auto-publish-with-playwright.py login_to_publish_image \
  -t "标题" \
  -c "正文内容" \
  -i img1.jpg img2.jpg \
  -s
```

## Publish an article with video
```bash
source ~/.pyenv/versions/xhs-playwright/bin/activate  
python3 scripts/auto-publish-with-playwright.py login_to_publish_video \
  -t "标题" \
  -c "正文内容" \
  -v <视频文件> \
  -s
```
