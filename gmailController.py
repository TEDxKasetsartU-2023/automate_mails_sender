# gmail bot
# | IMPORT SECTION
import base64
import email.encoders as encoder
import mimetypes
import os
import time

from datetime import datetime
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from typing import Dict, List, Union

# | GLOBAL VARIABLES
# CREDENTIALS_FILENAME = "credentials.json"
# MAIL_LIST_FILENAME = "staff_res.csv"
# RESULT_FILENAME = "result.csv"
SCOPES = ["https://mail.google.com/"]

# | FUNCTIONS
def create_service(CREDENTIALS_FILENAME, SCOPES = ["https://mail.google.com/"]) -> Union[Resource, None]:
    creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILENAME, SCOPES
            )
            creds = flow.run_local_server(port=0)

    try:
        service = build("gmail", "v1", credentials=creds)
        print("service created successfully")
        return service
    except Exception as e:
        print("Unable to connect.")
        print(e)
        return None


# def create_message_with_files(
#     receiver: str, subject: str, text: str, files: List[str]
# ) -> Dict[str, str]:
#     message = MIMEMultipart()
#     message["to"] = receiver
#     message["subject"] = subject

#     msg = MIMEText(text, "html")
#     message.attach(msg)

#     _id = 1
#     for file, mode in files:
#         if file is not None:
#             content_type, encoding = mimetypes.guess_type(file)
#             if content_type is None or encoding is not None:
#                 content_type = "application/octet-stream"
#             main_type, sub_type = content_type.split("/", 1)
#             if main_type == "image":
#                 with open(file, "rb") as fp:
#                     msg = MIMEImage(fp.read(), _subtype=sub_type)
#             else:
#                 with open(file, "rb") as fp:
#                     msg = MIMEBase(main_type, sub_type)
#                     msg.set_payload(fp.read())

#             filename = os.path.basename(file)
#             if mode == "inline":
#                 msg.add_header("Content-Id", f"<file{_id}>")
#                 msg.add_header("Content-Disposition", "inline", filename=filename)
#                 _id += 1
#             else:
#                 msg.add_header("Content-Disposition", "attachment", filename=filename)
#                 if sub_type == "pdf":
#                     encoder.encode_base64(msg)
#             message.attach(msg)

#     return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}


def create_message(
    receiver: str, subject: str, text: str
) -> Dict[str, str]:
    message = MIMEMultipart()
    message["to"] = receiver
    message["subject"] = subject

    msg = MIMEText(text, "html")
    message.attach(msg)

    return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_msg(
    service: Resource, user_id: str, message: Dict[str, str]
) -> Union[Dict[str, Union[str, List[str]]], None]:
    try:
        res = service.users().messages().send(userId=user_id, body=message).execute()
        return res
    except HttpError as error:
        print(f"Error\n\n{error}")
        return None

# # | MAIN
# if __name__ == "__main__":
#     service = create_service()
#     parsed_html = "" # html that already parsed and ready to send
#     subject = "" # subject
#     email = "" # receiver e-mail
#     content = create_message(email, subject, parsed_html)
#     res = send_msg(service, "me", content)
#     print(res)