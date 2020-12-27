DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = '{{ role_id }}') THEN

      CREATE GROUP {{ role_id }};
   END IF;
END
$do$;