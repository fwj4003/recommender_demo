import MySQLdb
import json
import time
from sklearn.neighbors import NearestNeighbors
from sklearn import cross_validation
import math

K=20
try:
	st=time.time()
	con = MySQLdb.connect(host='127.0.0.1',user='root',passwd='pikachu',db='douban',port=3306,charset="utf8")
	cur = con.cursor()
	cur.execute('select * from rates')
	data = cur.fetchall()
	v=[]
	for i in data:
		v.append([int(j.encode()) for j in i[2]])
	train,test=cross_validation.train_test_split(v, test_size=0.01, random_state=7)
	neigh = NearestNeighbors(n_neighbors=K,algorithm='kd_tree',metric='minkowski')
	neigh.fit(train)
	recall=[]
	precision=[]
	coverage=[]
	for i in test:
		tmp=neigh.kneighbors(i,return_distance=False)[0]
		me=set()
		you=set()
		for j in range(len(i)):
			if i[j]>3:
				me.add(j)
		r=dict()
		for j in tmp:
			for k in range(len(train[j])):
				if train[j][k]>3:
					if r.get(k)==None:
						r[k]=1
					else:
						r[k]+=1
		res = list(sorted(r, key=r.__getitem__, reverse=True))
		re=set(res[:min(10,len(res))+1])
		## if i rated all the drama less than 3 , the len(me) may equal 0
		recall.append(len(re&me)*1.0/(len(me)+0.001))
		precision.append(len(me&re)*1.0/(len(re)+0.001))
		coverage.append(len(res)/489.0)
		break
	print 'K: %d' % (K)
	print 'Recall: %f' % (sum(recall)/len(recall))
	print 'Precision: %f' % (sum(precision)/len(precision))
	print 'Coverage: %f' % (sum(coverage)/len(coverage))
	
	cur.close()
	con.commit()
	con.close()
	print 'cost time : %f' % (time.time()-st)
except MySQLdb.Error,e:
	print "Mysql Error %d: %s" % (e.args[0],e.args[1])

