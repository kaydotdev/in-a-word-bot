# IN A WORD BOT

-------------

<a href="http://t.me/in_a_word_bot"><img src="https://img.shields.io/static/v1?label=&labelColor=505050&message=telegram%20bot&color=%230076D6&style=for-the-badge&logo=google-chrome&logoColor=%230076D6" alt="bot"/></a>

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
export API_TOKEN=...
export MAX_MESSAGE_LENGTH=...
export MAX_FILE_SIZE=...

export REPO_LINK=...
export DEV_LINK=...

export WEBHOOK_HOST=...
export WEBHOOK_PATH=...

export WEBAPP_HOST=...
export WEBAPP_PORT=...
```

Run bot in Python interpreter mode:

```bash
python main.py
```

Optionally, run bot on a `gunicorn` server:

```bash
gunicorn main:app --bind localhost:8080 --worker-class aiohttp.GunicornUVLoopWebWorker
```
