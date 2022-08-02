import os
import boto3
from dotenv import load_dotenv
load_dotenv()

username = 'cliuser8'
password = 'Cliuser@1'

client = boto3.client('cognito-idp', region_name='ap-south-1')

def sign_up(uname, pwd):
    response = client.sign_up(
        ClientId=os.getenv('COGNITO_USER_CLIENT_ID'),
        Username=username,
        Password=password,
        UserAttributes=[{'Name': 'email','Value': 'kthulasikumar@gmail.com'},{'Name': 'email_verified','Value': 'true'}]
    )

    print(response)

    response = client.admin_confirm_sign_up(
                UserPoolId=os.getenv('COGNITO_USERPOOL_NAME'),
                Username=username)
    print(response)

