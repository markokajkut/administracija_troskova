import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Function to send an email with an attached PDF
def send_email(to_email, subject, body):
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = 'sinisa_borjanic_reporting@mail.com'
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Attach the PDF file
    # with open(attachment_path, 'rb') as attachment:
    #     pdf_attachment = MIMEApplication(attachment.read(), _subtype="pdf")
    #     pdf_attachment.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
    #     message.attach(pdf_attachment)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP('smtp.mail.com', 587) as server:
        server.starttls()
        server.login('sinisa_borjanic_reporting@mail.com', 'borjanicizvjestaji123')
        server.sendmail('sinisa_borjanic_reporting@mail.com', to_email, message.as_string())

# Example usage
pdf_report_path = 'Izvještaj_2023-11-12-2023-11-12.pdf'
send_email('markokajkut1@gmail.com', 'Monthly Report', 'Please find attached the monthly report.')