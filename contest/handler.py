import os
import requests
import json
import datetime
import boto3
import os
import uuid
import pdfrw


def handler(event, context):
    print("Hello from LocalStack Lambda container image!")

    # 0. do a really basic input check
    if "@" not in event["email"]:
        raise ValueError(f"Not a valid email {event['email']}")

    # 1. generate certificate pdf
    generate_certificate(event["email"])

    # 2. connect to s3 on localstack
    s3_client = boto3.client(
        "s3",
        endpoint_url=f"http://{os.environ.get('LOCALSTACK_HOSTNAME')}:{os.environ.get('EDGE_PORT')}",
    )

    # 3. make sure the bucket exists
    s3_client.create_bucket(Bucket="localstack-demo")

    # 3. copy the generated file to s3
    s3_client.upload_file("/tmp/certificate.pdf", "localstack-demo", "certificate.pdf")

    # record the participation event
    record_participant(event, context)


def generate_certificate(value: str):
    """Generates the highly official certificate of participation!"""
    pdf = pdfrw.PdfReader("./cert_template.pdf")
    pdf.pages[0].Annots[2].update(pdfrw.PdfDict(V=value))
    pdf.pages[0].Annots[2].update(pdfrw.PdfDict(Ff=1))
    pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject("true")))
    pdfrw.PdfWriter().write("/tmp/certificate.pdf", pdf)


def record_participant(event, context):
    payload = {
        "email": event["email"],
        "invoked_function_arn": context.invoked_function_arn,
    }

    data = json.dumps(
        {
            "timestamp": datetime.datetime.now().isoformat(),
            "session_id": str(uuid.uuid4()),
            "action": "executed_lambda",
            "version": "1",
            "payload": json.dumps(payload),
        }
    )

    r = requests.post(
        "https://api.tinybird.co/v0/events",
        params={
            "name": "analytics_events",
            "token": "p.eyJ1IjogIjAwZDRjYzRjLTg4N2UtNGNmZS05YzY4LTJjNzMyNjE5ODdjMCIsICJpZCI6ICI2YzRhMDViNi1iZjVlLTRkY2QtODNlZS1jMmFjYjg5ZjQ1NzAifQ.EPdBzyAb28wUbtZacobblsMi42IwTd7d2amppDfw-jE",
        },
        data=data,
    )
