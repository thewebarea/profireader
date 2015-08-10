

CREATE SEQUENCE user_company_role_id_seq
	START WITH 1
	INCREMENT BY 1
	NO MAXVALUE
	NO MINVALUE
	CACHE 1;

CREATE TABLE company_role (
	id character varying(50) NOT NULL
);

CREATE TABLE user_company_role (
	user_id uuid NOT NULL,
	company_id uuid NOT NULL,
	role_id character varying NOT NULL,
	id bigint DEFAULT nextval('user_company_role_id_seq'::regclass) NOT NULL
);

ALTER TABLE article
	ALTER COLUMN author_user_id TYPE integer /* TYPE change - table: article original: character varying(36) new: integer */,
	ALTER COLUMN company_id TYPE integer /* TYPE change - table: article original: character varying(36) new: integer */;

ALTER TABLE article_history
	ALTER COLUMN contributor_user_id TYPE integer /* TYPE change - table: article_history original: character varying(36) new: integer */;

ALTER TABLE company
	ADD COLUMN logo uuid,
	ADD COLUMN country character varying(70),
	ADD COLUMN region character varying(70),
	ADD COLUMN adress character varying(70),
	ADD COLUMN phone character varying(30),
	ADD COLUMN phone2 character varying(30),
	ADD COLUMN email character varying(50),
	ADD COLUMN short_description text,
	ALTER COLUMN id TYPE uuid /* TYPE change - table: company original: character varying(36) new: uuid */,
	ALTER COLUMN user_id TYPE uuid /* TYPE change - table: company original: character varying(36) new: uuid */,
	ALTER COLUMN user_id SET NOT NULL;

ALTER TABLE file
-- 	ADD COLUMN description character varying(1000) DEFAULT '':: character varying NOT NULL,
	ADD COLUMN copyright character varying(1000) DEFAULT ''::character varying NOT NULL,
	ADD COLUMN company_id integer,
	ADD COLUMN author character varying(100) DEFAULT ''::character varying NOT NULL,
	ADD COLUMN ac_count integer DEFAULT 0 NOT NULL,
	ALTER COLUMN name SET DEFAULT ''::character varying,
	ALTER COLUMN name SET NOT NULL,
	ALTER COLUMN mime SET DEFAULT 'text/plain'::character varying,
	ALTER COLUMN mime SET NOT NULL,
	ALTER COLUMN "size" SET DEFAULT 0,
	ALTER COLUMN "size" SET NOT NULL,
	ALTER COLUMN user_id TYPE integer /* TYPE change - table: file original: character varying(36) new: integer */,
	ALTER COLUMN cr_tm SET NOT NULL,
	ALTER COLUMN md_tm SET NOT NULL,
	ALTER COLUMN ac_tm SET NOT NULL,
	ALTER COLUMN id TYPE uuid /* TYPE change - table: file original: character varying(36) new: uuid */,
	ALTER COLUMN parent_id TYPE uuid /* TYPE change - table: file original: character varying(36) new: uuid */;

ALTER TABLE file_content
	ALTER COLUMN id TYPE uuid /* TYPE change - table: file_content original: character varying(36) new: uuid */;

