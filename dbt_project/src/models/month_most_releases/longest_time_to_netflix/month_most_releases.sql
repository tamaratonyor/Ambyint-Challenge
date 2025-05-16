SELECT 
MONTH(parsed_date_added) AS month_number,
TO_CHAR(parsed_date_added, 'Month') AS month_name,
COUNT(*) AS number_of_releases
FROM 
{{ ref('stg_date_converted') }}
GROUP BY month_number, month_name
ORDER BY number_of_releases DESC
LIMIT 1
