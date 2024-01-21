import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive",
]
creds = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=SCOPES
)


def upload_file_to_drive(file_name, file_path, mimetype, folder_id):
    """MimeTypes
    audio: audio/wav
    images: image/jpeg"""
    try:
        service = build("drive", "v3", credentials=creds)

        file_metadata = {
            "name": file_name,
            "parents": [folder_id],
        }

        media = MediaFileUpload(file_path, mimetype=mimetype)

        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        return "https://drive.google.com/uc?export=download&id=" + file.get("id")
    except HttpError as err:
        print(err)


def dup_slide(slides_id, slides_name, folder_id):
    try:
        service = build("drive", "v3", credentials=creds)
        new_file = {
            "name": slides_name,
            "parents": [{"id": folder_id}],
        }

        new_slides = service.files().copy(fileId=slides_id, body=new_file).execute()

        return new_slides
    except HttpError as err:
        print(err)


def replace_slides_elements(reqs, new_slides_id):
    try:
        service_slides = build("slides", "v1", credentials=creds)

        service_slides.presentations().batchUpdate(
            body={"requests": reqs}, presentationId=new_slides_id
        ).execute()

    except HttpError as err:
        print(err)
