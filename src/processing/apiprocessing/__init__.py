import json
import base64
import logging

import azure.functions as func


def main(msg: func.QueueMessage) -> None:
    response = base64.b64decode(msg.get_body()).decode('ascii')
    response_payload = json.loads(response)
    text_to_process = response_payload.get('text', '')

    logging.info(f"Received message: {response_payload.get('text', None)}")
