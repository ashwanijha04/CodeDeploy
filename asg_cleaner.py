# Lambda Code to Automatically delete the autoscaling group on deployment failure

import boto3
cd_client = boto3.client('codedeploy')
asg_client = boto3.client('autoscaling')


def lambda_handler(event, context):
    application =  event['detail']['application']
    deploymentId = event['detail']['deploymentId']
    deploymentGroup = event['detail']['deploymentGroup']

    print(f"Starting cleanup for failed deployment {deploymentId} (Application = {application} | Deployment Group = {deploymentGroup})")
    asg = 'CodeDeploy_' + deploymentGroup + '_' + deploymentId
    print('AutoScaling Group: ', asg)

    deployment = cd_client.get_deployment(deploymentId=deploymentId)
    deployment_type = deployment['deploymentInfo']['deploymentStyle']['deploymentType']

    print('Deployment Type:', deployment_type)

    if(deployment_type == 'BLUE_GREEN'):
        try:
            print(f"Attempting to remove Auto Scaling Group '{asg}'")
            response = asg_client.delete_auto_scaling_group(AutoScalingGroupName=asg,ForceDelete = True)
            print('Auto Scaling Group ', asg, 'removed successfully')
        except Exception as e:
            print('Could not delete the ASG.')
            print('Reason:', e)
        finally:
            print('Process Complete.')
    else:
        print('The deployment is not a blue green deployment. Taking no action.')
