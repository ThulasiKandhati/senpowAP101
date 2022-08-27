import os
import boto3
from dotenv import load_dotenv
load_dotenv()
import random
import string

client = boto3.client('cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME'),aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
         aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'))
def send_plain_email(subj, bod):
    ses_client = boto3.client("ses", region_name=os.getenv('COGNITO_REGION_NAME'),aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
         aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'))
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

def sign_up(username, c_msg, check0, check1, check2, check3, check4):
    ret_msg = ''
    ret_val = ['N','N','N']
    r_debug =""
    c_msg = " " if not c_msg else c_msg
    try:
        pwd = ''
        if not check0:
            pass1 = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=4)) 
            password = username+'@'+pass1
            r_debug = "Start user sigup~"
            response = client.sign_up(
                ClientId=os.getenv('COGNITO_USER_CLIENT_ID'),
                Username=username,
                Password=password,
                UserAttributes=[{'Name': 'email','Value': 'kthulasikumar@gmail.com'}]
            )
            
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                r_debug += "Signedup user~"
                ret_val[0] = 'Y'
                ret_msg = 'User created.'
                
            print(response)
        if not check1:
            r_debug += "Confrim sign up"
            response = client.admin_confirm_sign_up(
                         UserPoolId=os.getenv('COGNITO_USERPOOL_NAME'),
                         Username=username)
            print(response)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                r_debug += "Confirmed signup~"
                ret_val[1] = 'Y'
                ret_msg += ' User Confrimed.'
        if not check2:
            r_debug += "email verify~"
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
                r_debug += "Email confiemd~"

        if c_msg.find("AP101_USER add") == -1 and check3:
            response = client.admin_add_user_to_group(
                     UserPoolId=os.getenv('COGNITO_USERPOOL_NAME'),
                     Username=username,
                     GroupName='AP101_USER'
               )
            print(response)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                ret_msg += ' AP101_USER added.'

        if c_msg.find("AP101_ADMIN add") == -1 and check4:
            response = client.admin_add_user_to_group(
                     UserPoolId=os.getenv('COGNITO_USERPOOL_NAME'),
                     Username=username,
                     GroupName='AP101_ADMIN'
               )
            print(response)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                ret_msg += ' AP101_ADMIN added.'
        r_debug += "All CHecks Done~"
        send_plain_email("Senthur Power App user Created",f"User Name: {username} and password: {password}") 
        return ret_val, ret_msg, r_debug
    except Exception as e:
        print(str(e)[:150])
        ret_msg += str(e)[:150]
        r_debug += f"Error {e}"
    finally:
      return ret_val, ret_msg, r_debug

def sign_in(username, password):
    try:
        response = client.initiate_auth(
        ClientId = os.getenv('COGNITO_USER_CLIENT_ID'),
        AuthFlow ='USER_PASSWORD_AUTH',
        AuthParameters={
           'USERNAME': username,
           'PASSWORD': password
        })
        return response
    except Exception as e:
        return 'ERR_INVALID_AUTH' + str(e)[:75]


def forgot_password(username):
    try:
        response = client.forgot_password(
           ClientId=os.getenv('COGNITO_USER_CLIENT_ID'),
           Username=username
        )
        return response
    except Exception as e:
        return 'ERR_INVALID_FORGPASS' + str(e)[:75]



def confirm_forgot_password(username, confirm_code):
    try:
        pass1 = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=4))
        password = username+'@'+pass1
        response = client.confirm_forgot_password(
               ClientId= os.getenv('COGNITO_USER_CLIENT_ID'),
               Username=username,
               ConfirmationCode=confirm_code,
               Password=password
        )
        send_plain_email("Senthur Power App user Created",f"User Name: {username} and password: {password}")
        return response
    except Exception as e:
        return 'ERR_INVALID_CNFFORGPASS' + str(e)[:75]