ALTER TABLE "user"
	DROP COLUMN password_hash,
	DROP COLUMN registered_tm,
	DROP COLUMN email_conf_token,
	DROP COLUMN pass_reset_token,
	ADD COLUMN avatar_file_id uuid,
	ADD COLUMN password character varying(100),
	ADD COLUMN email_conf_key character varying(100),
	ADD COLUMN pass_reset_key character varying(100),
	ADD COLUMN registered_via character varying(20),
	ALTER COLUMN id TYPE uuid /* TYPE change - table: user original: character varying(36) new: uuid */,
	ALTER COLUMN profireader_gender TYPE character varying(100) /* TYPE change - table: user original: character varying(10) new: character varying(100) */,
	ALTER COLUMN profireader_link TYPE character varying(100) /* TYPE change - table: user original: text new: character varying(100) */,
	ALTER COLUMN profireader_phone TYPE character varying(100) /* TYPE change - table: user original: character varying(20) new: character varying(100) */,
	ALTER COLUMN about_me TYPE character varying(1000) /* TYPE change - table: user original: character varying(666) new: character varying(1000) */,
	ALTER COLUMN google_id TYPE character varying(100) /* TYPE change - table: user original: character varying(50) new: character varying(100) */,
	ALTER COLUMN google_gender TYPE character varying(100) /* TYPE change - table: user original: character varying(10) new: character varying(100) */,
	ALTER COLUMN google_link TYPE character varying(100) /* TYPE change - table: user original: text new: character varying(100) */,
	ALTER COLUMN google_phone TYPE character varying(100) /* TYPE change - table: user original: character varying(20) new: character varying(100) */,
	ALTER COLUMN facebook_id TYPE character varying(100) /* TYPE change - table: user original: character varying(50) new: character varying(100) */,
	ALTER COLUMN facebook_gender TYPE character varying(100) /* TYPE change - table: user original: character varying(10) new: character varying(100) */,
	ALTER COLUMN facebook_link TYPE character varying(100) /* TYPE change - table: user original: text new: character varying(100) */,
	ALTER COLUMN facebook_phone TYPE character varying(100) /* TYPE change - table: user original: character varying(20) new: character varying(100) */,
	ALTER COLUMN linkedin_id TYPE character varying(100) /* TYPE change - table: user original: character varying(50) new: character varying(100) */,
	ALTER COLUMN linkedin_gender TYPE character varying(100) /* TYPE change - table: user original: character varying(10) new: character varying(100) */,
	ALTER COLUMN linkedin_link TYPE character varying(100) /* TYPE change - table: user original: text new: character varying(100) */,
	ALTER COLUMN linkedin_phone TYPE character varying(100) /* TYPE change - table: user original: character varying(20) new: character varying(100) */,
	ALTER COLUMN twitter_id TYPE character varying(100) /* TYPE change - table: user original: character varying(50) new: character varying(100) */,
	ALTER COLUMN twitter_gender TYPE character varying(100) /* TYPE change - table: user original: character varying(10) new: character varying(100) */,
	ALTER COLUMN twitter_link TYPE character varying(100) /* TYPE change - table: user original: text new: character varying(100) */,
	ALTER COLUMN twitter_phone TYPE character varying(100) /* TYPE change - table: user original: character varying(20) new: character varying(100) */,
	ALTER COLUMN microsoft_id TYPE character varying(100) /* TYPE change - table: user original: character varying(50) new: character varying(100) */,
	ALTER COLUMN microsoft_gender TYPE character varying(100) /* TYPE change - table: user original: character varying(10) new: character varying(100) */,
	ALTER COLUMN microsoft_link TYPE character varying(100) /* TYPE change - table: user original: text new: character varying(100) */,
	ALTER COLUMN microsoft_phone TYPE character varying(100) /* TYPE change - table: user original: character varying(20) new: character varying(100) */,
	ALTER COLUMN yahoo_id TYPE character varying(100) /* TYPE change - table: user original: character varying(50) new: character varying(100) */,
	ALTER COLUMN yahoo_gender TYPE character varying(100) /* TYPE change - table: user original: character varying(10) new: character varying(100) */,
	ALTER COLUMN yahoo_link TYPE character varying(100) /* TYPE change - table: user original: text new: character varying(100) */,
	ALTER COLUMN yahoo_phone TYPE character varying(100) /* TYPE change - table: user original: character varying(20) new: character varying(100) */;

ALTER SEQUENCE user_company_role_id_seq
	OWNED BY user_company_role.id;

CREATE OR REPLACE FUNCTION has_user_in_company_role(u_id uuid, c_id uuid, inc character varying[], exc character varying[]) RETURNS boolean
    LANGUAGE plpgsql
    AS $$DECLARE
ret Boolean;
roles varchar(50)[];
BEGIN
  SELECT INTO roles role_id FROM user_company_role WHERE user_company_role.user_id=i_id AND user_company_role.company_id=c_id;
  RETURN True;
END$$;

CREATE OR REPLACE FUNCTION row_cr_md() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN

NEW.cr_tm = clock_timestamp();
NEW.md_tm = NEW.cr_tm;
RETURN NEW;

