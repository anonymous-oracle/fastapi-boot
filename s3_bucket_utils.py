from boto3 import client, resource
from config import S3_ACCESS_KEY_ID, S3_BUCKET_NAME, S3_SECRET_ACCESS_KEY, S3_FOLDER_ACTIVE, S3_FOLDER_DELETED
import asyncio

class BucketS3ToS3():
    def __init__(self, access_key_id, secret_access_key, bucket_name):
        self.__s3 = resource('s3', aws_access_key_id=access_key_id,
                             aws_secret_access_key=secret_access_key)
        self.__bucket_name = bucket_name

    def copy_file(self, src_path, dst_path):
        copy_source = {
            'Bucket': self.__bucket_name,
            'Key': src_path
        }
        try:
            bucket = self.__s3.Bucket(self.__bucket_name)
            bucket.copy(copy_source, dst_path)
            return True
        except Exception as e:
            print(e)
            return False

    def delete_file(self, del_path):
        try:
            self.__s3.Object(self.__bucket_name, del_path).delete()
            return True
        except Exception as e:
            print(e)
            return False

    def move_file(self, src_path, dst_path):
        try:
            self.copy_file(src_path, dst_path)
            self.delete_file(src_path)
            return True
        except Exception as e:
            print(e)
            return False


class BucketS3():

    def __init__(self, access_key_id, secret_access_key, bucket_name):
        self.__s3 = client('s3', aws_access_key_id=access_key_id,
                           aws_secret_access_key=secret_access_key)
        self.__bucket_name = bucket_name

    async def upload_file(self, src_path, dst_path):
        try:
            self.__s3.upload_file(src_path, self.__bucket_name, dst_path)
            return True
        except Exception as e:
            print(e)
            return False

    async def download_file(self, src_path, dst_path):
        try:
            self.__s3.download_file(self.__bucket_name, src_path,  dst_path)
            return True
        except Exception as e:
            print(e)
            return False


bucket_upl_dwl = BucketS3(
    S3_ACCESS_KEY_ID, S3_SECRET_ACCESS_KEY, S3_BUCKET_NAME)
bucket_copy = BucketS3ToS3(
    S3_ACCESS_KEY_ID, S3_SECRET_ACCESS_KEY, S3_BUCKET_NAME)

if __name__ == '__main__':
    # bucket.upload_file('temp/temp.txt', 'temp2/temp2.txt')
    # bucket.download_file('temp/temp.txt', 'temp/temp.txt')
    bucket_copy.copy_file(f"{S3_FOLDER_ACTIVE}/35c7dbcb-7b6a-494f-9194-5288edea684a.wav",
                          f"{S3_FOLDER_DELETED}/35c7dbcb-7b6a-494f-9194-5288edea684a.wav")
    pass
