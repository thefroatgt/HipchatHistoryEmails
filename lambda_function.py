from __future__ import print_function

from urllib2 import urlopen
import datetime
import json
import boto3

#secrets
HIPCHATTOKEN = ''
ROOMS = [
    ['Room Name One','123'],
    ['Room Name Two','456']
    ]
AWSKEY = ''
AWSSECRET = ''
EMAIL = 'someone@example.com'

def lambda_handler(event, context):
    
    date = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")
    print('Getting Hipchat Logs for ' + date)

    try:
        for room in ROOMS:
            print('Getting Room' + room[0] + ' ' + room[1])
            body = get_hipchat_logs(date,room[1])
            send_email(room[0] + ' messages on ' + date, body)
            
    except:
        print('Get failed!')
        raise

def get_hipchat_logs(date, room):
    url = 'https://api.hipchat.com/v1/rooms/history'
    url += '?room_id=' + room
    url += '&date=' + date
    url += '&format=json'
    url += '&auth_token=' + HIPCHATTOKEN
    url += '&timezone=EST'
    
    response = urlopen(url)
    html = response.read()
    
    parsed_json = json.loads(html)
    
    if len(parsed_json['messages']) == 0:
        return ''
    
    body = '<table>'
    
    for message in parsed_json['messages']:
        body += '<tr><td>' + message['date'][11:16] + '</td><td nowrap="nowrap">' + message['from']['name'] + ":</td><td>" + message['message'] + '</td></tr>'
        
    body += '</table>'
    
    print(body)
    
    return body

def send_email(subject, body):
    if body == '':
        return
    
    session = boto3.Session(
        aws_access_key_id=AWSKEY,
        aws_secret_access_key=AWSSECRET,
        region_name='us-east-1')

    ses = session.client('ses')

    response = ses.send_email(
        Source = EMAIL,
        Destination={
            'ToAddresses': [
                EMAIL
            ]
        },
        Message={
            'Subject': {
                'Data': subject
            },
            'Body': {
                'Html': {
                    'Data': body
                }
            }
        }
    )
    



  
  

  
  
