import pandas as pd
import multiprocessing
import psycopg2
import xlwt
import json
import csv

# datos para la conexion a las bases de datos
dbhost = 'host_connection'
dbname = 'db_name'
dbuser = 'user'
dbpass = 'password'

# variables auxiliares para las funciones
region = "_mx"
tabla_bio = "bio019"
label = "Precipitation of Coldest Quarter"
coeficiente = "1"
unidad = "mm"

# funcion para realizar flujos de ejecucion
def do_all():

	print('==> BEGIN do_all ')

	# creacion de diccionario para carga de datos de la paltaforma Proyecto-42 del C3
	dic_global = createFileforProyecto42()
	
	# creacion de dataset para carga de datos de la paltaforma Proyecto-42 del C3
	createDataforProyecto42(dic_global)

	# obtiene las ocurrencias de la tabla snib de la base de integracion
	records = find_occ_integration()

	# obtiene los valores vectorizados de los raster de worldclim
	# records = find_occ_rasterbase()

	for row in records:
	# 	print("idejemplar: ", row[0])
	# 	# print("point: ", row[12])

		# obtiene lso ids de celda en las diferentes resoluciones de un punto (geom) dado
		cells = getIdCellFromPoint(row[12])
		if cells == None:
			continue

		# inserta el registro en la tabla de ocurrencias bajo el formato json establecido de las variables taxonomicas en la base de datos species beta
		insert_fuentedatos_spv3(row, cells)
		
		# inserta el registro en la tabla de ocurrencias bajo el formato json establecido de las variables raster en la base de datos species beta
		# insert_fuentedatos_raster_spv3(row)
			
	print('==> FINISH do_all')

# obtiene las ocurrencias de la tabla snib de la base de integracion
def find_occ_integration():

	try:
		print('====> ****** BEGIN find_occ_integration ')

		# conexion a base de datos de integracion
		conn_string = 'host={dbhost} dbname={dbname} user={dbuser} password={dbpass}'.format(dbhost=dbhost, dbname=dbname, dbuser=dbuser, dbpass=dbpass)
		# print("********* conexion: ", conn_string)

		conn = psycopg2.connect(conn_string)
		conn.autocommit = True
		cur = conn.cursor()

		# print(idejemplar)
		# query = "select idejemplar, reinovalido, phylumdivisionvalido, clasevalida, ordenvalido, familiavalida, generovalido, especievalida, aniocolecta, mescolecta, diacolecta, urlejemplar, the_geom from snib where the_geom is not null offset 14100000 limit 10000000;"
		query = "select idejemplar, reinovalido, phylumdivisionvalido, clasevalida, ordenvalido, familiavalida, generovalido, especievalida, aniocolecta, mescolecta, diacolecta, urlejemplar, the_geom from snib where the_geom is not null and fuente_datos = 'snib'"
		
		# print(query)
		cur.execute(query)
		records = cur.fetchall()

	except (Exception, psycopg2.Error) as error:
		print("Error while fetching data from PostgreSQL", error)
	finally:
	    if conn:
	    	cur.close()
	    	conn.close()
	    	# print("PostgreSQL connection is closed")
	    print('====> ****** FINISH find_occ_integration ')
	    return records

# obtiene lso ids de celda en las diferentes resoluciones de un punto (geom) dado
def getIdCellFromPoint(the_geom):

	try:
		# print('====> ****** BEGIN getIdCellFromPoint ')

		# conexion a base de datos de integracion
		conn_string = 'host={dbhost} dbname={dbname} user={dbuser} password={dbpass}'.format(dbhost=dbhost, dbname=dbname, dbuser=dbuser, dbpass=dbpass)
		# print("conn_string: " + conn_string)

		conn = psycopg2.connect(conn_string)
		conn.autocommit = True
		cur = conn.cursor()

		query = "select gridid_64km, gridid_32km, gridid_16km, gridid_8km from grid_8km_aoi where ST_Intersects(ST_GeomFromText(ST_AsText('" + the_geom + "'),4326), the_geom)"
		# query = "select gridid_64km, gridid_32km, gridid_16km, gridid_8km from grid_8km_aoi where ST_Intersects(ST_GeomFromText('POINT (-122.6 50.9)',4326), the_geom)"
		# print(query)

		cur.execute(query)
		record = cur.fetchone()
		# print(len(record))

		
	except (Exception, psycopg2.Error) as error:
		print("Error while fetching data from PostgreSQL", error)
	finally:
	    if conn:
	    	cur.close()
	    	conn.close()
	    # print('====> ****** FINISH getIdCellFromPoint ')
	    return record

