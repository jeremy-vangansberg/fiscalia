FROM apache/airflow:2.10.5

# Copier les requirements et les installer
COPY requirements.txt /
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt