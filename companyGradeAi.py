# -*- coding:utf-8 -*-

import pandas as pd
from sklearn.preprocessing._data import MinMaxScaler
from sklearn.cluster._kmeans import KMeans
from sklearn.neighbors._classification import KNeighborsClassifier
import numpy as np

# 리눅스에서 파이썬 한글처리 (한글처리해야 한글가능)
from os import environ
environ["NLS_LANG"] = ".AL32UTF8"

import os.path
data_dir ='/home/sollind/python/'
xData = pd.read_csv(os.path.join(data_dir, 'companyInfoHab.csv'), encoding='utf-8')
xData = xData[["매출액(억원)","영업이익률","순이익률","부채비율","당좌비율","유보율","복지 및 급여","업무와 삶의 균형","사내문화","승진 기회 및 가능성","경영진"]]
# print(xData)
# print(xData.shape)

# 데이터 null값 0으로 바꾸기
name = ["매출액(억원)","영업이익률","순이익률","부채비율","당좌비율","유보율","복지 및 급여","업무와 삶의 균형","사내문화","승진 기회 및 가능성","경영진"]
for i in name:
    xData[i]=xData[i].fillna(0)

# 각각 data와 label의 최대 최소가 다르니까 MinMaxScaler()따로 설정
data_mms = MinMaxScaler()
label_mms = MinMaxScaler()

# trainData 정규화
trainData = data_mms.fit_transform(xData)
# print(trainData)

# label 만들기
# 부채비율은 빼고 나머지는 전부 더해서 정규화
sum = None
count = None
yData = []
for td in trainData:
    sum = 0.0
    count = 0
    for i in td:
        if count == 3:
            sum -= i
        else:
            sum+=i
        count += 1
    yData.append(sum)
# print(yData)
yData = label_mms.fit_transform(pd.DataFrame(yData))
# print(yData)
# print("-----------------")

# 1~5등급으로 label분류
label = []
for y in yData:
    if y <=0.1:
        label.append(10)
    elif 0.1 < y <=0.2:
        label.append(9)
    elif 0.2 < y <=0.3:
        label.append(8)
    elif 0.3 < y <=0.4:
        label.append(7)
    elif 0.4 < y <=0.5:
        label.append(6)
    elif 0.5 < y <=0.6:
        label.append(5)
    elif 0.6 < y <=0.7:
        label.append(4)
    elif 0.7 < y <=0.8:
        label.append(3)
    elif 0.8 < y <=0.9:
        label.append(2)
    else:
        label.append(1)
# print(label)

# KNeighborsClassifier(n_neighbors=5) 가까운 5개(n_neighbors=5)중에 많은거
knc = KNeighborsClassifier(n_neighbors=5)
# 학습
knc.fit(trainData, label)

# # 가까운 k개 각각 테스트
# import matplotlib.pyplot as plt
# ks = range(1,31)
# inertias = []
# for k in ks:
#     model = KMeans(n_clusters=k)
#     model.fit(trainData)
#     inertias.append(model.inertia_)
#     # Plot ks vs inertias
# plt.plot(ks, inertias, '-o')
# plt.xlabel('number of clusters, k')
# plt.ylabel('inertia')
# plt.xticks(ks)
# plt.show()

# # 검증
# test = knc.predict(trainData)
# # print(test)
# count = 0
# for i in range(len(trainData)):
#     if test[i] == label[i]:
#         count += 1
# print("검증 : "+str(count/len(trainData)*100)+"%")

# # 테스트
# predicateData = np.array([[83113,-9.63,-9.80,169.55,58.82,962.02,2.9,3.1,2.6,2.9,2.2]])
# predicateData = data_mms.transform(predicateData)
# result = knc.predict(predicateData)
# print("결과: "+str(result[0]))

# WAS ---------------------------------------------------------------------------------
# Flask : 가볍게 쓰기 좋음
from flask.app import Flask
from flask import request
from flask.helpers import make_response
from flask.json import jsonify

app = Flask(__name__)
@app.route("/companyGrade")
def companyGrade():
    companyData = request.args.get("companyData")
    companyData = companyData.split(",")
    companyData2 = []
    for i in range(len(companyData)):
        companyData2.append(float(companyData[i]))
    predicateData = np.array([companyData2])
    predicateData = data_mms.transform(predicateData)
    result = knc.predict(predicateData)
    
    # float은 안들어감 String이나 int형만 들어가는것 같음
    result2 = {"result": int(result[0])}
    data = []
    data.append(result2)
     
    finalData = {"data": data}
    print(finalData)
    # 줄때 jsonify 사용
    json = jsonify(finalData)
    resBody = make_response(json)
     
    # 누구나 가져갈수 있게 크로스 도메인
    resHeader = {"Access-Control-Allow-Origin":"*"}
    return resBody, resHeader

if __name__ == "__main__":
    # 0.0.0.0은 아무나 192.168.0.138 이렇게 주면 그 주소만 접속가능
    # 7887 포트번호
    # debug=True 콘솔에 로그
    app.run("0.0.0.0", 1743, debug=True)
