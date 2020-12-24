DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles  -- SELECT list can be empty for this
      WHERE rolname = '{}') THEN

      CREATE GROUP {};
   END IF;
END
$do$;
