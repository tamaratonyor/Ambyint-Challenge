{% set seed_tables = dbt_utils.get_relations_by_pattern(
    schema_pattern='public',
    table_pattern='netflix_titles%'
) %}

{% set unioned_queries = [] %}
{% for table in seed_tables %}
  {% do unioned_queries.append("select * from " ~ table) %}
{% endfor %}

{{ unioned_queries | join("\nunion all\n") }}
