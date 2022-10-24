from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from datetime import datetime, timedelta
from airflow.operators import BashOperator

args = {
    'owner':'airflow',
    'start_date': datetime(2022,10,24)
}

def push_function(**kwargs):
    pushed_value = 4
    ti = kwargs['ti']
    ti.xcom_push(key='pushed_value',value=pushed_value)

def branch_function(**kwargs):
    ti = kwargs['ti']
    pulled_value = ti.xcom_pull(key='pushed_value')
    if pulled_value % 2 == 0:
        return 'even_task'
    else:
        return 'odd_task'


with DAG(dag_id='branching', default_args=args, schedule_interval="@daily") as dag:
    push_task = PythonOperator(
        task_id='pushed_value',
        python_callable=push_function,
        provide_context=True
    )

    branch_task = BranchPythonOperator(
        task_id='Branching',
        python_callable=branch_function,
        provide_context=True
    )

    even_task = BashOperator(
        task_id='even_task',
        bash_command='echo "Got an even"'
    )

    odd_task = BashOperator(
        task_id='odd_task',
        bash_command='echo "Got an odd"'
    )

    push_task >> branch_task >> [even_task, odd_task]

