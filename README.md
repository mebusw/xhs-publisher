
## How to Set Up

```bash
python3 -m venv ~/.pyenv/versions/xhs-playwright
source ~/.pyenv/versions/xhs-playwright/bin/activate  
# Windows: xhs-playwright\Scripts\activate
# MacOS:   pyenv activate xhs-playwright
pip install playwright requests dashscope dotenv argparse
cp .env.example .env
```

Note, We don't install playwright with MCP from Microsoft
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