# inserta el registro en la tabla de ocurrencias bajo el formato json establecido de las variables taxonomicas en la base de datos species beta
def insert_fuentedatos_spv3(row, cells):

	try:
		# print('====> ****** BEGIN insert_fuentedatos_spv3 ')

		# conexion a base de datos de integracion
		conn_string = 'host={dbhost} dbname={dbname} user={dbuser} password={dbpass}'.format(dbhost=dbhost, dbname=dbname_speciesv3, dbuser=dbuser, dbpass=dbpass)
		# print("********* conexion: ", conn_string)

		conn = psycopg2.connect(conn_string)
		conn.autocommit = True
		cur = conn.cursor()
		# print(row)

		jsonvar = '{"64km":' + str(cells[0]) + ', "32km":' + str(cells[1]) + ', "16km":' + str(cells[2]) + ', "8km":' + str(cells[3]) + ', "idejemplar":"' + row[0] + '","reino":"' + row[1] + '","phylum":"' + row[2] + '","clase":"' + row[3] + '","orden":"' + row[4] + '","familia":"' + row[5] + '","genero":"' + row[6] + '","especie":"' + row[7] + '","aniocolecta":' + str(row[8]) + ',"mescolecta":' + str(row[9]) + ',"diacolecta":' + str(row[10]) + ',"urlejemplar":"' + str(row[11]) + '","the_geom":"' + row[12] + '"}'
		# print("jsonvar: ", jsonvar)

		# insercion de datos para fuente de datos snib: 1
		query = 'INSERT INTO occ_variable (idfuente_datos, metadatos) VALUES(1,\'' + jsonvar + '\')'		
		# print(query)
		cur.execute(query)

	except (Exception, psycopg2.Error) as error:
		print("Error while fetching data from PostgreSQL", error)
	finally:
	    if conn:
	    	cur.close()
	    	conn.close()
	    	# print("PostgreSQL connection is closed")
	    # print('====> ****** FINISH insert_fuentedatos_spv3 ')

# obtiene los valores vectorizados de los raster de worldclim
def find_occ_rasterbase():

	try:
		print('====> ****** BEGIN find_occ_rasterbase ')

		# conexion a base de datos de integracion
		conn_string = 'host={dbhost} dbname={dbname} user={dbuser} password={dbpass}'.format(dbhost=dbhost, dbname=dbname_speciesv3, dbuser=dbuser, dbpass=dbpass)
		# print("********* conexion: ", conn_string)

		conn = psycopg2.connect(conn_string)
		conn.autocommit = True
		cur = conn.cursor()

		
		query = "SELECT id, the_geom, fid, value, country, fgid, gid, newvalue FROM " + tabla_bio + region + ";"
		
		# print(query)
		cur.execute(query)
		records = cur.fetchall()

	except (Exception, psycopg2.Error) as error:
		print("Error while fetching data from PostgreSQL", error)
	finally:
	    if conn:
	    	cur.close()
	    	conn.close()
	    	# print("PostgreSQL connection is closed")
	    print('====> ****** FINISH find_occ_rasterbase ')
	    return records

