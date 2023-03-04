import json
import pymysql
import rds_config
import sys
import uuid
from datetime import datetime

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
    if http_method == 'GET':
        email=''
        email = event['queryStringParameters']['email']
        
        with conn.cursor() as cur:
            qry = "UPDATE foods.foodlist SET verified = 1 WHERE email = '"+email+"';"
            cur.execute(qry)
            conn.commit()
            cur.close()
            statusCode = 200
            res_item = {'msg' : 'Updated successfully'}
            
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
  
        
     

