## Create IAM roles to use with the CloudWatch agent on Amazon EC2 instances
## Ref: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/create-iam-roles-for-cloudwatch-agent.html#create-iam-roles-for-cloudwatch-agent-roles

## Installing the CloudWatch agent
## Ref: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/install-CloudWatch-Agent-on-EC2-Instance.html

## Create the CloudWatch agent configuration file
## Ref: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/create-cloudwatch-agent-configuration-file.html
***************
## Create IAM policy cloudwatch full access and attach to EC2
## install cloudwatch logs agent
```
sudo yum install -y awslogs
```
## edit /ect/awslogs/awslogs.conf
## edit /ect/awslogs/awscli.conf
## Start the awslog service
```
systemctl start awslogsd
systemctl enable awslogs.service
```