# inserta el registro en la tabla de ocurrencias bajo el formato json establecido de las variables raster en la base de datos species beta
def insert_fuentedatos_raster_spv3(row):

	try:
		# print('====> ****** BEGIN insert_fuentedatos_raster_spv3 ')

		# conexion a base de datos de integracion
		conn_string = 'host={dbhost} dbname={dbname} user={dbuser} password={dbpass}'.format(dbhost=dbhost, dbname=dbname_speciesv3, dbuser=dbuser, dbpass=dbpass)
		# print("********* conexion: ", conn_string)

		conn = psycopg2.connect(conn_string)
		conn.autocommit = True
		cur = conn.cursor()

		# {"bid": "string", "tag": "string", "icat": "string", "type": "string", "label": "string", "layer": "string", "unidad": "string", "the_geom": "geometry", "coeficiente": "string"}

		jsonvar = '{"bid":"' + str(row[2]) + '","value":' + str(row[7]) + ',"type":"001","label":"' + label + '","layer":"' + tabla_bio + '","unidad":"' + unidad + '","coeficiente":"' + coeficiente + '","the_geom":"' + row[1]  + '"}'
		# print("jsonvar: ", jsonvar)

		# insercion de datos para fuente de datos snib: 1
		query = 'INSERT INTO occ_variable (idfuente_datos, metadatos) VALUES(2,\'' + jsonvar + '\')'		
		# print(query)
		cur.execute(query)

	except (Exception, psycopg2.Error) as error:
		print("Error while fetching data from PostgreSQL", error)
	finally:
	    if conn:
	    	cur.close()
	    	conn.close()
	    	# print("PostgreSQL connection is closed")
	    # print('====> ****** FINISH insert_fuentedatos_raster_spv3 ')


def addCell2Meta():

	try:
		print('====> ****** BEGIN addCell2Meta ')

		# conexion a base de datos de integracion
		conn_string = 'host={dbhost} dbname={dbname} user={dbuser} password={dbpass}'.format(dbhost=dbhost, dbname=dbname_speciesv3, dbuser=dbuser, dbpass=dbpass)

		print("conn_string: " + conn_string)

		conn = psycopg2.connect(conn_string)
		conn.autocommit = True
		cur = conn.cursor()

		query = "select metadatos->>'idejemplar' as idejemplar, om.idocc_malla from occ_variable toc join occ_malla om on ST_Intersects(ST_GeomFromText(ST_AsText(metadatos->> 'the_geom'),4326), om.the_geom) where idfuente_datos = 1 and metadatos->>'clase' = 'Mammalia'"
		
		print(query)
		cur.execute(query)
		records = cur.fetchall()

		print("records length:" + str(len(records)))

		for row in records:
			print("idejemplar: ", row[0])
			print("idocc_malla: ", row[1])

			query = "update occ_variable set metadatos =  metadatos || '{\"64km\":" + str(row[1]) + "}' where metadatos->> 'idejemplar' = '" + row[0] + "'"
			cur.execute(query)


	except (Exception, psycopg2.Error) as error:
		print("Error while fetching data from PostgreSQL", error)
	finally:
	    if conn:
	    	cur.close()
	    	conn.close()
	    	# print("PostgreSQL connection is closed")
	    print('====> ****** FINISH addCell2Meta ')
	    return records


