# 🛰️ Python Socket Server Project

클라이언트의 **요청을 확인**하고, 요청 데이터를 **저장**하며, **멀티파트(Multipart)** 형식으로 전송된 이미지를 **추출/저장**하는 학습용 **Python Socket Server** 프로젝트입니다.


## 📂 프로젝트 구성

- 프로젝트의 주요 파일 및 디렉토리 구조는 다음과 같습니다.

```bash
Python-Socket-Server/
├── socketServer.py         # 메인 서버 프로그램
├── response.bin            # 서버 응답 파일 (클라이언트에 고정된 응답 반환용)
├── request/                # 클라이언트 요청 원본 데이터 저장 폴더
│   └── YYYY-MM-DD-HH-MM-SS.bin
├── images/                 # 멀티파트 형식으로 전송된 이미지 추출/저장 폴더
└── README.md               # 프로젝트 문서 (지금 보고 계신 파일)
```


## ⚙️ 프로그램 설치방법

### 1. Python 버전 확인

- Python 3.x 버전이 설치되어 있는지 확인합니다.

```bash
python --version
```

### 2. 프로젝트 클론
GitHub에서 프로젝트를 로컬로 복제합니다.

```Bash
git clone https://github.com/seohyunlee-coding/Python-Socket-Server
cd Python-Socket-Server
```


## 🚀 프로그램 사용법
### 1. 서버 실행
- 터미널에서 메인 서버 프로그램을 실행합니다.

```Bash
python socketServer.py
```
- → 127.0.0.1:8000 에서 서버가 실행됩니다.

### 2. 클라이언트 요청 (예: curl)
- 아래 curl 명령어를 사용하여 멀티파트(Multipart) 형식으로 데이터와 이미지를 포함한 POST 요청을 서버로 전송합니다.

```Bash
curl -X POST -S -H "Authorization: JWT b181ce4155b7413ebd1d86f1379151a7e035f8bd" -H "Accept: application/json" -F "author=1" -F "title=curl 테스트" -F "text=API curl로 작성된 AP 테스트 입력 입니다." -F "created_date=2024-06-10T18:34:00+09:00" -F "published_date=2024-06-10T18:34:00+09:00" -F "image=@C:/Users/dev/Desktop/cat-323262_1280.jpg;type=image/jpg" http://127.0.0.1:8000/api_root/Post/
```

### 3. 결과 확인
- 서버가 요청을 받은 후 다음 위치에 파일이 저장됨
- request/ 폴더: 클라이언트 요청의 원본 데이터가 .bin 형식으로 저장
- images/ 폴더: 전송된 이미지 파일이 추출되어 저장



## 🛠️ 사용한 기술
- Python 3.x
- Socket 프로그래밍
- curl (클라이언트 요청 전송)
- Windows PowerShell (실행 환경)



## 🐛 버그 및 디버그 팁
- 데이터 형식: 요청 데이터 저장은 바이너리 형식(.bin)으로 이루어짐
- 이미지 손상: 멀티파트 처리 시 HTTP 헤더 파싱이나 바운더리(Boundary) 처리가 제대로 안 될 경우 이미지가 손상될 수 있음


## 📚 참고 및 출처
- Python 공식 문서: https://docs.python.org/3/library/socket.html
- curl 공식 문서: https://curl.se/docs/


## 👨‍💻 프로그래머 정보
- 이름: 이서현
- 이메일: cwijiq3085@gmail.com
- GitHub: seohyunlee-coding
