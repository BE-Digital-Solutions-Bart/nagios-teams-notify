#!/usr/bin/env python3

import requests
import json
import sys

def send_teams_notification(webhook_url, title, message):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.0",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": title,
                            "weight": "bolder",
                            "size": "medium"
                        },
                        {
                            "type": "TextBlock",
                            "text": message,
                            "wrap": True
                        }
                    ]
                }
            }
        ]
    }
    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        print(f"Failed to send notification: {response.status_code}, {response.text}")
    else:
        print("Notification sent successfully")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: notify_teams.py <webhook_url> <title> <message>")
        sys.exit(1)

    webhook_url = sys.argv[1]
    title = sys.argv[2]
    message = sys.argv[3]

    send_teams_notification(webhook_url, title, message)