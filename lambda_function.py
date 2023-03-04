##lambda_function
import logging
import provision
import login
import verifyemail
import passwordmanager

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# initializing size of string 
def lambda_handler(event, context):
    logger.info('Received message: %s', event)
    http_method = event.get('httpMethod')
    
    print(event)
    path = (event.get('path').split("/")[1]) 
    print(path)
   
    if http_method == 'OPTION':
        response = {
            statusCode: 200,
            headers: {
                        'Content-Type' : 'application/json',
                        'Access-Control-Allow-Origin' : '*',
                        'Allow' : 'GET, OPTIONS, POST,DELETE',
                        'Access-Control-Allow-Methods' : 'GET, OPTIONS, POST,DELETE',
                        'Access-Control-Allow-Headers' : '*'
                }
                }
    else:
        if path == "provision":
            response = provision.lambda_handler(event, context)
        elif path == "login":
            response = login.lambda_handler(event, context)
        elif path == "passwordmanager":
            response = passwordmanager.lambda_handler(event, context)
        elif path == "verifyemail":
            response = verifyemail.lambda_handler(event, context)    
    logger.info("Response: %s", response)
    return response