import os
import boto3
from dotenv import load_dotenv
load_dotenv()
import random
import string

client = boto3.client('cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME'))
def send_plain_email(subj, bod):
    ses_client = boto3.client("ses", region_name="ap-south-1")
    CHARSET = "UTF-8"

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "kthulasikumar@gmail.com",
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": bod,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": subj,
            },
        },
        Source="kthulasikumar@gmail.com",
    )


def reset_pass(usernam):
    pass1 = ''.join(random.choices(string.ascii_lowercase +
                    string.digits, k=4))
    password = username+pass1
    response = client.admin_set_user_password(
    UserPoolId=os.getenv('COGNITO_USERPOOL_NAME'),
    Username=usernam,
    Password=pas,
    Permanent=True
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        send_plain_email("Senthur Power App Password Reset",f"User Name: {username} and password: {password}")

def sign_up(uname, c_msg, check0, check1, check2, check3, check4):
    ret_msg = ''
    ret_val = ['N','N','N']
    try:
        pwd = ''
        if not check0:
            pass1 = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=4)) 
            password = username+pass1
            response = client.sign_up(
                ClientId=os.getenv('COGNITO_USER_CLIENT_ID'),
                Username=username,
                Password=password,
                UserAttributes=[{'Name': 'email','Value': 'kthulasikumar@gmail.com'}]
            )
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                ret_val[0] = 'Y'
                ret_msg = 'User created.'
                
            print(response)
        if not check1:
            response = client.admin_confirm_sign_up(
                         UserPoolId=os.getenv('COGNITO_USERPOOL_NAME'),
                         Username=username)
                print(response)
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    ret_val[1] = 'Y'
                    ret_msg += ' User Confrimed.'
        if not check2:
            response = client.admin_update_user_attributes(
                 UserPoolId=os.getenv('COGNITO_USERPOOL_NAME'),
                 Username=username,
                 UserAttributes=[
                  {
                   'Name': 'email_verified',
                   'Value': 'true'
                  },]
              )
            print(response)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                ret_val[2] = 'Y'
                ret_msg += ' Email Confrimed.'

        if c_msg.find("AP101_USER add") == -1 and check3:
            response = client.admin_add_user_to_group(
                     UserPoolId=os.getenv('COGNITO_USERPOOL_NAME'),
                     Username=username,
                     GroupName='AP101_USER'
               )
            print(response)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                ret_msg += ' AP101_USER added.'

        if c_msg.find("AP101_ADMIN add") == -1 and check3:
            response = client.admin_add_user_to_group(
                     UserPoolId=os.getenv('COGNITO_USERPOOL_NAME'),
                     Username=username,
                     GroupName='AP101_ADMIN'
               )
            print(response)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                ret_msg += ' AP101_ADMIN added.'
    send_plain_email("Senthur Power App user Created",f"User Name: {username} and password: {password}") 
    return ret_val, ret_msg
    except Exception as e:
        print(str(e)[:150])
        ret_msg += str(e)[:150]
    finally:
      return ret_val, ret_msg
