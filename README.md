# IN A WORD BOT

[![Telegram bot link](https://img.shields.io/static/v1?label=&labelColor=505050&message=telegram%20bot&color=%2329b6f6&style=for-the-badge&logo=telegram&logoColor=%2329b6f6)](https://t.me/in_a_word_bot)

## Techstack

![GCP](./docs/gcp.svg)
![Python](./docs/python.svg)
![Jupyter](./docs/jupyter.svg)
![Pytorch](./docs/pytorch.svg)
![ONNX](./docs/onnx.svg)
![Redis](./docs/redis.svg)

## Description

Finding the right information in the **digital era** may be the real challenge nowadays because it's growing **exponentially** day by day! Whether you are a student preparing an essay or a researcher working with the knowledge base, you spend a lot of time searching, filtering, and summarizing text. [Google](https://www.google.com/) can assist you with the first two steps, but I will help with the last one! Send me a plain text, file, or link to an external resource, and I will summarize it for you in a word :grin:.

## Getting started

### Run bot locally

First, change the directory from the `root` to the `src`:

```bash
cd src
```

If you have a virtual environment, activate it:

```bash
source venv/bin/activate
```

Set environment variables:

```bash
export ENV_API_TOKEN=...
export ENV_MAX_MESSAGE_LENGTH=...
export ENV_MAX_FILE_SIZE=...

export ENV_REPO_LINK=...
export ENV_DEV_LINK=...

export ENV_WEBHOOK_MODE=...

# Optional if ENV_WEBHOOK_MODE is False
export ENV_WEBHOOK_HOST=...
export ENV_WEBHOOK_PATH=...

export ENV_WEBAPP_HOST=...
export ENV_WEBAPP_PORT=...
```

Run bot in Python interpreter mode:

```bash
python main.py
```

Optionally, run bot on a `gunicorn` server (webhook mode ONLY):

```bash
gunicorn main:app --bind localhost:8080 --worker-class aiohttp.GunicornUVLoopWebWorker
```
