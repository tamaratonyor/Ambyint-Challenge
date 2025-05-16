pip install -r requirements.txt
python script.py
dbt deps
dbt seed --full-refresh && dbt run
