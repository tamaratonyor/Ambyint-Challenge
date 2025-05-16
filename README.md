# Ambyint-Challenge
Given the size of the files I opted to get them on snowflake using seeds. If the files were larger I would have dumped them on a bucket on S3 and created models using the s3 location. This method has no reliance on a cloud provider and so can be tested more easily if you would like to run it locally. I would also have created more models and had fewer CTEs if the data were much larger.

The python script can be ran provided you have set the following enviroment variables:
SF_USER,
SF_PASSWORD,
SF_ACCOUNT,
SF_WAREHOUSE,
SF_DATABASE,
SF_SCHEMA

Below are my solutions for the stages
Stage 1:
netflix_titles.csv is read into a table via dbt seeds

Stage 2:
Desired Snowflake object outputs are created by seeds, automation is done by cron job which is added to the cron directory once the setup.sh script is run. Other orchestration tools are better but this makes local testing easier

Stage 3:
Python script is script.py

Stage 4:
Testing is done in 2 areas, built in test on the columns, not_null and unique show IDs as well as
some accepted values for program type i.e. TV Show or Movie. More importantly, the union of all of the seed files the python script produces, is validated by the logic written in dbt_project/src/macros/validate_union_row_count.sql
And a desired view output is created by the dbt_project/src/models/tests/validate_dynamic_union_row_count.sql file

Stage 5:
Separate models are written for each of these results in the dbt_project/src/models directory
