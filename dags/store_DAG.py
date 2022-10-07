from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from datacleaner import data_cleaner

default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2019, 12, 9),
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}


dag=DAG('store_dag',default_args=default_args,schedule_interval='@daily',
        template_searchpath=['/usr/local/airflow/sql_files'],
        catchup=False)


t1 = BashOperator(task_id='check_file_exists', bash_command='shasum /usr/local/airflow/store_files_airflow/raw_store_transactions.csv', 
                retries=2, retry_delay=timedelta(seconds=15),dag=dag)

t2 = PythonOperator(task_id='clean_csv',
                python_callable=data_cleaner,
                dag=dag)

t3 = MySqlOperator(task_id="mysql", 
                mysql_conn_id='mysql_conn',
                sql="create_table.sql",
                dag=dag)

t4 = MySqlOperator(
    task_id="InsertTable",
    mysql_conn_id='mysql_conn',
    sql="insert_into_table.sql",
    dag=dag
)

t5 = MySqlOperator(
    task_id="Create_Report",
    mysql_conn_id="mysql_conn",
    sql="select_from_table.sql",
    dag=dag
)



t1 >> t2 >> t3 >> t4 >> t5