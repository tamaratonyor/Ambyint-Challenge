WITH titles_with_woody AS (
  SELECT
    title,
    SPLIT(cast_name, ',') AS cast_array
  FROM {{ ref('stg_date_converted') }}
  WHERE cast_name ILIKE '%Woody Harrelson%'
),

exploded_cast AS (
  SELECT
    title,
    TRIM(f.value) AS actor
  FROM titles_with_woody,
       LATERAL FLATTEN(input => cast_array) f
  WHERE TRIM(f.value) != 'Woody Harrelson'
)

SELECT
  actor,
  COUNT(DISTINCT title) AS appearances_with_woody
FROM exploded_cast
GROUP BY actor
HAVING COUNT(DISTINCT title) > 1
ORDER BY appearances_with_woody DESC
