import logging
import boto3
from botocore.exceptions import ClientError


def create_bucket(bucket_name, region="eu-west-2"):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        s3_client = boto3.client('s3', region_name=region)
        location = {'LocationConstraint': region}
        s3_client.create_bucket(Bucket=bucket_name,
                                CreateBucketConfiguration=location)
        print('Bucket Created: ' + bucket_name)
        response_public = s3_client.put_bucket_acl(
            Bucket=bucket_name, ACL='public-read')
        print("pubic", response_public)

        website_configuration = {
            'ErrorDocument': {'Key': 'error.html'},
            'IndexDocument': {'Suffix': 'index.html'},
        }

        response_bucket_website = s3_client.put_bucket_website(
            Bucket=bucket_name, WebsiteConfiguration=website_configuration)

        print("bucket website", response_bucket_website)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_video_to_s3(bucket_name, videoFileName, videoFilePath):
    """Upload a video to S3

    :param bucket_name: Bucket to upload to
    :param object_name: Object name to use when uploading
    :param file_path: Path to the file to upload
    :return: True if file was uploaded, else False
    """

    # Upload the file
    try:
        s3 = boto3.resource('s3')
        s3_client = boto3.client('s3')
        response = s3.Bucket(bucket_name).upload_file(
            videoFilePath + '/' + videoFileName, videoFileName)
        print(response)

        response_object_acl = s3_client.put_object_acl(
            ACL='public-read', Bucket=bucket_name, Key=videoFileName)

        print("object acl", response_object_acl)

    except ClientError as e:
        logging.error(e)
        return False
    return True


def empty_and_delete_bucket(bucket):
    """Empty and delete an S3 bucket

    :param bucket: Bucket to empty and delete
    :return: True if bucket was emptied and deleted, else False
    """

    # Delete all objects in the bucket
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket)
        for obj in bucket.objects.all():
            obj.delete()
        bucket.delete()
    except ClientError as e:
        logging.error(e)
        return False
    return True


bucket_name = 'sagar-youtube-bucket'
create_bucket(bucket_name)
upload_video_to_s3(bucket_name, 'final_clip.mp4', './output')
empty_and_delete_bucket(bucket_name)
