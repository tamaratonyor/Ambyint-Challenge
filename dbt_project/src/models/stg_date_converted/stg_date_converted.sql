SELECT 
  show_id,
  type,
  title,
  director,
  "CAST" AS cast_name,
  country,
  TRY_TO_DATE(TRIM(date_added), 'MMMM DD, YYYY') AS parsed_date_added,
  release_year,
  rating,
  duration,
  listed_in,
  description
FROM {{ ref('raw_merged') }}
WHERE date_added IS NOT NULL
