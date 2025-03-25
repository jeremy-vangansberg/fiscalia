from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
# import sys
# import os

# sys.path.append('/opt/airflow/src')  # Ajoute explicitement le chemin
# print("PYTHONPATH set to:", sys.path)  # Debugging


# Import direct depuis src
from src.data_extraction.api_extractor import BofipExtractor
from src.data_transformation.decompressor import Decompressor
from src.config.settings import settings

# Configuration par défaut des tâches
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    'bofip_data_collection',
    default_args=default_args,
    description='Pipeline de collecte et traitement des données BOFiP',
    schedule_interval='0 0 * * *',  # Tous les jours à minuit
    start_date=days_ago(1),
    catchup=False,
    tags=['bofip', 'fiscalia'],
)
def bofip_collection_dag():
    """DAG pour la collecte et le traitement des données BOFiP"""

    @task(task_id='extract_data')
    def extract_bofip_data():
        """Extraction des données BOFiP"""
        extractor = BofipExtractor()
        file_path = extractor.extract_data()
        return str(file_path)

    @task(task_id='decompress_data')
    def decompress_bofip_data(file_path: str):
        """Décompression des données BOFiP"""
        decompressor = Decompressor(output_dir=settings.EXTRACTED_DIR)
        extracted_path = decompressor.decompress(file_path)
        return str(extracted_path)

    @task(task_id='transform_data')
    def transform_bofip_data(extracted_path: str):
        """Transformation des données BOFiP"""
        print(f"Transformation des données dans {extracted_path}")
        return extracted_path

    @task(task_id='upload_to_datalake')
    def upload_to_datalake(file_path: str):
        """Upload des fichiers vers Azure Data Lake"""
        destination = f"raw/bofip/{file_path.split('/')[-1]}"
        from src.scripts.upload_to_datalake import upload_to_datalake
        upload_to_datalake(
            source_path=file_path,
            destination_path=destination
        )
        return destination

    # Tâche de nettoyage des fichiers temporaires
    cleanup = BashOperator(
        task_id='cleanup',
        bash_command=f'rm -rf {settings.RAW_DIR}/* {settings.EXTRACTED_DIR}/*',
    )

    # Définition du flux de données
    file_path = extract_bofip_data()
    extracted_path = decompress_bofip_data(file_path)
    transformed_path = transform_bofip_data(extracted_path)
    uploaded_path = upload_to_datalake(file_path)
    
    # Définition de l'ordre des tâches
    [transformed_path, uploaded_path] >> cleanup

# Instanciation du DAG
dag = bofip_collection_dag() 