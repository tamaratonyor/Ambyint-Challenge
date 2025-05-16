-- depends_on: {{ ref('raw_merged') }}

{{ config(materialized='view') }}

{{ validate_union_row_count(
    union_model='raw_merged',
    seed_prefix='netflix_titles',
    database=target.database,
    schema=target.schema
) }}
