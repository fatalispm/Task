CREATE TABLE persons (
  id INTEGER PRIMARY KEY NOT NULL DEFAULT nextval('persons_id_seq'::regclass),
  name CHARACTER VARYING(100),
  birth_date DATE,
  nationality CHARACTER VARYING(50),
  additional_info TEXT
);

CREATE TABLE unsorted_info (
  id INTEGER PRIMARY KEY NOT NULL DEFAULT nextval('unsorted_info_id_seq'::regclass),
  data JSONB,
  file_name CHARACTER VARYING(100),
  start BOOLEAN,
  title CHARACTER VARYING DEFAULT 100
);
