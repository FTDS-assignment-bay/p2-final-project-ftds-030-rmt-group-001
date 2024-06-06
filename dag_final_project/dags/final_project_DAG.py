import re
import pandas as pd
import datetime as dt

from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from elasticsearch import Elasticsearch
from sqlalchemy import create_engine


def ambil_data():
    '''fetch data dari postgres'''
    database = "airflow"
    username = "airflow"
    password = "airflow"
    host = "postgres"

    # Membuat URL koneksi PostgreSQL
    postgres_url = f"postgresql+psycopg2://{username}:{password}@{host}/{database}"

    # Gunakan URL ini saat membuat koneksi SQLAlchemy
    engine = create_engine(postgres_url)
    conn = engine.connect()

    df = pd.read_sql_query("select * from final_project", conn)
    # Save DataFrame to CSV
    df.to_csv('/opt/airflow/dags/data_raw_load.csv', sep=',', index=False)

def clean_dataframe():
    ''' fungsi untuk membersihkan data'''
    # load data
    data = pd.read_csv("/opt/airflow/dags/data_raw_load.csv")
    
    # drop duplicate data
    data = data.drop_duplicates()

    # drop beberapa kolom yang tidak terlalu penting
    data = data.drop(['isbn13', 'isbn10', 'subtitle', 'thumbnail'], axis=1)

    # hapus data yang bersifat missing value
    data = data.dropna()

    # ubah beberapa kolom menjadi integer
    data[['published_year', 'num_pages', 'ratings_count']] = data[['published_year', 'num_pages', 'ratings_count']].astype(int)

    # buat function untuk pembersihan teks
    def pre_text(text):
        # lowercase
        text = text.lower()

        # whitespace
        text = text.strip()

        # menghapus semua karakter spesial kecuali spasi
        text = re.sub(r'[^A-Za-z0-9 ]+', '', text)

        return text
    
    # pembersihan teks pada kolom description
    data['description'] = data['description'].apply(lambda x: pre_text(x))

    # drop description yang kosong (bukan None)
    data = data.drop(data[data['description'] == ''].index)

    # ganti tanda penghubung pada authors
    data['authors'] = data['authors'].str.replace(';', ' & ')

    # kolom gabungan authors dan description
    data['desc_authors'] = data['description'] + ' ' + data['authors']
    
    # lowercase
    data['desc_authors'] = data['desc_authors'].str.lower()

    # reset index
    data = data.reset_index(drop=True)
    
    # save data
    data.to_csv('/opt/airflow/dags/data_clean.csv', index=False)


def upload_to_elasticsearch():
    ''' fungsi untuk mengupload data ke dalam elascticsearch'''
    es = Elasticsearch("http://elasticsearch:9200")
    data = pd.read_csv('/opt/airflow/dags/data_clean.csv')
    
    for i, r in data.iterrows():
        doc = r.to_dict()  # Convert the row to a dictionary
        res = es.index(index="final_project", id=i+1, body=doc)
        print(f"Response from Elasticsearch: {res}")
        
        
default_args = {
    'owner': 'group_1_030',
    'start_date': dt.datetime(2024, 6, 4, 13, 0, 0) - dt.timedelta(hours=7),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1)
}


with DAG(
    'Final_Project', #atur sesuai nama project kalian
    description='Final_project',
    schedule_interval='30 6 * * *', #atur schedule untuk menjalankan airflow pada 06:30.
    default_args=default_args,
    catchup=False
) as dag:
    # Task : 1
    '''  Fungsi ini ditujukan untuk mengambil data dari postgres.'''
    ambil_data_pg = PythonOperator(
        task_id='ambil_data_postgres',
        python_callable=ambil_data)    

    # Task: 2
    '''  Fungsi ini ditujukan untuk menjalankan pembersihan data.'''
    edit_data = PythonOperator(
        task_id='edit_data',
        python_callable=clean_dataframe)

    # Task: 3
    '''  Fungsi ini ditujukan untuk menyimpan data kedalam elasticsearch.'''
    """upload_data = PythonOperator(
        task_id='upload_data_elastic',
        python_callable=upload_to_elasticsearch)"""

    #proses untuk menjalankan di airflow
    ambil_data_pg >> edit_data #>> upload_data