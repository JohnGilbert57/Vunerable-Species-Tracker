from django.db import connection

def db_query(sql,bind_variables = []):
	cursor=connection.cursor()
	cursor.execute(sql,bind_variables)
	rows = cursor.fetchall()
	return rows