# creacion de diccionario para carga de datos de la paltaforma Proyecto-42 del C3
def createFileforProyecto42():

	print('====> ****** BEGIN createFileforProyecto42')

	try:

		# conexion a base de datos de integracion
		conn_string = 'host={dbhost} dbname={dbname} user={dbuser} password={dbpass}'.format(dbhost=dbhost, dbname=dbname_speciesv3, dbuser=dbuser, dbpass=dbpass)
		# print("********* conexion: ", conn_string)

		conn = psycopg2.connect(conn_string)
		conn.autocommit = True
		cur = conn.cursor()
		nivel_taxon = ["reino", "phylum", "clase", "orden", "familia", "genero", "especie"]
		# nivel_taxon = ["reino", "phylum", "clase", "orden"]
		
		headers = ["subcategoria", "var", "var_alias", "description", "visibility", "is_category", "values"]
		first_row = ["taxonomia", "idejemplar", "idejemplar", "identificador de la occ", "visible", "FALSO", "{'is_category': 'false'}"]
		campos_genericos = ["taxonomia", "visible", "CIERTO"]
		row1 = ["Taxonomia", "aniocolecta", "aniocolecta", "año de la colecta de la occ", "visible", "FALSO", "{'is_category': 'false'}"]
		row2 = ["Taxonomia", "mescolecta", "mescolecta", ",mes de la colecta de la occ", "visible", "FALSO", "{'is_category': 'false'}"]
		row3 = ["Taxonomia", "diacolecta", "diacolecta", ",dia de la colecta de la occ", "visible", "FALSO", "{'is_category': 'false'}"]
		row4 = ["Taxonomia", "the_geom", "the_geom", ",geometria de la colecta de la occ", "visible", "FALSO", "{'is_category': 'false'}"]
		row5 = ["Taxonomia", "64km", "64km" ,"id de celda de la occ", "visible", "FALSO", "{'is_category': 'false'}"]
		row6 = ["Taxonomia", "32km", "32km" ,"id de celda de la occ", "visible", "FALSO", "{'is_category': 'false'}"]
		row7 = ["Taxonomia", "16km", "16km" ,"id de celda de la occ", "visible", "FALSO", "{'is_category': 'false'}"]
		row8 = ["Taxonomia", "8km", "8km" ,"id de celda de la occ", "visible", "FALSO", "{'is_category': 'false'}"]

		# diccionarios
		dic_reino = {}
		dic_phylum = {}
		dic_clase = {}
		dic_orden = {}
		dic_familia = {}
		dic_genero = {}
		dic_especie = {}

		# book = xlwt.Workbook(encoding="utf-8")
		# sheet1 = book.add_sheet("diccionario")
		# sheet1.write(0, 5, "values")

		with open('test.csv', 'w', newline='') as file:
			writer = csv.writer(file, delimiter='|')
			field = headers
			writer.writerow(field)

		with open('test.csv', 'a', newline='') as file:
				writer = csv.writer(file, delimiter='|')
				field = first_row
				writer.writerow(field)


		for id_taxon, taxon in enumerate(nivel_taxon):

			print("id_taxon: " + str(id_taxon), ", taxon: " + taxon)

			# subarray_taxon = nivel_taxon[0:id_taxon+1]
			subarray_taxon = nivel_taxon[id_taxon]
			# print(subarray_taxon)
			# subarray_string = ','.join(subarray_taxon)
			subarray_string = subarray_taxon
			# print("subarray_string: " + subarray_string)

			gen_dic = {}
			if id_taxon == 0:
				gen_dic = dic_reino
			if id_taxon == 1:
				gen_dic = dic_phylum
			if id_taxon == 2:
				gen_dic = dic_clase
			if id_taxon == 3:
				gen_dic = dic_orden
			if id_taxon == 4:
				gen_dic = dic_familia
			if id_taxon == 5:
				gen_dic = dic_genero
			if id_taxon == 6:
				gen_dic = dic_especie


			# insercion de datos para fuente de datos snib: 1
			query = 'select distinct ' + subarray_string + ' from public.grpocc_variable'
			print(query)

			cur.execute(query)
			records = cur.fetchall()

			# {'is_category': 'true', 'options': {'1':'Protoctista','2':'Prokaryotae','3':'Plantae','4':'Fungi','5':'Protozoa','6':'Animalia'}}
			origin_value = {}
			origin_value['is_category'] = 'true'

			for idx, x in enumerate(records):
				# print(idx)
				# value = ','.join(x[0:id_taxon+1])
				value = records[idx][0]
				# print(value)
				# gen_dic[value] = (idx+1)
				gen_dic[(idx+1)] = value

			origin_value['options'] = gen_dic
			# sheet1.write((id_taxon+1), 5, json.dumps(origin_value))

			# if id_taxon == 0:
			# 	with open('test.csv', 'w', newline='') as file:
			# 		writer = csv.writer(file, delimiter='|')
			# 		field = [taxon, json.dumps(origin_value)]
			# 		writer.writerow(field)
			# else:
			
			with open('test.csv', 'a', newline='') as file:
				writer = csv.writer(file, delimiter='|')
				field = [campos_genericos[0], taxon, taxon, taxon + " de la occ", campos_genericos[1], campos_genericos[2], json.dumps(origin_value)]
				writer.writerow(field)

		# print(dic_reino.items())
		# print(dic_phylum.items())
		# print(dic_clase.items())
		# print(dic_orden.items())
		# print(dic_reino.get(1))
		# print(dic_familia.items())

		with open('test.csv', 'a', newline='') as file:
			writer = csv.writer(file, delimiter='|')
			writer.writerow(row1)
		with open('test.csv', 'a', newline='') as file:
			writer = csv.writer(file, delimiter='|')
			writer.writerow(row2)
		with open('test.csv', 'a', newline='') as file:
			writer = csv.writer(file, delimiter='|')
			writer.writerow(row3)
		with open('test.csv', 'a', newline='') as file:
			writer = csv.writer(file, delimiter='|')
			writer.writerow(row4)
		with open('test.csv', 'a', newline='') as file:
			writer = csv.writer(file, delimiter='|')
			writer.writerow(row5)
		with open('test.csv', 'a', newline='') as file:
			writer = csv.writer(file, delimiter='|')
			writer.writerow(row6)
		with open('test.csv', 'a', newline='') as file:
			writer = csv.writer(file, delimiter='|')
			writer.writerow(row7)
		with open('test.csv', 'a', newline='') as file:
			writer = csv.writer(file, delimiter='|')
			writer.writerow(row8)


	except (Exception, psycopg2.Error) as error:
		print("Error while fetching data from PostgreSQL", error)

	finally:

	    if conn:
	    	cur.close()
	    	conn.close()
	    	print("PostgreSQL connection is closed")

	    dic_global = {'reino': dic_reino, 'phylum': dic_phylum, 'clase': dic_clase, 'orden': dic_orden, 'familia': dic_familia, 'genero': dic_genero, 'especie': dic_especie}

	    print('====> ****** FINISH createFileforProyecto42')

	    return dic_global
	    	
