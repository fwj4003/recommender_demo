import MySQLdb
import json
import time
try:
	st=time.time()
	con = MySQLdb.connect(host='127.0.0.1',user='root',passwd='pikachu',db='douban',port=3306,charset="utf8")
	cur = con.cursor()
	cur.execute('select * from rate')
	data = cur.fetchall()
	for i in data:
		cur.execute('insert into rates (aid,score) values(%s,%s)',(i[0],i[1]+(500-len(i[1]))*'0'))
	cur.close()
	con.commit()
	con.close()
	print time.time()-st
except MySQLdb.Error,e:
	print "Mysql Error %d: %s" % (e.args[0],e.args[1])