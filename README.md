# CHATCLI

## steps
1. download rename this file to chat.py
2. create virtualenv: python3 -m venv openai
3. source openai/bin/activate
4. pip install openai
5. get api key: https://platform.openai.com/account/api-keys and config api token ~/.config/openai.json

```
{"token":"openai-token"}
```
6. python chat.py
7. if you dont want every time source virtual env, replace header `#!/usr/bin/env python3` with openai env python absolute path `#!/home/xxx/openai/bin/python`
