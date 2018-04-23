import pyodbc
'''
server = 'SRVBDDGDB.igepn.edu.ec'
database = 'GDB_TV'
username = 'user_gdbt_cns'
password = 'necofI2017'
driver= 'GDB'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=58016;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute(
"SELECT TOP 5 even_id FROM GDB_TV.sde.Event")
row = cursor.fetchone()
if row:
    print (row)
'''

#conn = pyodbc.connect(r'DSN=GDB;UID=user_gdbt_cns;PWD=necofI2017')

def getSeiscomEvents(fechaInit, fechaEnd, name):
	consulta = []

	cnxn = pyodbc.connect(
	    r'DRIVER={ODBC Driver 11 for SQL Server};'
	    r'SERVER=SRVBDDGDB.igepn.edu.ec\MSSQLGDB;'
	    r'DATABASE=GDB_TV;'
	    r'UID=user_gdbt_cns;'
	    r'PWD=necofI2017'
	    )

	cursor = cnxn.cursor()
	cursor.execute("SELECT DISTINCT E.even_id, E.even_publicID_po, O.time_value, O.magnitude_value_M, E.even_type, '**' AS AP, AP.apic_id, AP.time_value, AP.waveformID_stationCode FROM GDB_TV.sde.Origin O JOIN GDB_TV.sde.Event E ON O.even_id = E.even_id AND O.time_value BETWEEN '" + fechaInit + "' AND '" + fechaEnd + "' JOIN GDB_TV.sde.Arrival_Pick AP ON O.orig_id = AP.orig_id AND AP.waveformID_stationCode IN   ('"+ name +"') ORDER BY E.even_id")

	rows = cursor.fetchall()
	for row in rows:
	    consulta.append(row)

	return consulta

testing1 = getSeiscomEvents('2017-01-24 00:00:00.000','2017-01-25 00:00:00.000', 'CAYR')

for x in testing1:
	print(x)
