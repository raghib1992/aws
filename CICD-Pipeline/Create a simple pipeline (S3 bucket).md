Ref https://docs.aws.amazon.com/codepipeline/latest/userguide/tutorials-simple-s3.html


1. Create an S3 bucket for your application, enable Versionng
- Bucket Name: cicd-source-code-bucket
- Upload SampleApp_Linux.zip file into s3

2. Create Amazon EC2 Windows instances and install the CodeDeploy agent

3. Create an Amazon EC2 Linux instance and install the CodeDeploy agent
- Choose Create role
    - Under Select type of trusted entity, select AWS service. Under Choose a use case, select EC2. Under Select your use case, choose EC2. Choose Next: Permissions.
    - Policy: AmazonSSMManagedInstanceCore, AmazonEC2RoleforAWSCodeDeploy
- Create EC2 Instance
    - Tag env: dev
    - attach role


4. Create an application in CodeDeploy
- Choose Create role
    - Under Select trusted entity, choose AWS service. Under Use case, choose CodeDeploy. Choose CodeDeploy from the options listed. Choose Next. The AWSCodeDeployRole managed policy is already attached to the role
- create an application in CodeDeploy
    - Application name, enter MyDemoApplication
    - Compute Platform, choose EC2/On-premises
- create a deployment group in CodeDeploy
    - Deployment group name, enter MyDemoDeploymentGroup
    - Service role, choose the service role you created earlier.
    - Deployment type, choose In-place.
    - Environment configuration, choose Amazon EC2 Instances. with Tags mention in ec2
    - Agent configuration with AWS Systems Manager, choose Now and schedule updates
    - Deployment settings, choose CodeDeployDefault.OneAtaTime

5. Create your first pipeline in CodePipeline
- Pipelines page, choose Create pipeline
    -  Pipeline name, enter MyFirstPipeline
    - Service role, do one of the following:
        * Choose New service role to allow CodePipeline to create a new service role in IAM.
        * Choose Existing service role to use a service role already created in IAM. In Role name, choose your service role from the list.
    - Add source stage, in Source provider, choose Amazon S3
    - allows CodePipeline to use Amazon CloudWatch Events
    - Add build stage, choose Skip build stage
    - Add deploy stage, in Deploy provider, choose CodeDeploy


6. Add another stage in the pipeline to deploy from staging servers to production servers using CodeDeploy
- To create a second deployment group in CodeDeploy
    - choose same Application
    - Create deployment group 
- Add the deployment group as another stage in your pipeline
    - Create a third stage
    - choose the name of the pipeline
    - choose Edit
    - choose + Add stage to add a stage immediately after the Deploy stage
    - Stage name, enter Production. Choose Add stage.
    - In the new stage, choose + Add action group
    - Action name, enter Deploy-Second-Deployment. In Action provider, under Deploy, choose CodeDeploy.
    - choose - Application, Prod Deployment grp, Inout atifact source

7. Disable and enable transitions between stages in CodePipeline
- To disable and enable transitions between stages in a CodePipeline pipeline
    - Open the CodePipeline console
    - hoose the Disable transition button between the second stage (Deploy) and the third stage
Step 7: Clean up resources