# Ambyint-Challenge
Given the size of the files I opted to get them on snowflake using seeds. If the files were larger I would have dumped them on a bucket on S3 and created models using the s3 location. This method has no reliance on a cloud provider and so can be tested more easily if you would like to run it locally. 

The python script can be ran provided you have set the following enviroment variables:
SF_USER,
SF_PASSWORD,
SF_ACCOUNT,
SF_WAREHOUSE,
SF_DATABASE,
SF_SCHEMA

