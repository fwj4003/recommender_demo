import MySQLdb
import json
try:
	f=file("drama.json")
	obj=json.load(f)
	con = MySQLdb.connect(host='127.0.0.1',user='root',passwd='pikachu',db='douban',port=3306,charset="utf8")
	cur = con.cursor()
	drama=[]
	for data in obj:
		drama.append((data['id'],data['title'],data['url'],data['cover'],data['rate']))
	cur.executemany('insert into all_drama values(%s,%s,%s,%s,%s)',drama)
	cur.close()
	con.commit()
	con.close()
except MySQLdb.Error,e:
	print "Mysql Error %d: %s" % (e.args[0],e.args[1])


