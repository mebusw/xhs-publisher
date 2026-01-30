
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
4. Execute `/xhs-publisher 标题 正文内容 图片` in Claude Code.
