import boto
import json
# Create an SNS client
sns = boto3.client('sns')

# Publish a simple message to the specified SNS topic
response = sns.publish(
    TopicArn='arn:aws:sns:us-east-1:758637906269:notify-me:1e1955f1-ff4b-4784-82ca-19c31e152740',    
    Message='Hello World!',    
)

# Print out the response
print(response)
