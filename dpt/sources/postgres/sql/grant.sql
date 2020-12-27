GRANT {{ permission }}
ON
  {% if target.type == 'SCHEMA' %}ALL SEQUENCES IN SCHEMA {{ target.id }} {% endif %}
TO {{ subject.id }}