# -*- coding:utf-8 -*-

# Flask : 가볍게 쓰기 좋음
from flask.app import Flask
from flask import request
from flask.helpers import make_response
from flask.json import jsonify
from cx_Oracle import connect

# 리눅스에서 파이썬 한글처리 (한글처리해야 한글가능)
from os import environ
environ["NLS_LANG"] = ".AL32UTF8"

app = Flask(__name__)
@app.route("/ddabong")
def boardDdabong():
    bd_b_no = request.args.get("boardNo")
    bd_m_id = request.args.get("userID")
    first = request.args.get("first")
    ddabong = request.args.get("ddabong")
    
    con, cur = None, None
    try:
        con = connect("sollind/end1128@192.168.0.126:1521/xe")
        if first == "first":
            # 하 프로그램상 늦어서 연속으로 여러번 들어오면 같은이름의 따봉이 여러개 생겨서 오류남
            # 그래서 이미 있는지 확인하고 해야되는데 하....
            cur = con.cursor()
             
            # sql문 전송
            cur.execute("select count(*)from Board_ddabong where bd_b_no = "+bd_b_no+" and bd_m_id = '"+bd_m_id+"'")
            check = None
            for data in cur:
                check = data[0]
            if check != 0:
                sql = "delete from BOARD_DDABONG where bd_b_no = "+bd_b_no+" and bd_m_id = '" + bd_m_id + "'"
            else:
                sql = "insert into Board_ddabong values(Board_ddabong_seq.nextval, 1," + bd_b_no + ", '" + bd_m_id + "')"
        else:
            sql = "update Board_ddabong set bd_ddabong = " + ddabong + " where bd_no = " + first
            
        sql2 = "update Board set b_ddabong = ("
        sql2 += "select count(*) from Board_ddabong where bd_b_no = "+bd_b_no+" and bd_ddabong = 1"
        sql2 += ") where b_no = " + bd_b_no
        # db작업 총괄 객체
        cur = con.cursor()
         
        # sql문 전송
        cur.execute(sql)
        con.commit()
        
        # db작업 총괄 객체
        cur = con.cursor()
         
        # sql문 전송
        cur.execute(sql2)
        con.commit()
        
        db = {"result": "success"}
        data = []
        data.append(db)
    except Exception as e:
        print(e)
        db = {"result": "fail"}
        data = []
        data.append(db)
    cur.close
    con.close()
     
    finalData = {"data": data}
    # 줄때 jsonify 사용
    json = jsonify(finalData)
    resBody = make_response(json)
     
    # 누구나 가져갈수 있게 크로스 도메인
    resHeader = {"Access-Control-Allow-Origin":"*"}
    return resBody, resHeader

@app.route("/getSearchBoard")
def getSearchBoard():
    b_search = request.args.get("b_search");
    b_type = request.args.get("b_type");
    if b_type == "전체":
        b_type = ""
        
    data = []
    con, cur = None, None;
    try:
        con = connect("sollind/end1128@192.168.0.126:1521/xe")
        sql = "select * from Board "
        sql += "where (UPPER(b_title) like UPPER('%" + b_search + "%') or UPPER(b_txt) like UPPER('%" + b_search + "%')) and b_type like '%"+b_type+"%' "
        sql += "order by b_date desc"
        
        cur = con.cursor()
        
        cur.execute(sql)
        
        db = {}
        
        for b_no, b_type, b_title, b_txt, b_m_id, b_date, b_img, b_ddabong in cur:
            db = {"b_no": b_no, "b_type": b_type, "b_title": b_title, "b_txt": b_txt, "b_m_id": b_m_id, "b_date": b_date, "b_img": b_img, "b_ddabong": b_ddabong}
            data.append(db)
    except Exception as e:
        print(e)
        db = {"result": "fail"}
        data.append(db)
    cur.close
    con.close()
    
    finalData = {"data": data}
    json = jsonify(finalData)
    resBody = make_response(json)
    
    resHeader = {"Access-Control-Allow-Origin":"*"}
    return resBody, resHeader

@app.route("/getBoardData")
def getBoardData():
    b_no = request.args.get("b_no")
    num = int(request.args.get("num"))
    b_type = request.args.get("type")
    if b_type == "전체":
        b_type = ""

    data = []
    con, cur = None, None
    try:
        con = connect("sollind/end1128@192.168.0.126:1521/xe")
        sql="select * "
        sql+="from ("
        sql+="select rownum as rn, b_no, b_type, b_title, b_txt, b_m_id, b_date, b_img , b_ddabong "
        sql+="from ("
        sql+="select * from Board where b_no <= "+b_no+" and b_type like '%"+b_type+"%' order by b_date desc"
        sql+=")"
        sql+=")"
        sql+="where rn >= "+str(num*10+1)+" and rn <= "+str(num*10+10)
        # db작업 총괄 객체
        cur = con.cursor()
         
        # sql문 전송
        cur.execute(sql)
        
        db = {}
        db2 = {}
        count = 1
        lastNum = 0
        for rn, no, boardType, title, txt, ID, date, img, b_ddabong in cur:
            if count%2==1:
                db = {"rn": rn, "b_no": no, "b_type": boardType, "b_title": title, "b_txt": txt, "b_m_id": ID, "b_date": date, "b_img": img, "b_ddabong": b_ddabong}
            else:
                db2 = {"rn2": rn, "b_no2": no, "b_type2": boardType, "b_title2": title, "b_txt2": txt, "b_m_id2": ID, "b_date2": date, "b_img2": img, "b_ddabong2": b_ddabong}
                db.update(db2)
                data.append(db)
            count += 1
            lastNum += 1
        if lastNum%2==1:
            data.append(db)
    except Exception as e:
        print(e)
        data = []
        db = {"result": "fail"}
        data.append(db)
    cur.close
    con.close()
     
    finalData = {"data": data}
    # 줄때 jsonify 사용
    json = jsonify(finalData)
    resBody = make_response(json)
     
    # 누구나 가져갈수 있게 크로스 도메인
    resHeader = {"Access-Control-Allow-Origin":"*"}
    return resBody, resHeader

@app.route("/getCompanyInfo")
def getCompanyInfo():
    c_search = request.args.get("c_search")
    data = []
    con, cur = None, None
    try:
        con = connect("sollind/end1128@192.168.0.126:1521/xe")
        sql="select c_no, c_name, c_score, c_logo "
        sql+="from COMPANY "
        sql+="where UPPER(c_name) like UPPER('%" + c_search + "%') "
        sql+="order by c_score"
        
        cur = con.cursor()
         
        cur.execute(sql)
        
        db = {}
        for c_no, c_name, c_score, c_logo in cur:
            db = {"c_no": c_no, "c_name": c_name, "c_score": round(c_score, 1), "c_logo": c_logo}
            data.append(db)
    except Exception as e:
        print(e)
        db = {"result": "fail"}
        data.append(db)
    cur.close
    con.close()
     
    finalData = {"data": data}
    json = jsonify(finalData)
    resBody = make_response(json)
     
    resHeader = {"Access-Control-Allow-Origin":"*"}
    return resBody, resHeader

if __name__ == "__main__":
    # 0.0.0.0은 아무나 192.168.0.138 이렇게 주면 그 주소만 접속가능
    # 7887 포트번호
    # debug=True 콘솔에 로그
    app.run("0.0.0.0", 7887, debug=True)
