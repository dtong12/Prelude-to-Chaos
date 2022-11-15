import boto3
from botocore.exceptions import ClientError
import os

def send_email(email_contents):
    SENDER = "davis.tong2021@gmail.com" # must be verified in AWS SES Email
    RECIPIENT = "davis.tong1@gmail.com" # must be verified in AWS SES Email
    AWS_REGION = "us-east-1"
    SUBJECT = "Glitch Alarm"

    string_output = ''

    for dictionary in email_contents:
        for key in dictionary:
            string_output += f"{key}: {dictionary[key]}<br>"   
        string_output += "<br>"
    BODY_TEXT = string_output
    
    #Formatting
    BODY_HTML = f"""<html>
    <head></head>
    <body>
    <p>{BODY_TEXT}</p>
    </body>
    </html>
                """ 

    client = boto3.client('ses')
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [RECIPIENT],
            },
            Message={
                'Body': {
                    'Html': {'Data': BODY_HTML},
                    'Text': {'Data': BODY_TEXT},
                },
                'Subject': {'Data': SUBJECT},
            },
            Source=SENDER
        )
    except ClientError as e: print(e.response['Error']['Message'])
    else: print("Email sent! Message ID:", response['MessageId']),


def testing_email():
    print()
    contents = [
        ({"sportsbook": 'fanduel', "game name":'ruud vs fritz',  "line_name":'set 1 game 2 winner', "glitch type":'glitch in game', "game_matching": f"-   Point -> Sofa: 5 dk: 3" }), 
        ({"sportsbook": 'draftkings', "game name":'nadal vs djkovic', "line_name":'set 2 winner', "glitch type":'glitch in set', "set_matching": f"-   Point -> Sofa: 2 dk: 1" })
    ]
    send_email(contents)

    

if __name__ == '__main__':
    testing_email()
