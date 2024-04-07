import json
import boto3
import json
from io import BytesIO
from PIL import Image, ImageOps
import os


s3 = boto3.client("s3")
size = int(os.environ.get("THUMBNAIL_SIZE"))
def thumbnail_generator(event, context):
    bucket,key,img_size = get_object_details(event)
    details = f"Bucket: {bucket}\nKey: {key}\nImage_Size: {img_size}"
    print(details)
    
    if (not key.endswith("_thumbnail.png")):    
        image = get_s3_object(bucket,key)
        
        thumbnail = image_to_thumbnail(image)
        thumbnail_key = generate_filename(key)

        thumbnail_url = upload_to_s3(bucket,thumbnail_key,thumbnail,img_size)
        print(thumbnail_url)
        
        return thumbnail_url

def upload_to_s3(bucket,key,image,img_size):
    out_thumbnail = BytesIO()

    image.save(out_thumbnail,'PNG')
    out_thumbnail.seek(0)

    response = s3.put_object(
        Body=out_thumbnail,
        Bucket=bucket,
        ContentType='image/png',
        Key=key
    )
    print(response)

    try:
        # Generate a presigned URL for the S3 object
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=3600
        )
        return url
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None
    
def generate_filename(key):
    key_split = key.rsplit('.', 1)
    return key_split[0] + "_thumbnail.png"

def image_to_thumbnail(image):
    return ImageOps.fit(image, (size, size), Image.LANCZOS)

def get_object_details(event):
    if event:
        print("EVENT:::", event)
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        img_size = event['Records'][0]['s3']['object']['size']
        
        return bucket, key, img_size
    
    return "bucket","key","img_size"

def get_s3_object(bucket,key):
    response = s3.get_object(Bucket=bucket,Key=key)
    
    print("BodyType: ",type(response['Body'])) # StreamingBody
    imageData = response['Body'].read()
    print("ImageData: ",type(imageData)) # Bytes


    file = BytesIO(imageData)
    img = Image.open(file)

    return img