0. capstone_UI 기술스택
    언어 : (파이썬)98% + (자바스크립트 + css)2%
    사용한 라이브러리 : Dash + Plotly
    이 프로그램의 용도 : 학습자의 비대면 학습의 집중도를 측정, 기록하여 스스로에게 학습을 유도시킬수 있는 웹서비스


1. 폴더 구조 
    capstone_UI
    ├── __pycache__
    ├── assets
    │   ├── photo
    │   └── test_Video
    └── src
        ├── __pycache__
        ├── datastroage
        │   └── __pycache__
        ├── model_api
        │   ├── __pycache__
        │   └── model
        ├── pages
        │   └── __pycache__
        └── web_function
            └── __pycache__


2. 폴더 역할
    ** __pycache__ 폴더는 import 사용시 자동생성되는 폴더

    a. assets : JS, css 파일들 및 이미지, 영상 등 서비스에 필요한 리소스 파일들 디렉토리 <- Dash 라이브러리의 기본 문법. 꼭 해당폴더 위치를 지킬것
    b. src : 웹서비스가 작동하게 만드는 소스파일들 디렉토리
        src 내부디렉토리
            - datastroage : 실시간 집중도 결과를 메모리에 저장하는 역할
            - model_api : 웹캠에서 받은 사진을 통해 집중도 결과를 추출해주는 역할
            - pages : 클라이언트 화면을 보여주는 역할
            - web_function : 구간별 집중도에 따른 집중, 비집중 등을 판별하고 이를 기록 및 화면으로 보여주는 역할


3. 실행방법
    1. app_activate.py 파일 실행함 
    2. 30초 ~ 1분 뒤에 터미널에 인터넷 주소창이 출력됨
    3. 이 주소창으로 인터넷에 접속하면 웹 서비스 사용