WITH flattened_casts AS (
    SELECT 
        TRIM(SPLIT_PART(actor.value::STRING, ' ', 1)) AS first_name
    FROM {{ ref('raw_merged') }} AS r
    , LATERAL FLATTEN(input => SPLIT(r.cast, ',')) AS actor
),

filtered_names AS (
    SELECT *
    FROM flattened_casts
    WHERE first_name IS NOT NULL AND first_name <> ''
)

SELECT 
    first_name,
    COUNT(*) AS appearances
FROM filtered_names
GROUP BY first_name
ORDER BY appearances DESC
LIMIT 1
