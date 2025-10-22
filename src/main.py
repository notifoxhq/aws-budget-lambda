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
    
    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': start,
                'End': end
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost']
        )
        logger.info("Successfully retrieved cost data from Cost Explorer")
        
        cost = response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
        cost_float = float(cost)
        logger.info(f"Monthly cost retrieved: ${cost_float:.2f}")
        return cost_float
        
    except Exception as e:
        logger.error(f"Error fetching cost data: {str(e)}")
        raise

def get_account_id():
    logger.info("Fetching AWS account ID")
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        account_id = identity['Account']
        logger.info(f"Retrieved account ID: {account_id}")
        return account_id
    except Exception as e:
        logger.error(f"Error fetching account ID: {str(e)}")
        raise

def send_alert(message):
    logger.info("Preparing to send Notifox alert")
    logger.info(f"Alert message: {message}")
    
    url = "https://api.notifox.com/alert"

    payload = json.dumps({
        "audience": [
            notifox_audience
        ],
        "alert": message
    })

    headers = {
        'Authorization': f'Bearer {notifox_api_key}',
        'Content-Type': 'application/json'
    }

    try:
        logger.info(f"Sending POST request to Notifox API: {url}")
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info(f"Notifox API response status: {response.status_code}")
        logger.info(f"Notifox API response body: {response.text}")
        return response
    except Exception as e:
        logger.error(f"Error sending alert to Notifox: {str(e)}")
        raise

def lambda_handler(event, context):
    logger.info("Lambda function started")
    logger.info(f"Event received: {json.dumps(event) if event else 'None'}")
    
    try:
        # Check environment variables
        logger.info(f"Environment variables - NOTIFOX_AUDIENCE: {'Set' if notifox_audience else 'Not set'}")
        logger.info(f"Environment variables - NOTIFOX_API_KEY: {'Set' if notifox_api_key else 'Not set'}")
        
        monthly_cost = get_monthly_cost()
        account_id = get_account_id()

        message = f"Account {account_id}: monthly AWS cost so far: ${monthly_cost:.2f}"
        logger.info(f"Constructed alert message: {message}")

        logger.info("Sending alert via Notifox")
        resp = send_alert(message)
        
        if resp.status_code != 200:
            logger.error(f"Failed to send alert: {resp.text}")
            raise Exception(f"Failed to send alert: {resp.text}")

        logger.info(f"Successfully sent alert: {resp.text}")
        logger.info("Lambda function completed successfully")

        return {
            "statusCode": 200,
            "message": "Alert sent successfully",
            "cost": monthly_cost,
            "account_id": account_id,
            "event_source": event_source,
            "event_detail_type": event_detail_type,
            "schedule_name": schedule_name,
            "timezone": timezone
        }

    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        logger.error(f"Exception type: {type(e).__name__}")
        raise
