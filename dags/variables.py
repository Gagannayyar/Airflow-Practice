import airflow
from airflow.operators.bash_operator import BashOperator
from airflow.models import DAG, Variable
from datetime import datetime, timedelta

default_args = {
    'owner':'airflow',
    'start_date': datetime(2022,10,16)
}

dag = DAG(
    'variable',
    default_args=default_args,
    schedule_interval=timedelta(1)
)

t1 = BashOperator(task_id="Some_task", bash_command="echo {{var.value.source_path}}",dag=dag)