import MySQLdb
import json
import time
def f(x):
	return int(x.encode())>0
try:
	st=time.time()
	con = MySQLdb.connect(host='127.0.0.1',user='root',passwd='pikachu',db='douban',port=3306,charset="utf8")
	cur = con.cursor()
	cur.execute('select * from rate')
	data = cur.fetchall()
	for now in data:
		v=[f(i) for i in now[1]]
		total=sum(v)
		if total<15:
			cur.execute('delete from rate where aid=%s',(now[0],))
			print 'delete one row'
	cur.close()
	con.commit()
	con.close()
	print time.time()-st
except MySQLdb.Error,e:
	print "Mysql Error %d: %s" % (e.args[0],e.args[1])