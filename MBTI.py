# -*- coding:utf-8 -*-

# Flask : 가볍게 쓰기 좋음
from flask.app import Flask
from flask import request
from flask.helpers import make_response
from flask.json import jsonify

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer # 자연어 처리(특정 단어가 몇번 나오는지)
from sklearn.svm import LinearSVC # 경계선 (마진을 기준)으로 분류
from sklearn.pipeline import Pipeline
import pickle
import os.path

import urllib # http 파라메터 값 한글 디코드 하려고 사용
import googletrans # 구글 번역기
translator = googletrans.Translator()

data_dir ='~/python/'
train = pd.read_csv(os.path.join(data_dir, 'MBTItrain.csv'), encoding='utf-8', header=None, names=['posts', 'type'])
# train = train.sample(frac=0.30) # 임시
# print(train.shape, test.shape)
train.head()


# 이미 만들어진 모델이 있어서 재생성해야하는지 여부를 지정
recreate_model=False
 
# 해당 이름의 모델 파일이 있다면 모델 학습을 수행하지 않음
filename = 'mbti_test.sav'
 
# 만약 모델이 존재하지 않는다면 모델을 재생성
if not os.path.isfile(filename):
    recreate_model=True
 
X = train['posts'] # data
y = train['type']  # labels
# 데이타를 8:2 로 분할
# test_size=0.2는 20% 테스트 데이터로 분류
# random_state=42는 다시 학습시킬때도 같을걸 학습시키도록 기준 정하기
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
 
# 모델 재생성 여부 확인
if recreate_model:    
     
    # vectorizer 정의 및 fit_transform
    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)
     
    # 훈련
    clf = LinearSVC()
    clf.fit(X_train_tfidf, y_train)
     
    # vectorizer 및 모델 파이프라인
    text_clf = Pipeline([('tfidf',TfidfVectorizer()),('clf',LinearSVC())])
    text_clf.fit(X_train, y_train)
     
    # 모델 저장
    pickle.dump(text_clf, open(filename, 'wb'))
 
# 모델 재생성하지 않으면 기존 저장된 모델 불러오기
else:
    # loading the model from disk
    text_clf = pickle.load(open(filename, 'rb'))
     
# 검증
# predictions = text_clf.predict(X_test)
# print(classification_report(y_test, predictions))
# print(f"Overall accuracy of the model: {round(metrics.accuracy_score(y_test, predictions),10)}")

# WAS---------------------------------------------------------------------------------------------------------
app = Flask(__name__)
@app.route("/mbtiTest")
def mbtiTest():
    text = request.args.get("text")
    text = urllib.parse.unquote(text)
    outStr = translator.translate(text, dest='en',src='auto')
    text = f"{outStr.text}"
    data=[text]
    
    predictions = text_clf.predict(data)
    print(predictions)
    db = {"result": predictions[0]}
    data = []
    data.append(db)
     
    finalData = {"data": data}

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
    app.run("0.0.0.0", 1541, debug=True)