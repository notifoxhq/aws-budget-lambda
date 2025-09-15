import os
import logging
import boto3
import requests
import json
from datetime import datetime, timezone

# Initialize the logger
logger = logging.getLogger()
logger.setLevel("INFO")

notifox_audience = os.environ.get('NOTIFOX_AUDIENCE')
notifox_api_key = os.environ.get('NOTIFOX_API_KEY')

def get_monthly_cost():
    # Set up AWS Cost Explorer client
    client = boto3.client('ce')

    # Get first day of this month
    today = datetime.now(timezone.utc)
    start = today.replace(day=1).strftime('%Y-%m-%d')
    end = today.strftime('%Y-%m-%d')

    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start,
            'End': end
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost']
    )

    cost = response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
    return float(cost)

def get_account_id():
    sts = boto3.client('sts')
    identity = sts.get_caller_identity()
    return identity['Account']

def send_alert(message):
    url = "https://api.notifox.com/alert"

    payload = json.dumps({
        "audience": [
            notifox_audience
        ],
        "alert": message
    })

    headers = {
        'x-api-key': notifox_api_key,
        'Content-Type': 'application/json'
    }

    return requests.request("POST", url, headers=headers, data=payload)

def lambda_handler(event, context):
    try:
        
        monthly_cost = get_monthly_cost()

        message = f"Account {get_account_id()}: monthly AWS cost so far: ${monthly_cost:.2f}"

        resp = send_alert(message)
        if resp.status_code != 200:
            logger.error(f"Failed to send alert: {resp.text}")
            raise Exception(f"Failed to send alert: {resp.text}")

        logger.info(f"Sent alert: {resp.text}")

        return {
            "statusCode": 200,
            "message": "Receipt processed successfully"
        }

    except Exception as e:
        logger.error(f"Error processing order: {str(e)}")
        raise
