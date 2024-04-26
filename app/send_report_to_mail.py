import os
import base64
import calendar
import subprocess
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileType, FileName, Disposition, ContentId
from dotenv import load_dotenv
from report import generate_report, delete_pdf_after_download
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

load_dotenv()

# def run_mysqldump(database, user, password, output_file):
#     try:
#         # Build the mysqldump command
#         command = [
#             'mysqldump',
#             '-u', user,
#             '-p' + password,
#             database,
#             '--result-file=' + output_file
#         ]

#         # Run the mysqldump command
#         subprocess.run(command, check=True)

#         print(f"Database dump completed successfully. Dump file saved to: {output_file}")
#     except subprocess.CalledProcessError as e:
#         print(f"Error: {e}")


# def run_mysqldump_and_transfer(database, database_container_name, user, password, output_file, app_container_name):
#     try:
#         # Build the mysqldump command
#         mysqldump_command = [
#             'docker', 'exec',
#             '-i', '--user', 'root',  # Specify the user if needed
#             database_container_name,  # Replace with your database container name
#             'mysqldump',
#             '-u', user,
#             f'--password={password}',
#             database
#         ]

#         # Run the mysqldump command and redirect output to a file
#         with open(output_file, 'wb') as dump_file:
#             subprocess.run(mysqldump_command, check=True, stdout=dump_file)

#         print(f"Database dump completed successfully. Dump file saved to: {output_file}")

#         # Copy the dump file from the database container to the app container
#         docker_cp_command = [
#             'docker', 'cp',
#             f'{database_container_name}:{output_file}',  # Replace with your database container name
#             app_container_name + f':/app/reports'  # Replace with the path in your app container
#         ]

#         subprocess.run(docker_cp_command, check=True)

#         print(f"Dump file copied to the app container.")
#     except subprocess.CalledProcessError as e:
#         print(f"Error: {e}")

# Replace these with your actual database credentials, dump file path, and container names
database_name = os.environ.get("DB_DATABASE")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
dump_file_path = '/var/backups/backup.sql'
app_container_name = 'app'
app_dump_path = 'app/reports/backup.sql'

# Run mysqldump in the database container and transfer the dump file to the app container
# run_mysqldump_and_transfer(database_name, "db", db_user, db_password, dump_file_path, app_container_name)



# database_name = os.environ.get("DB_DATABASE")
# db_user = os.environ.get("DB_USER")
# db_password = os.environ.get("DB_PASSWORD")
# dump_file_path = '/app/backup.sql'

# # Run mysqldump using the provided credentials
# run_mysqldump(database_name, db_user, db_password, dump_file_path)


def administracija_sqlalchemy():

    # sqlalchemy engine and connection
    engine = create_engine(
    f"mariadb+mariadbconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}",
    poolclass=QueuePool, pool_size=5, max_overflow=10)
    return engine

administracija_engine = administracija_sqlalchemy()


email_sender = os.environ.get("EMAIL_SENDER")
sendgrid_api = os.environ.get("SENDGRID_API")

current_date = datetime.now().date()

# Calculate the date exactly one month earlier
one_month_earlier = current_date - relativedelta(months=1)
# Find the last day of the month
last_day_of_month = calendar.monthrange(one_month_earlier.year, one_month_earlier.month)[1]
# Create a new date with the last day of the month
last_day_date = datetime(one_month_earlier.year, one_month_earlier.month, last_day_of_month).date()

mjeseci = {1: "Januar",
           2: "Februar",
           3: "Mart",
           4: "April",
           5: "Maj",
           6: "Jun",
           7: "Jul",
           8: "Avgust",
           9: "Septembar",
           10: "Oktobar",
           11: "Novembar",
           12: "Decembar"}

administracija_engine = administracija_sqlalchemy()
mail_receiver = os.environ.get("REPORT_MAIL_RECEIVER")
message = Mail(from_email=email_sender,
                to_emails=mail_receiver,
                subject='Mjesečni izvještaj Futuris SB',
                plain_text_content=f'U prilogu Vam dostavljamo izvještaj za mjesec {mjeseci[one_month_earlier.month].lower()}, {one_month_earlier.year} godine.', #Uz to Vam dostavljamo i bekap baze podataka.',
                html_content=f'<strong>U prilogu Vam dostavljamo izvještaj za mjesec {mjeseci[one_month_earlier.month].lower()}, {one_month_earlier.year} godine.') #Uz to Vam dostavljamo i bekap baze podataka.</strong>')

report_filename = generate_report(pocetni_datum=one_month_earlier,
                                    krajnji_datum=last_day_date,
                                    administracija_engine=administracija_engine)
file_path = f'./reports/{report_filename}'
with open(file_path, 'rb') as f:
    data = f.read()
encoded = base64.b64encode(data).decode()
attachment = Attachment()
attachment.file_content = FileContent(encoded)
attachment.file_type = FileType('application/pdf')
attachment.file_name = FileName(report_filename)
attachment.disposition = Disposition('attachment')
attachment.content_id = ContentId('Example Content ID 1')
message.attachment = attachment

# db_backup_name = f'backup_{mjeseci[current_date.month].lower()}_{current_date.year}.sql'
# with open(app_dump_path, 'rb') as f:
#     data = f.read()
# encoded = base64.b64encode(data).decode()
# attachment = Attachment()
# attachment.file_content = FileContent(encoded)
# attachment.file_type = FileType('application/sql')
# attachment.file_name = FileName(db_backup_name)
# attachment.disposition = Disposition('attachment')
# attachment.content_id = ContentId('Example Content ID 2')
# message.attachment = attachment

try:
    sg = SendGridAPIClient(sendgrid_api)
    response = sg.send(message)
    
    print(f"Report {report_filename} sent on {current_date}, to {mail_receiver}, with status code {response.status_code}, and headers {response.headers}.")
    print(f"Database backup {report_filename} sent on {current_date}, to {mail_receiver}, with status code {response.status_code}, and headers {response.headers}.")

    delete_pdf_after_download(report_filename)
except Exception as e:
    print(e)

# if os.path.exists(app_dump_path):
#     os.remove(app_dump_path)
#     print(f"Database backup {report_filename} removed.")
# else:
#     pass