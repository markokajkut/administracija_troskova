# app/Dockerfile

FROM python:3

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/* \
    apt install mariadb-server

# RUN git clone https://github.com/markokajkut/administracija_troskova.git

# COPY requirements.txt ./requirements.txt

COPY . .

RUN pip install python-dotenv
RUN pip install streamlit
RUN pip install mariadb

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
