# Lambda
## Create Function
1. Author From Scratch
2. name of the functio -Hello World
3. Run time Pyhton3.8
4. by default - it make permission with cloud watch
5. Create function



# API-Gateway
## Create API
1. Rest API - Build
2. AP Name - any name (new api)
3. description (optional)
4. Endpoint type Regional

## Create Action 
1. Create Method
2. Get
3. Click on tick

## / -GET-Setup
1. Integration Type (select as per requirement, for now its lambda)
2. Use lambda Proxy Integration
3. Lambda Region
4. Lambda Funtion Name
5. Use Default timeput -cheked

## To Deploy this API
1. Action --> deploy API
2. Deployment stage --> New Stage
3. Stage prod
4. deploy

https://zi48i4hprk.execute-api.ap-south-1.amazonaws.com/test

## Install curl into your machine
Ref - Download from https://curl.se/windows/
1. extract the file
2. mv to c folder
3. rename it to curl
4. add path of bin folder in system variable
5. open cmd
6. curl -X GET "api url"
```
curl -X GET "https://zi48i4hprk.execute-api.ap-south-1.amazonaws.com/test"



lambda
Create Function
Name- Hello-World-2
Run Time python 3.8
Permisiion
Use existing role from previous lambda function


Function
```
import json
def lambda_handler(event,context):
    myString=event[myString]
    return{
        'statusCode': 200,
        'body": json:dumps(myString)
    }

APi Gateway
 select previous api
 select /
 select action --> Create Resource
 resource name - my resource
 create resource
 Create method
 Get
 click right
 Integration type lambda
 lambda funtion hello-workd-2
 use default til=me checked

 Intergartion Request
 expand mapping templates
 Request body passthrough - When there are no templates defined
 adding mapping templates
  application/json
    checked checkmark icon
  
  generate Template
  {
    "myString": "$input.params('myString')"
  }

  Action 
  Deploy APi
  prod
  depoly

*************************************
Trigger Lambda from API
********************************
Create API
Rest AP Build
New API
anem
description
endpoint pytpe regional
Action 
Create Methof
GET
Check mark icon
Integration type MOck
Save

Get Method Execution pane
Method Request
URL Query String Parameter
Name check mark icon

Integration Request
MApping Template
When There no template define
content type
application/json
template
```
{
    #if( $input.params('myString') == "myValue" )
        "statusCode": 200
    #else
        "statusCode": 500
    #end
}
```
save

Integration Response
mapping Template Secrion
application/json
template
```
{
    "statusCode": 200'
    "message": "Hello from Edureka!"
}
```
save

Method Response
add response
500
click on check mark


Intergation Resonse
add respone

Http satus regex 5\d{2}
Methios response status 500
COntent handling Passthrough

save

expoand 500 option
expoand Mapping Templates
Content type 
application/json
```
{
    "statusCode": 500,
    "message": "This is an error message."
}
```
save

test the mocking
client test click
Query String myString=myValue
test
