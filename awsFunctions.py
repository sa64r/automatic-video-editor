import logging
import boto3
from botocore.exceptions import ClientError


def create_s3_bucket(bucket_name, region="eu-west-2"):
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

        website_configuration = {
            'ErrorDocument': {'Key': 'error.html'},
            'IndexDocument': {'Suffix': 'index.html'},
        }

        response_bucket_website = s3_client.put_bucket_website(
            Bucket=bucket_name, WebsiteConfiguration=website_configuration)
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
    print("uploading", videoFileName, "to", bucket_name, '.....')
    try:
        s3 = boto3.resource('s3')
        s3_client = boto3.client('s3')
        response = s3.Bucket(bucket_name).upload_file(
            videoFilePath + '/' + videoFileName, videoFileName)
        print('Uploaded to Bucket: ' + bucket_name)

        response_object_acl = s3_client.put_object_acl(
            ACL='public-read', Bucket=bucket_name, Key=videoFileName)

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


def get_video_url(bucket_name, video_name):
    """Get the video URL from S3

    :return: Video URL
    """

    # Get the video URL
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        for obj in bucket.objects.all():
            if obj.key == video_name:
                location = boto3.client('s3').get_bucket_location(
                    Bucket=bucket_name)['LocationConstraint']
                return "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket_name, obj.key)

    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_image_to_s3(bucket_name, imageFileName):
    """Upload an image to S3

    :param bucket_name: Bucket to upload to
    :param object_name: Object name to use when uploading
    :param file_path: Path to the file to upload
    :return: True if file was uploaded, else False
    """

    # Upload the file
    print("uploading", imageFileName, "to", bucket_name, '.....')
    try:
        s3 = boto3.resource('s3')
        s3_client = boto3.client('s3')
        response = s3.Bucket(bucket_name).upload_file(
            imageFileName, imageFileName)
        print('Uploaded to Bucket: ' + bucket_name)

        response_object_acl = s3_client.put_object_acl(
            ACL='public-read', Bucket=bucket_name, Key=imageFileName)

    except ClientError as e:
        logging.error(e)
        return False
    return True

# upload and detect faces in image using rekognition


def detect_faces(bucket_name, image_name):
    """Detect faces in an image

    :param bucket_name: Bucket name
    :param image_name: Image name
    :return: True if faces detected, else False
    """

    # Detect faces in the image
    try:
        rekognition = boto3.client('rekognition')
        response = rekognition.detect_faces(
            Image={'S3Object': {'Bucket': bucket_name, 'Name': image_name}},
            Attributes=['ALL'])
        print('Detected faces in ' + image_name)
        return response
    except ClientError as e:
        logging.error(e)
        return False
    return True
