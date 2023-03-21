import boto3
import json
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ssm_client = boto3.client("ssm")

LIFECYCLE_KEY = "LifecycleHookName"
ASG_KEY = "AutoScalingGroupName"
EC2_KEY = "EC2InstanceId"
DOCUMENT_NAME = "ASGLogBackup"
RESPONSE_DOCUMENT_KEY = "DocumentIdentifiers"

def check_response(response_json):
    try:
        if response_json['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            return False
    except KeyError:
        return False

def list_document():
    document_filter_parameters = {'key': 'Name', 'value': DOCUMENT_NAME}
    response = ssm_client.list_documents(
        DocumentFilterList=[ document_filter_parameters ]
    )
    return response

def check_document():
    # If the document already exists, it will not create it.
    try:
        response = list_document()
        if check_response(response):
            logger.info("Documents list: %s", response)
            if response[RESPONSE_DOCUMENT_KEY]:
                logger.info("Documents exists: %s", response)
                return True
            else:
                return False
        else:
            logger.error("Documents' list error: %s", response)
            return False
    except Exception, e:
        logger.error("Document error: %s", str(e))
        return None   

def send_command(instance_id):
    # Until the document is not ready, waits in accordance to a backoff mechanism.
    while True:
        timewait = 1
        response = list_document()
        if any(response[RESPONSE_DOCUMENT_KEY]):
            break
        time.sleep(timewait)
        timewait += timewait
    try:
        response = ssm_client.send_command(
            InstanceIds = [ instance_id ], 
            DocumentName = DOCUMENT_NAME, 
            TimeoutSeconds = 120
            )
        if check_response(response):
            logger.info("Command sent: %s", response)       
            return response['Command']['CommandId']
        else:
            logger.error("Command could not be sent: %s", response)
            return None
    except Exception, e:
        logger.error("Command could not be sent: %s", str(e))
        return None