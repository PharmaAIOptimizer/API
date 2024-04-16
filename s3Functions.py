import boto3
import re
import base64

def upload_file(file_name, bucket, object_name=None):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified, file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except Exception as e:
        print(e)
        return False
    return True

def delete_file(bucket, object_name):
    """
    Delete a file from an S3 bucket

    :param bucket: Bucket of the file
    :param object_name: S3 object name
    :return: True if file was deleted, else False
    """
    s3_client = boto3.client('s3')
    try:
        s3_client.delete_object(Bucket=bucket, Key=object_name)
    except Exception as e:
        print(e)
        return False
    return True

def download_file(bucket, object_name, file_name=None):
    """
    Download a file from an S3 bucket

    :param bucket: Bucket to download from
    :param object_name: S3 object name
    :param file_name: File name to download the object to. 
                      If not specified, object_name is used.
    :return: True if file was downloaded, else False
    """
    # If file_name was not specified, use object_name
    if file_name is None:
        file_name = object_name

    # Download the file
    s3_client = boto3.client('s3')
    try:
        s3_client.download_file(bucket, object_name, file_name)
    except Exception as e:
        print(e)
        return False
    return True

def find_object_with_highest_number(bucket_name):
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    
    max_number = -1
    object_with_max_number = None
    
    if 'Contents' in response:
        for obj in response['Contents']:
            object_name = obj['Key']
            # Assuming the number is at the end and is preceded by a non-numeric character
            # For example: 'file-123', 'image_456.png'
            match = re.search(r'(\d+)(?!.*\d)', object_name)
            if match:
                number = int(match.group())
                if number > max_number:
                    max_number = number
                    object_with_max_number = object_name
    
    return object_with_max_number

def decode_file(base64_string):
    # Decode the base64 string and save the snapshot
    with open('snapshot.csv', 'wb') as file:
        file.write(base64.b64decode(base64_string))

def upload_snapshot(file_name):
    # Get the latest snapshot number
    object_name = find_object_with_highest_number('dailysupplysnapshot')

    # Increment the number
    if object_name:
        match = re.search(r'(\d+)(?!.*\d)', object_name)
        if match:
            number = int(match.group())
            number += 1
            object_name = object_name.replace(str(match.group()), str(number))
    else:
        object_name = 'snapshot_1'

    # Upload the file
    if upload_file(file_name, 'dailysupplysnapshot', object_name):
        print(f"Uploaded {file_name} as {object_name}")
    else:
        print("Upload failed")



# Replace 'my_bucket' with your S3 bucket name
# Replace 'my_file.txt' with the path to your file
# Replace 'my_object_name' with the desired object name in S3 (optional)

# if upload_file('Analysis/Daily Snapshot.csv', 'dailysupplysnapshot', 'snapshot_1'):
#     print("Upload successful")
# else:
#     print("Upload failed")

# if download_file('dailysupplysnapshot', 'snapshot_1', 'snapshot.csv'):
#     print("Download successful")
# else:
#     print("Download failed")

# To delete the file you just uploaded
# if delete_file('my_bucket', 'my_object_name'):
#     print("Deletion successful")
# else:
#     print("Deletion failed")

# highest_number_object = find_object_with_highest_number('dailysupplysnapshot')
# if highest_number_object:
#     print(f"The object with the highest number: {highest_number_object}")
# else:
#     print("No objects found or no numeric endings detected.")

# decode_file('SXRlbSBOdW1iZXIg4oCTIDYgZGlnaXQsTkRDIE51bWJlcixVUEMgTnVtYmVyLENvbnN0YW50LEN1c3RvbWVyLVNwZWNpZmljIEl0ZW0gTnVtYmVyLERlc2NyaXB0aW9uLFBhY2sgU2l6ZSBEaXZpc29yLFNpemUgUXR5LFJYL09UQyBJbmRpY2F0b3IsQVdQIFByaWNlLEFjcXVpc2l0aW9uIFByaWNlLFJldGFpbCBQcmljZSxDb250cmFjdCBGbGFnLEdlbmVyaWMgRGVzY3JpcHRpb24sUmV0YWlsIFBhY2sgUXVhbnRpdHksV0FDIFByaWNlLEl0ZW0gTnVtYmVyIOKAkyA4IGRpZ2l0CjAwMTEzOTAsNDExNjc0MzEwMDIsMDQxMTY3NDMxMDIzLCAgICAgICAgICAgICAgICAgICAgICAgICwgICAgICAgICAgLEFMTEVHUkEgRCAxMkhSIDYwTUcgQ0FQTEVUIDEwQywwMDAwMDAxMDAwMCwxMCAgICAgICxPLDAwMDAwMDE4NjYsMDAwMDAwMTE3MywwMDAwMDAxNzYwLE4sZmV4b2ZlbmFkaW5lL3BzZXVkb2VwaGVkcmluZSBPLDAwMDAxLDAwMDAwMDEwNjYsMTAwODQ5MTYKMDAxMTM5NSw0MTE2NzQzMTAwNCwwNDExNjc0MzEwNDcsICAgICAgICAgICAgICAgICAgICAgICAgLCAgICAgICAgICAsQUxMRUdSQSBEIDEySFIgNjBNRyBDQVBMRVQgMjBDLDAwMDAwMDIwMDAwLDIwICAgICAgLE8sMDAwMDAwMjc2MiwwMDAwMDAxNzM2LDAwMDAwMDI2MDQsTixmZXhvZmVuYWRpbmUvcHNldWRvZXBoZWRyaW5lIE8sMDAwMDEsMDAwMDAwMTU3OCwxMDA4NDkxNwowMDExNDIxLDQxMTY3NDMyMDA1LDA0MTE2NzQzMjA1MSwgICAgICAgICAgICAgICAgICAgICAgICAsICAgICAgICAgICxBTExFR1JBIEQgMjRIUiAxODBNRyBUQUJMRVQgMTAsMDAwMDAwMTAwMDAsMTAgICAgICAsTywwMDAwMDAyMTE2LDAwMDAwMDEzMzAsMDAwMDAwMTk5NSxOLGZleG9mZW5hZGluZS9wc2V1ZG9lcGhlZHJpbmUgTywwMDAwMSwwMDAwMDAxMjA5LDEwMDg0OTE5')
