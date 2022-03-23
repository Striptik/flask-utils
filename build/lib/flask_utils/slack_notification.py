import json

import requests

import config

from .logger import log_error, log_exception


def send_slack(channel, template_id, params={}):
    try:
        response = requests.post(
            "{}/api/notifications".format(config.MS_NOTIFICATION_HOST),
            json={
                "contact": channel,
                "notification_type": "slack",
                "template_id": template_id,
                "params": params,
            },
            headers={"content_type": "application/json"},
        )
        if response.status_code < 300:
            return True
        response_json = json.loads(response.content.decode("utf-8"))
        log_error(
            "Failed to send notification",
            {
                "response": response_json,
                "data": {
                    "contact": channel,
                    "notification_type": "slack",
                    "template_id": template_id,
                    "params": params,
                },
            },
        )
        return False
    except Exception as e:
        log_exception(
            e, {"email": channel, "template_id": template_id, "params": params}
        )
        return False


def send_error_to_slack(channel=None, template=None, title=None, datas=None):
    if (channel is None) or (template is None) or (title is None):
        log_error(
            "Error params",
            dict(channel=channel, template=template, title=title, datas=datas),
        )
        return None
    message = {
        "message": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": title, "emoji": True},
            }
        ]
    }
    if datas is not None:
        for key, value in datas.items():
            message.get("message").append(
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": str(key) + " : " + str(value)},
                }
            )
    send_slack(channel, int(template), message)
