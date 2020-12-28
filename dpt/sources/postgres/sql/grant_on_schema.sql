{% if permission.get('all') %}
GRANT ALL ON SCHEMA {{ target.id }} TO {{ subject.id }};
{% elif permission.get('usage') %}
GRANT USAGE ON SCHEMA {{ target.id }} TO {{ subject.id }};
{% endif %}

