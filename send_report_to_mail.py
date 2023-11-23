import smtplib
import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileType, FileName, Disposition, ContentId
from dotenv import load_dotenv

load_dotenv()

#app_password = os.environ.get("EMAIL_APP_PASSWORD")
email_sender = os.environ.get("EMAIL_SENDER")
sendgrid_api = os.environ.get("SENDGRID_API")
#print(email_sender, sendgrid_api)

message = Mail(from_email=email_sender,
               to_emails='markokajkut1@gmail.com',
               subject='Monthly Report',
               plain_text_content='Please find attached the monthly report.',
               html_content='<strong>Please find attached the monthly report.</strong>')

file_path = 'Izvještaj_2023-11-12-2023-11-12.pdf'
with open(file_path, 'rb') as f:
    data = f.read()
encoded = base64.b64encode(data).decode()
attachment = Attachment()
attachment.file_content = FileContent(encoded)
attachment.file_type = FileType('application/pdf')
attachment.file_name = FileName(file_path)
attachment.disposition = Disposition('attachment')
attachment.content_id = ContentId('Example Content ID')
message.attachment = attachment

try:
    sg = SendGridAPIClient(sendgrid_api)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)


# # Function to send an email with an attached PDF
# def send_email(to_email, subject, body, attachment_path):
#     # Setup the MIME
#     message = MIMEMultipart()
#     message['From'] = email_sender
#     message['To'] = to_email
#     message['Subject'] = subject
#     message.attach(MIMEText(body, 'plain'))

#     # Attach the PDF file
#     with open(attachment_path, 'rb') as attachment:
#         pdf_attachment = MIMEApplication(attachment.read(), _subtype="pdf")
#         pdf_attachment.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
#         message.attach(pdf_attachment)

#     # Connect to the SMTP server and send the email
#     with smtplib.SMTP('smtp.mail.com', 587) as server:
#         server.starttls()
#         server.login(email_sender, app_password)
#         server.sendmail(email_sender, to_email, message.as_string())

# # Example usage
# pdf_report_path = 'Izvještaj_2023-11-12-2023-11-12.pdf'
# send_email('markokajkut1@gmail.com', 'Monthly Report', 'Please find attached the monthly report.', pdf_report_path)