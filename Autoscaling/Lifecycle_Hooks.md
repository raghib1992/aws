Lifecycle Hooks
REF https://github.com/aws-samples/aws-lambda-lifecycle-hooks-function


Step 1 – Create an SNS topic to receive the result of the backup
```
aws sns create-topic --name backupoutcome
aws sns subscribe --topic-arn arn:aws:sns:ap-south-1:561243041928:backupoutcome --protocol email --notification-endpoint sankalaninfotech@gmail.com
```

## Step 2 – Create an IAM role for your instances and your Lambda function
### IAM ROle for instance to enable them to run the SSM agent, upload your files to s3 bucket, and complete the lifecycle hooks and publish to the SNS topic
### Create Policy ASGBackupPolicy 
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "autoscaling:CompleteLifecycleAction",
        "sns:Publish"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
```
### Create Role for Ec2
#### attach policy AmazonEC2RoleforSSM and ASGBackupPolicy


### Create role for Lambda
#### Attach policies AmazonSSMFullAccess, ASGBackupPolicy, and AWSLambdaBasicExecutionRole

### Create Launch Template
#### with ec2 role and user data
```
    #!/bin/bash
    sudo yum install amazon-ssm-agent -y
    sudo /sbin/start amazon-ssm-agent
```

### Create AUtoscaling Group


### Create Lifecycle hooks
```
aws autoscaling put-lifecycle-hook --lifecycle-hook-name ASGBackup --auto-scaling-group-name ASGBackup --lifecycle-transition autoscaling:EC2_INSTANCE_TERMINATING --heartbeat-timeout 3600
```

## Step 4 – Create an S3 bucket for files
```
aws s3api create-bucket --bucket raghib_balti
```

## Step 5 – Create the SSM document
1. Log into the EC2 console.

2. Go to System Manager Shared Resources.

3. Choose Documents, Create document.

4. For Document name, enter “ASGLogBackup”.

5. For Content, add the above JSON, modified for your environment.

6. Choose Create document.

```
{
  "schemaVersion": "1.2",
  "description": "Backup logs to S3",
  "parameters": {},
  "runtimeConfig": {
    "aws:runShellScript": {
      "properties": [
        {
          "id": "0.aws:runShellScript",
          "runCommand": [
            "",
            "ASGNAME='ASGBackup'",
            "LIFECYCLEHOOKNAME='ASGBackup'",
            "BACKUPDIRECTORY='/var/log'",
            "S3BUCKET='raghib-balti'",
            "INSTANCEID=$(curl http://169.254.169.254/latest/meta-data/instance-id)",
            "REGION=$(curl http://169.254.169.254/latest/meta-data/placement/availability-zone)",
            "REGION=${REGION::-1}",
            "SNSTARGET='arn:aws:sns:'${REGION}':561243041928:backupoutcome'",                       
            "HOOKRESULT='CONTINUE'",
            "MESSAGE=''",
            "",
            "tar -cf /tmp/${INSTANCEID}.tar $BACKUPDIRECTORY &> /tmp/backup",
            "if [ $? -ne 0 ]",
            "then",
            "   MESSAGE=$(cat /tmp/backup)",
            "else",
            "   aws s3 cp /tmp/${INSTANCEID}.tar s3://${S3BUCKET}/${INSTANCEID}/ &> /tmp/backup",
            "       MESSAGE=$(cat /tmp/backup)",
            "fi",
            "",
            "aws sns publish --subject 'ASG Backup' --message \"$MESSAGE\"  --target-arn ${SNSTARGET} --region ${REGION}",
            "aws autoscaling complete-lifecycle-action --lifecycle-hook-name ${LIFECYCLEHOOKNAME} --auto-scaling-group-name ${ASGNAME} --lifecycle-action-result ${HOOKRESULT} --instance-id ${INSTANCEID}  --region ${REGION}"
          ]
        }
      ]
    }
  }
}
```

## Step 6 – Create the Lambda function
Log in to the Lambda console.

Choose Create Lambda function.

For Select blueprint, choose Skip, Next.

For Name, type “lambda_backup” and for Runtime, choose Python 2.7.

For Lambda function code, paste the Lambda function from the lambda_backup.py.

Choose Choose an existing role.

For Role, choose lambda-role (previously created).

In Advanced settings, configure Timeout for 5 minutes.

Choose Next, Create function.


## Step 7 – Configure CloudWatch Events to trigger the Lambda function
Log in to the CloudWatch console.

Choose Events, Create rule.

For Select event source, choose Auto Scaling.

For Specific instance event(s), choose EC2 Instance-terminate Lifecycle Action and for Specific group name(s), choose ASGBackup.

For Targets, choose Lambda function and for Function, select the Lambda function that you previously created, “lambda_backup”.

Choose Configure details.

In Rule definition, type a name and choose Create rule.