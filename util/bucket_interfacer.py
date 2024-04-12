from firebase_admin import storage
from google.cloud.storage.bucket import Bucket
from util.context_manager import ContextManager

class Bucket_Interfacer(ContextManager):
    def __init__(self, bucket_name=None, app=None):
        super().__init__()
        self._bucket: Bucket = storage.bucket(bucket_name, app)

    def __exit__(self, exc_type, exc_value, tb):
        del self._bucket
        super().__exit__(exc_type, exc_value, tb)