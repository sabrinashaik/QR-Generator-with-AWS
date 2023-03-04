import json
import pymysql
import rds_config
import sys
import time
x = int(time.time())

rds_host = rds_config.db_endpoint
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
port = 3306
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_host,user=name,
                           passwd=password,db=db_name,
                           connect_timeout=5,
                           cursorclass=pymysql.cursors.DictCursor)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()






def lambda_handler(event, context):
    http_method = event.get('httpMethod')
    
        
    if http_method == 'POST':
        body = event.get('body')
        email=''
        password = ''
        if body is not None:
            email = json.loads(body).get('email', email)
            password = json.loads(body).get('password', password)
        
        with conn.cursor() as cur:
            qry = "select * from userlist where email ='"+email+"';"
            cur.execute(qry)
            data = cur.fetchall()
            conn.commit()
            if len(data) != 0:
                response = data[0]
                logger.info(response['verified'])
                if password == response['password']:
                    if response['verified'] == 1:
                        statusCode = 200
                        res_item={'msg' : 'Auth Success'}
                    else:
                        statusCode = 203 
                        res_item={'msg' : 'Email Validation pending'}
                else:
                    statusCode = 403
                    res_item={'msg' : 'Auth Fail'}
            else:
                statusCode = 404
                res_item={'msg' : 'User not found'}
                
            
           
            
            
            return {
                    'statusCode': statusCode,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                        'Access-Control-Allow-Credentials': 'true',
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps(res_item)
                }
        
    else:
        response = {
                "isBase64Encoded": False,
                "statusCode": 405,
                "body": json.dumps('httpMethod: '+http_method+ ' not supported for request'),  
                "headers": {
                    'Content-Type' : 'application/json',
                    'Access-Control-Allow-Origin' : '*',
                    'Allow' : 'PATCH',
                    'Access-Control-Allow-Methods' : 'PATCH',
                    'Access-Control-Allow-Headers' : '*'
                    }
                }        
    return response      
  
        
     

