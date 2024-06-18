-- creacion de extensiones
CREATE EXTENSION IF NOT EXISTS plpgsql;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE EXTENSION IF NOT EXISTS intarray;
CREATE EXTENSION IF NOT EXISTS dblink;


-- catalogo de fuentes de datos
-- DROP TABLE public.fuente_datos;
CREATE TABLE public.fuente_datos (
	idfuente_datos serial4 NOT NULL,
	fuente_datos varchar(100) NULL,
	esquema_metadatos jsonb NULL,
	tipo_dato varchar(50) NULL,
	es_tercero bool NULL,
	CONSTRAINT fuente_datos_pkey PRIMARY KEY (idfuente_datos)
);

-- tabla de ocurrencias en formato json
-- DROP TABLE public.occ_variable;
CREATE TABLE public.occ_variable (
	idocc_var int4 NOT NULL DEFAULT nextval('occ_variable_idvar_seq'::regclass),
	idfuente_datos int4 NULL,
	metadatos jsonb NULL,
	CONSTRAINT occ_variable_pkey PRIMARY KEY (idocc_var)
);

-- tabla auxiliar para control de aois (no necesaria)
CREATE TABLE aoi (
	fgid int4 NULL,
	country varchar(200) NULL,
	geom geometry(multipolygon, 4326) NULL,
	gid serial4 NOT NULL
);
CREATE INDEX idx_aoi_geom ON public.aoi USING gist (geom);


-- catalogo de mallas
-- DROP TABLE public.area;
CREATE TABLE public.area (
	idarea serial4 NOT NULL,
	idregion int4 NULL,
	region varchar(50) NULL,
	resolucion varchar(50) NULL,
	gids _int4 NULL,
	CONSTRAINT area_pkey PRIMARY KEY (idarea)
);


-- tabla de celdas que componen las diferentes mallas (se crea a partir de tablas en RC)
-- DROP TABLE public.occ_malla;
CREATE TABLE public.occ_malla (
	idocc_malla int4 NULL,
	the_geom public.geometry(polygon, 4326) NULL,
	idarea int4 NULL
);

-- Tabla que almacena el agrupamiento de celdas por id de especie
-- tabla de registro unico de especies con arreglo de celdas (aproximacion de sp_snib) 
-- DROP TABLE public.grpocc_variable;
CREATE TABLE public.grpocc_variable (
	spid serial4 NOT NULL,
	reino varchar(255) NULL,
	phylum varchar(255) NULL,
	clase varchar(255) NULL,
	orden varchar(255) NULL,
	familia varchar(255) NULL,
	genero varchar(255) NULL,
	especie varchar(255) NULL,
	arg_grp_res64 _int4 NULL,
	arg_grp_res32 _int4 NULL,
	arg_grp_res16 _int4 NULL,
	arg_grp_res8 _int4 NULL,
	CONSTRAINT grpocc_variable_pkey PRIMARY KEY (spid)
);
-- iniciliza secuencia en 3000, la secuencia es creada autimaticamente cuando se crea la tabla
ALTER SEQUENCE grpocc_variable_spid_seq RESTART WITH 3000;
-- select nextval(pg_get_serial_sequence('grpocc_variable', 'spid'));



-- generacion de funciones
CREATE OR REPLACE FUNCTION public.get_epsilon(double precision, integer, integer, integer, integer)
 RETURNS double precision
 LANGUAGE sql
AS $function$
    SELECT $2*(((cast($3 as float)+($1/2))/(cast($2 as float)+$1))-((cast($4 as float)+$1)/(cast($5 as float)+(2*$1))))/(|/($2*((cast($4 as float)+$1)/(cast($5 as float)+2*$1))*(1-((cast($4 as float)+$1)/(cast($5 as float)+(2*$1))))));
  $function$
;



CREATE OR REPLACE FUNCTION public.get_score(double precision, integer, integer, integer, integer)
 RETURNS double precision
 LANGUAGE sql
AS $function$
      SELECT ((cast($3 as float)+($1/2))/(cast($4 as float)+$1))/(((cast($2 as float)-cast($3 as float))+($1/2))/((cast($5 as float)-cast($4 as float))+$1));
    $function$
;



