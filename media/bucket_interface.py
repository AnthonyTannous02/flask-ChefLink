from datetime import datetime
from util.bucket_interfacer import Bucket_Interfacer
from google.cloud.exceptions import NotFound, GoogleCloudError
from google.cloud.storage.blob import Blob

class BucketInterface(Bucket_Interfacer):
    def __init__(self, bucket_name=None, app=None):
        super().__init__(bucket_name=bucket_name, app=app)

    def upload_image(self, file, destination_path: str) -> bool:
        blob = self.__gen_blob(destination_path)
        try:
            blob.upload_from_file(file, content_type="image/png")
        except GoogleCloudError as e:
            print(str(e))
            return False
        return True

    def remove_image(self, image_path: str) -> bool:
        blob = self.__gen_blob(image_path)
        try:
            blob.delete()
        except NotFound as e:
            print(str(e))
            return False
        return True

    def gen_url(self, image_path: str, expiration: datetime = datetime.today()) -> str:
        blob = self.__gen_blob(image_path)
        if blob.exists():
            return blob.generate_signed_url(expiration=expiration, method="GET")
        else:
            return "."

    def __gen_blob(self, path) -> Blob:
        return self._bucket.blob(path)