SELECT 
show_id,
title,
parsed_date_added,
release_year,
EXTRACT(YEAR FROM parsed_date_added) - release_year AS time_to_release
FROM 
{{ ref('stg_date_converted') }}
ORDER BY time_to_release DESC
LIMIT 1