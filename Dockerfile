# app/Dockerfile

FROM python:3.10-slim-bullseye

WORKDIR /app

RUN DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    pkg-config \
    default-libmysqlclient-dev \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/* \
    pkg-config \
    default-libmysqlclient-dev \
    libmariadb-dev 

# RUN git clone https://github.com/markokajkut/administracija_troskova.git

COPY requirements.txt _Pregled_podataka.py .env app_skelet_unos.py config.yaml entrypoint.sh report_template.html report.py unos_u_bazu.py weather.py app/
COPY provision /app/provision
COPY pages /app/pages
#COPY app.py db_preparation.py .env entrypoint.sh ./
RUN pip install -r app/requirements.txt
#WORKDIR /app

# RUN pip install python-dotenv
# RUN pip install mysqlclient
# RUN pip install SQLAlchemy
# RUN pip install streamlit
# RUN pip install mariadb

RUN chmod +x app/entrypoint.sh
#RUN python db_preparation.py

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["./entrypoint.sh"]
#CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