# creacion de dataset para carga de datos de la paltaforma Proyecto-42 del C3
def createDataforProyecto42(dic_global):

	print('====> ****** BEGIN createDataforProyecto42')

	try:
		dic_reino = dic_global.get('reino')
		dic_phylum = dic_global.get('phylum')
		dic_clase = dic_global.get('clase')
		dic_orden = dic_global.get('orden')
		dic_familia = dic_global.get('familia')
		dic_genero = dic_global.get('genero')
		dic_especie = dic_global.get('especie')
		
		# print(dic_reino)
		# print(dic_phylum)

		# conexion a base de datos de integracion
		conn_string = 'host={dbhost} dbname={dbname} user={dbuser} password={dbpass}'.format(dbhost=dbhost, dbname=dbname_speciesv3, dbuser=dbuser, dbpass=dbpass)
		# print("********* conexion: ", conn_string)

		conn = psycopg2.connect(conn_string)
		conn.autocommit = True
		cur = conn.cursor()

		query = "select metadatos->>'idejemplar' as idejemplar, metadatos->>'reino' as reino, metadatos->>'phylum' as phylum, metadatos->>'clase' as clase, metadatos->>'orden' as orden, metadatos->>'familia' as familia, metadatos->>'genero' as genero, metadatos->>'especie' as especie, metadatos->>'the_geom' as the_geom, metadatos->>'aniocolecta' as aniocolecta, metadatos->>'mescolecta' as mescolecta, metadatos->>'diacolecta' as diacolecta, metadatos->>'64km' as cell_64km, metadatos->>'32km' as cell_32km, metadatos->>'16km' as cell_16km, metadatos->>'8km' as cell_8km from occ_variable ov where idfuente_datos = 1 "
		cur.execute(query)
		records = cur.fetchall()

		first_row = True

		for record in records:

			print(record[0])
			# print(record[4])
			# print(dic_clase.get(record[3]))
			# print(dic_orden.get(record[4]))

			field = [record[0], dic_reino.get(record[1]), dic_phylum.get(record[2]), dic_clase.get(record[3]), dic_orden.get(record[4]), dic_familia.get(record[5]), dic_genero.get(record[6]), dic_especie.get(record[7]), record[8], record[9], record[10], record[11], record[12], record[13], record[14], record[15]]

			if first_row:
				with open('test_data.csv', 'w', newline='') as file:
					writer = csv.writer(file, delimiter='|')
					writer.writerow(field)
			else:
				with open('test_data.csv', 'a', newline='') as file:
					writer = csv.writer(file, delimiter='|')
					writer.writerow(field)

			first_row = False


	except (Exception, psycopg2.Error) as error:
		print("Error while fetching data from PostgreSQL", error)

	finally:
	    
	    print('====> ****** FINISH createDataforProyecto42')	


# punto de entrada
if __name__ == '__main__':
	do_all()
