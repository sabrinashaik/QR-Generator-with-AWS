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
    if http_method == 'GET':
        email=''
        email = event['queryStringParameters']['email']
        
        
        with conn.cursor() as cur:
            qry = "select * from password where username ='"+email+"';"
            cur.execute(qry)
            conn.commit()
            cur.close()
            res_items=cur.fetchall()
            statusCode = 200
        
    elif http_method == 'POST':
        body = event.get('body')
        username = ''
        app = ''
        passwd = ''
        if body is not None:
            username = json.loads(body).get('username', username)
            app = json.loads(body).get('app', app)
            passwd = json.loads(body).get('passwd', passwd)
        
        with conn.cursor() as cur:
            query = "INSERT INTO passwordmanager.password (username, app, passwd) VALUES(%s, %s, %s);"
            data = (username,app,passwd)
            try:
                cur.execute(query,data)
                conn.commit()
                cur.close()
                statusCode = 200
                res_items = {'msg': 'Request processed'}
                logger.info("password added")
            except Exception as e:
                logger.info(e)
                statusCode = 400
                res_items = {'msg': 'Request processed'}
    
    elif http_method == 'DELETE':
        id=''
        id = event['queryStringParameters']['id']
        
        with conn.cursor() as cur:
            qry = "delete from password where id ="+id+";"
            cur.execute(qry)
            conn.commit()
            cur.close()
            statusCode = 200 
            res_items = {'msg': 'Request processed'}
    else:
        statusCode = 400
        res_items = {'msg': 'httpMethod not supported for request'}
        
    return {
        'statusCode': statusCode,
        'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                    'Access-Control-Allow-Credentials': 'true',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps(res_items)
            }     
  
        
     

