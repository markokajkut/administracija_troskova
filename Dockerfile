# app/Dockerfile

FROM python:3.10-slim-bullseye

WORKDIR /app

RUN DEBIAN_FRONTEND=noninteractive && apt-get update --fix-missing && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    pkg-config \
    #default-libmysqlclient-dev \
    wkhtmltopdf \
    #libmariadb3 \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*
    #pkg-config
    #xvfb \
    #libfontconfig \
#RUN apt-get update && apt-get install -y wkhtmltopdf
#RUN sudo apt-get install wkhtmltopdf
#    libmariadb-dev \
#RUN apt-get update && apt-get install -y dos2unix
# RUN git clone https://github.com/markokajkut/administracija_troskova.git

RUN mkdir ./app
RUN mkdir ./reports
RUN mkdir ./provision

COPY app ./app/
COPY provision ./provision/
COPY requirements.txt ./
COPY .env ./app/
COPY config.yaml ./
#COPY pages ./pages
#COPY cronfile /etc/cron.d/cronfile
#COPY wkhtmltox_0.12.6.1-2.bullseye_amd64.deb /usr/local/bin
#COPY provision_app ./provision_app
#COPY app.py db_preparation.py .env entrypoint.sh ./
RUN pip install --no-cache-dir -r requirements.txt
#WORKDIR /app
#RUN chmod 0744 ./send_report_to_mail.py
#RUN chmod 0644 /etc/cron.d/cronfile
# Create the log file to be able to run tail
#RUN touch /var/log/cronjob.log
#RUN crontab /etc/cron.d/cronfile
# Add the cron job directly in the Dockerfile
RUN chmod +x ./provision/cronfile.sh
RUN chmod +x ./provision/entrypoint.sh
#ADD crontab /etc/cron.d/my-cron-file
#USER root
#RUN echo "* * * * * ./cronfile.sh >> /var/log/cronjob.log 2>&1" | crontab -
#RUN (crontab -l 2>/dev/null || true; echo "*/1 * * * * /app/cronfile.sh >> /var/log/cronjob.log 2>&1") | crontab -
#RUN (crontab -l 2>/dev/null; echo "*/1 * * * * /app/cronfile.sh >> /var/log/cronjob.log 2>&1") | crontab -
#RUN crontab -l | { cat; echo "38 21 9 * * root /usr/local/bin/python /app/send_report_to_mail.py >> /var/log/cronjob.log 2>&1"; } | crontab -
# RUN pip install python-dotenv
# RUN pip install mysqlclient
# RUN pip install SQLAlchemy
# RUN pip install streamlit
# RUN pip install mariadb
#RUN crontab -l cronfile
#RUN curl -O https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.bullseye_amd64.deb
#RUN dpkg -i wkhtmltox_0.12.6.1-2.bullseye_amd64.deb
###RUN chmod +x ./entrypoint.sh
# Give execution rights on the cron job
#RUN chmod 0644 /etc/cron.d/my-cron
#RUN chmod +x wkhtmltox_0.12.6.1-2.bullseye_amd64.deb
#RUN python db_preparation.py

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["./provision/entrypoint.sh"]
#CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
# Run the command on container startup
#CMD ["cron", "-f"]
