# IN A WORD BOT

-------------

<a href="http://t.me/in_a_word_bot"><img src="https://img.shields.io/static/v1?label=&labelColor=505050&message=telegram%20bot&color=%230076D6&style=for-the-badge&logo=google-chrome&logoColor=%230076D6" alt="bot"/></a>
<a><img src="https://img.shields.io/github/workflow/status/antonAce/in-a-word-bot/Build%20and%20deploy%20Python%20app?style=for-the-badge" alt="deploy-pipeline"/></a>

## Description

Finding the right information in the **digital era** may be the real challenge nowadays because it's growing **exponentially** day by day! Whether you are a student preparing an essay or a researcher working with the knowledge base, you spend a lot of time searching, filtering, and summarizing text. [Google](https://www.google.com/) can assist you with the first two steps, but I will help with the last one! Send me a plain text, file, or link to an external resource, and I will summarize it for you in a word :grin:.

## Run on local machine

Before running application set the following environment variables:
- **ENV_API_TOKEN**: Telegram bot token (from @BotFather);
- **ENV_TOKENIZER_CONFIGS**: *Transformer* model tokenizer configuration relative file path (named `byte-level-bpe.json` by default);
- **ENV_TRANSFORMER_WEIGHTS_CONFIGS**: *Transformer* model weights relative file path (file format should be`H5`);
- **ENV_WEBHOOK_ENABLED**: boolean value, if value is `True` bot starts in *webhook mode* (otherwise in *polling mode*) and requires to set dependent variables:
    - **ENV_WEBHOOK_HOST**: HTTPS domain name of the web app;
    - **ENV_WEBHOOK_PORT**: Port to expose for the webhook (Telegram API supports only 443, 80, 88 and 8443 ports);
    - **ENV_WEBHOOK_PATH**: Route of the webhook;
    - **ENV_WEBAPP_HOST**: Address of the application on the local machine (`0.0.0.0` by default);
    - **ENV_WEBAPP_PORT**: Port of the application on the local machine;

Start application in interpreter mode:

```shell
python bot.py
```

Start application as [Gunicorn](https://github.com/benoitc/gunicorn) worker (for webhook mode):

```shell
gunicorn bot:bot_factory --bind 0.0.0.0:80 --worker-class aiohttp.GunicornWebWorker
```
