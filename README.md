# XiaoHongShu Publisher SKILL

Automatically publish article, images or videos to xiaohongshu.com with playwright.

## How to Set Up

1. Install the SKILL via NodeJS
```bash
npx skills add https://github.com/mebusw/xhs-publisher.git
```


2. Install python dependencies
```bash
python3 -m venv ~/.pyenv/versions/xhs-playwright
source ~/.pyenv/versions/xhs-playwright/bin/activate  
# Windows: xhs-playwright\Scripts\activate
# MacOS:   pyenv activate xhs-playwright
pip install playwright requests dashscope dotenv argparse
cp .env.example .env
```

Note, it does NOT use playwright with MCP from Microsoft.
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest"
      ]
    }
  }
}
```

3. fill your phone number to `.env` file. When first time use or login failed, you need to run `/xhs-publisher login`.
4. In Claude Code, execute `/xhs-publisher login_to_publish_image -t 标题 -c 正文内容 -i 图片文件 -s` 或 `/xhs-publisher login_to_publish_video -t 标题 -c 正文内容 -v 视频文件 -s`.
