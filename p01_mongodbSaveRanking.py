# -*- coding:utf-8 -*-
from pymongo.mongo_client import MongoClient
from cx_Oracle import connect
from time import sleep
from http.client import HTTPConnection # 이클립스 버그, 오류아님
from xml.etree.ElementTree import fromstring

oCon = connect("sollind/end1128@192.168.0.126:1521/xe")
mCon = MongoClient("192.168.0.126")
db = mCon.xe
beforeData = db.View_Ranking.find()
for d in beforeData:   
    db.Save_Ranking.insert_one({"vr_c_name":d['vr_c_name'], "vr_c_count":d['vr_c_count']})
    
if  db.View_Ranking.find() != None:
    db.View_Ranking.drop()

sql = "select * from( "
sql+= "select rownum as rn, c_name, c_count "
sql+= "from(select * " 
sql+= "from company order by c_count desc "
sql+= ") "
sql+=") "
sql+="where rn >= 1 and rn <= 10"
cur = oCon.cursor()

cur.execute(sql)

for _, c_name, c_count in cur:
    db.View_Ranking.insert_one({"vr_c_name":c_name, "vr_c_co+unt":c_count})

sleep(10);
db.Save_Ranking.drop();


huc = HTTPConnection("192.168.0.126:7665") # or HTTPConnection

huc.request("GET", "/update")

res = huc.getresponse() # 응답 가져와서
resBody = res.read() # 응답내용

huc.close()
cur.close()
oCon.close()
mCon.close()


