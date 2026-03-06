# storages.py
from django_minio_backend.models import MinioBackend

def get_public_storage():
    return MinioBackend(
        bucket_name='microservices-bucket',
        storage_name='default',
    )
