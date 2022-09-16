import re

from typing import TypeVar
from secrets import token_urlsafe
from urllib.parse import urlencode

from boto3 import Session, client
from fastapi import UploadFile, Form
from pydantic import BaseModel

from src.core import get_settings


Schema = TypeVar("Schema", bound=BaseModel)


class CRUDFile:
    def __init__(
        self,
        service_name: str,
        bucket_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str
    ) -> None:
        self.service_name = service_name
        self.bucket_name = bucket_name
        self.session = Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        
        
    def parse_formdata(self, form_data: Form, schema: Schema) -> Schema:
        if not form_data:
            raise ValueError("from data needed")

        else:
            files: list[UploadFile] = []
            fields: dict[str, str | list[dict[str, str]]] = {}

            for key, value in form_data.items():
                if re.match(r"(files\[[0-9]+\])", key):
                    files.append(value)
                else:
                    fields[key] = value        
            
            uploaded_files: list[dict[str, str]] = (
                self.upload_image(files=files)
            )
            fields.update(uploaded_files)
                       
            insert_data = schema(**fields)

            return insert_data
            

    def upload_image(self, files: list[UploadFile]) -> dict[str, str]:
        image_urls: dict[str, str] = {}
        s3 = self.session.client(self.service_name)
        for file_object in files:
            object_key: str = token_urlsafe(16)
            s3.upload_fileobj(
                Fileobj=file_object.file,
                Bucket=self.bucket_name,
                Key=object_key,
                ExtraArgs={
                    "ContentType": file_object.content_type,
                    "Tagging": urlencode({"name": file_object.filename})
                }
            )

            image_type: str = re.sub(
                pattern=r"(_LEVEL_[0-9]\.png)",
                repl="",
                string=file_object.filename
            )
            image_url = (
                f"https://{self.bucket_name}.s3.amazonaws.com/{object_key}"
            )
            if image_type == "ORDINARY":
                column: str = "ordinary_character_image_url"
            elif image_type == "CHILD_TO_PARENT":
                column: str = "child_to_parent_character_image_url"
            else:
                column: str = "parent_to_child_character_image_url"
            
            image_urls[column] = image_url
                
        return image_urls
    

crud_file = CRUDFile(
    service_name="s3",
    bucket_name="kida-files",
    aws_access_key_id=get_settings().AWS_ACCESS_KEY_ID,
    aws_secret_access_key=get_settings().AWS_SECRET_ACCESS_KEY
)
