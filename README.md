# django-myapp 프로젝트 환경 설정
### 1. 프로젝트 클론하기
```
$ git clone https://github.com/DE4-Team2-1PJ/django-myapp.git
$ cd django-myapp
```
### 2. 가상 환경 설정
가상 환경을 설정하려면, 아래 명령어를 사용하여 가상 환경을 생성하고 활성화하세요.
#### Windows (cmd) 의 경우
```
$ python -m venv venv
$ venv\Scripts\activate
```
#### Windows (PowerShell) 의 경우
```
$ python -m venv venv
$ .\venv\Scripts\Activate
```
#### Mac/Linux 의 경우
```
$ python3 -m venv venv
$ source venv/bin/activate
```

### 3. 필수 패키지 설치
requirements.txt에 명시된 모든 패키지를 설치하려면, 아래 명령어를 입력하세요 (가상환경에 설치하세요):
```
$ pip install -r requirements.txt
```

### 4. 데이터베이스 마이그레이션
데이터베이스 테이블을 생성하려면 다음 명령어를 실행하세요 (가상환경에서 하세요):
```
$ python manage.py migrate
```
### 5. 서버 실행
프로젝트 서버를 실행하려면, 아래 명령어를 입력하세요 (가상환경에서 하세요):
```
$ python manage.py runserver
```

### 6. 브라우저에서 페이지 확인
브라우저에서 http://127.0.0.1:8000/recruits 접속
![image](https://github.com/user-attachments/assets/97d828c3-afbb-4fc5-975b-d26963b90082)

