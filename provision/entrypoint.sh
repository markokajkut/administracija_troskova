#!/bin/sh

streamlit run ./app/Pregled_podataka.py --server.port=8501 --server.address=0.0.0.0
#echo "02 18 10 * * root /usr/bin/python /app/send_report_to_mail.py > /proc/1/fd/1 2>/proc/1/fd/2" >> /etc/crontab