END$$;

CREATE OR REPLACE FUNCTION row_cr_md_ac() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN

NEW.cr_tm = localtimestamp;
NEW.md_tm = NEW.cr_tm;
NEW.ac_tm = NEW.cr_tm;
RETURN NEW;

END$$;

CREATE OR REPLACE FUNCTION row_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$DECLARE
    local_time double precision := EXTRACT(EPOCH FROM localtimestamp)::double precision;
    server_id character(3) := '001';
BEGIN
   -- f47ac10b-58cc-4372-a567-0e02b2c3d479

   NEW.id = lpad(to_hex(floor(local_time)::int), 8, '0') || '-' ||
             lpad(to_hex(floor((local_time - floor(local_time))*100000)::int), 4, '0') || '-' ||
             '4' || server_id || '-' ||
             overlay(
                     to_hex((floor(random() * 65535)::int | (x'8000'::int) ) &  (x'bfff'::int)  ) ||
                     lpad(to_hex(floor(random() * 65535)::bigint),4,'0') || lpad(to_hex(floor(random() * 65535)::bigint),4,'0') || lpad(to_hex(floor(random() * 65535)::bigint),4,'0')
                  placing '-' from 5 for 0);


   return NEW;


END$$;

CREATE OR REPLACE FUNCTION row_md() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN

NEW.md_tm = clock_timestamp();
RETURN NEW;

END$$;

ALTER TABLE company
	ADD CONSTRAINT company_id PRIMARY KEY (id);

ALTER TABLE company_role
	ADD CONSTRAINT company_role_pkey PRIMARY KEY (id);

ALTER TABLE file
	ADD CONSTRAINT file_id PRIMARY KEY (id);

ALTER TABLE file_content
	ADD CONSTRAINT file_content_file_id PRIMARY KEY (id);

ALTER TABLE "user"
	ADD CONSTRAINT user_id PRIMARY KEY (id);

ALTER TABLE user_company_role
	ADD CONSTRAINT user_company_role_id_primary_key PRIMARY KEY (id);

ALTER TABLE company
	ADD CONSTRAINT company_name_key UNIQUE (name);

ALTER TABLE company
	ADD CONSTRAINT company_logo_fkey FOREIGN KEY (logo) REFERENCES file(id);

ALTER TABLE company
	ADD CONSTRAINT company_user_id FOREIGN KEY (user_id) REFERENCES "user"(id) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE file
	ADD CONSTRAINT only_one_file_in_folder UNIQUE (name, parent_id);

ALTER TABLE file
	ADD CONSTRAINT file_parent_id FOREIGN KEY (parent_id) REFERENCES file(id) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE file_content
	ADD CONSTRAINT file_content_file_id_fkey FOREIGN KEY (id) REFERENCES file(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE "user"
	ADD CONSTRAINT user_google_id_google_email_key UNIQUE (google_id, google_email);

ALTER TABLE "user"
	ADD CONSTRAINT user_avatar_file_id_fkey FOREIGN KEY (avatar_file_id) REFERENCES file(id);

ALTER TABLE user_company_role
	ADD CONSTRAINT user_company_role_company_id FOREIGN KEY (company_id) REFERENCES company(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE user_company_role
	ADD CONSTRAINT user_company_role_id_fk FOREIGN KEY (role_id) REFERENCES company_role(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE user_company_role
	ADD CONSTRAINT user_company_role_user_id FOREIGN KEY (user_id) REFERENCES "user"(id) ON UPDATE CASCADE ON DELETE CASCADE;

CREATE TRIGGER id
	BEFORE INSERT ON company
	FOR EACH ROW
	EXECUTE PROCEDURE row_id();

CREATE TRIGGER cr_md_ac
	BEFORE INSERT ON file
	FOR EACH ROW
	EXECUTE PROCEDURE row_cr_md_ac();

CREATE TRIGGER id
	BEFORE INSERT ON file
	FOR EACH ROW
	EXECUTE PROCEDURE row_id();

CREATE TRIGGER id
	BEFORE INSERT ON "user"
	FOR EACH ROW
	EXECUTE PROCEDURE row_id();
