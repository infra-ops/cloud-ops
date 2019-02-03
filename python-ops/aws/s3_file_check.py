import boto3
import argparse

def check_object(bucket_name,key_name):
    s3_client = boto3.client('s3')
    res = s3_client.list_objects(
    Bucket=bucket_name,
    Prefix=key_name)
    if 'Contents' in res and  (len(res['Contents'])==1):
        print ("{} {} {} KB".format(res['Contents'][0]['Key'], str(res['Contents'][0]['LastModified']), str(res['Contents'][0]['Size']/1024) ))
    else:
        print("File Missing!!")

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bucket-name', help='Bucket Name', required=True)
    parser.add_argument('-f', '--file-name', help='File Name', required=True)
    args = parser.parse_args()
    print (args)
    check_object(bucket_name=args.bucket_name,key_name=args.file_name)
