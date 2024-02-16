from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import os
import pandas as pd
from io import BytesIO

account_url = os.environ['STORAGE_ACCOUNT_URL']
default_credential = DefaultAzureCredential()

def extract_relevant_vessel_data(is_unified_data: bool, vessel_imo: int) -> pd.DataFrame:
    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    container_client = blob_service_client.get_container_client("mlp")

    if is_unified_data:
        blob_client = container_client.get_blob_client(f"unification/{vessel_imo}.parquet")
    else:
        blob_client = container_client.get_blob_client(f"customer_data/period_reports/{vessel_imo}.parquet")

    streamdownloader = blob_client.download_blob()
    stream = BytesIO()
    streamdownloader.readinto(stream)

    return pd.read_parquet(stream)