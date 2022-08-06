import os
import boto3
from dotenv import load_dotenv
load_dotenv()


def sign_up(uname, pwd):
    try:
        ret_val = ['E','E','E','']
        response = client.sign_up(
            ClientId='2kn21825ivmts1vdd0cshf6h2g',
            Username=username,
            Password=password,
            UserAttributes=[{'Name': 'email','Value': 'kthulasikumar@gmail.com'}]
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            ret_val[0] = 'Y'
        print(response)

        response = client.admin_confirm_sign_up(
                     UserPoolId='ap-south-1_3fjfOpUAM',
                     Username=username)
        print(response)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            ret_val[1] = 'Y'
        response = client.admin_update_user_attributes(
           UserPoolId='ap-south-1_3fjfOpUAM',
           Username=username,
           UserAttributes=[
             {
                'Name': 'email_verified',
                'Value': 'true'
             },
           ]
        )
        print(response)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            ret_val[2] = 'Y'

    except Exception as e:
        print(str(e)[:150])
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            ret_val[3] = str(e)[:150]
    finally:
      return ret_val
