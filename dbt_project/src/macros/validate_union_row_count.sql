{% macro validate_union_row_count(union_model, seed_prefix, database, schema) %}
{% set seed_tables = [] %}

-- Look for all relations in the schema that start with the prefix
{% set relations = dbt_utils.get_relations_by_prefix(schema, prefix=seed_prefix) %}

{% for rel in relations %}
  {% do seed_tables.append(rel) %}
{% endfor %}

{% if seed_tables | length == 0 %}
    select '❌ No seed tables found' as issue, 0 as seeds_count, 0 as unioned_count
{% else %}

with seed_counts as (
    {% for rel in seed_tables %}
        select count(*) as row_count from {{ rel }}
        {% if not loop.last %} union all {% endif %}
    {% endfor %}
),

total_seed_rows as (
    select sum(row_count) as seeds_count from seed_counts
),

unioned_count as (
    select count(*) as unioned_count from {{ ref(union_model) }}
)

select
    'Row count mismatch' as issue,
    s.seeds_count,
    u.unioned_count
from total_seed_rows s, unioned_count u
where s.seeds_count != u.unioned_count

{% endif %}
{% endmacro %}
