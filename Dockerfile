# app/Dockerfile

FROM python:3

WORKDIR /app

RUN apt-get update && apt-get install -y
RUN apt-get install build-essential
RUN apt-get install curl
RUN apt-get install software-properties-common -y
RUN apt-get install git
RUN rm -rf /var/lib/apt/lists/*
RUN apt-get install pkg-config -y
#RUN NEEDRESTART_MODE=a apt-get install python3-dev -y
RUN apt-get install default-libmysqlclient-dev -y
RUN apt-get install libmariadb-dev -y 

# RUN git clone https://github.com/markokajkut/administracija_troskova.git

# COPY requirements.txt ./requirements.txt

COPY app.py db_preparation.py .env .

RUN pip install python-dotenv
RUN pip install mysqlclient
RUN pip install SQLAlchemy
RUN pip install streamlit
RUN pip install mariadb

#RUN python db_preparation.py

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["python", "db_preparation.py"]
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
