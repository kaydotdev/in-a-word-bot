import json
import base64
import logging

import azure.functions as func

from .extractive import extractive_summary
from .settings import THRESHOLD_MULTIPLYER


def main(msg: func.QueueMessage) -> None:
    response = base64.b64decode(msg.get_body()).decode('ascii')
    response_payload = json.loads(response)
    text_to_process = response_payload.get('text', '')
    summary = extractive_summary(text_to_process, THRESHOLD_MULTIPLYER)

    logging.info(f"Summary: {summary}")
