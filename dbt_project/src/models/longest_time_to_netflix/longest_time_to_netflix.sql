SELECT 
show_id,
title,
EXTRACT(YEAR FROM parsed_date_added) - release_year AS time_to_release
FROM 
{{ ref('stg_date_converted') }}
ORDER BY time_to_release
LIMIT 1