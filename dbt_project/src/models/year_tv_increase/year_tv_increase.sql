WITH count_tv_shows AS (
    SELECT 
        release_year,
        COUNT(*) AS number_tv_releases
    FROM 
        {{ ref('stg_date_converted') }}
    WHERE 
        type = 'TV Show'
    GROUP BY 
        release_year
),

yoy_change AS (
  SELECT
    curr.RELEASE_YEAR,
    curr.NUMBER_TV_RELEASES,
    prev.NUMBER_TV_RELEASES AS LAST_YEAR_RELEASES,
    curr.NUMBER_TV_RELEASES - prev.NUMBER_TV_RELEASES AS YOY_CHANGE,
    ROUND(
      (curr.NUMBER_TV_RELEASES - prev.NUMBER_TV_RELEASES) * 100.0 / NULLIF(prev.NUMBER_TV_RELEASES, 0),
      2
    ) AS YOY_PERCENT_CHANGE
  FROM count_tv_shows curr
  LEFT JOIN count_tv_shows prev
    ON curr.RELEASE_YEAR = prev.RELEASE_YEAR + 1
)

SELECT 
    release_year,
    number_tv_releases,
    last_year_releases,
    yoy_change AS percent_increase
FROM 
    yoy_change
WHERE last_year_releases IS NOT NULL
ORDER BY 
    percent_increase DESC
LIMIT 1