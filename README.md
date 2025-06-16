치지직 공식 API 활용하여 데이터 수집 및 분석을 진행해보았습니다.  

해당 github는 예시 query문 생성과 예시 데이터 생성까지 포함하고 있으며, 보안상의 문제로 채팅 분석이나 query문으로 생성된 데이터 2차 시각화 등은 포함하고 있지 않습니다.  


## 코드 다운로드
$ git clone https://github.com/gosaengchung/capstone_project
$ cd capstone_project  

## 패키지 설치
$ pip install -r requirements.txt  

## 네이버 개발자 센터로부터 치지직 API 활용 요청 후 API ID 및 key 저장

## 공식 API를 활용한 실시간 데이터 수집
live_channel.py를 통해 치지직(CHZZK) API로부터 실시간 방송 데이터를 1000개 단위로 수집.  

API 키는 보안을 위해 .gitignore에 포함된 별도의 파일에 저장.  

데이터에는 channelId, channelName, liveId, liveTitle, liveCategory, openDate, concurrentUserCount, tags 등이 포함됨.  

![image](https://github.com/user-attachments/assets/b8be4e8d-cd69-4b90-98d3-db9c04bc8a2c)

## EC2 서버 구축 및 자동화
AWS EC2 인스턴스를 생성하고 cap.pem 키 파일을 통해 접근  

Python 스크립트를 EC2 상에서 주기적으로 실행하기 위해 git bash로 접근  

> https://taetoungs-branch.tistory.com/113 (참고)
> 
crontab을 사용하여 live_channel.py를 1시간마다 run 시킴  

System.out.println("$ 0 * * * * /home/ubuntu/capstone_project/venv/bin/python /home/ubuntu/capstone_project/live_channel.py >> /home/ubuntu/capstone_project/cron_output.log 2>&1")  


# EC2 서버에 수집된 JSON 데이터 로컬로 다운로드
scp 명령어를 통해 EC2 내 저장된 JSON 파일들을 로컬로 다운로드
System.out.println("scp -i cap.pem ubuntu@your-ec2-ip:~/capstone_project/live_cleaned_*.json ~/local_directory/")

# SQLite DB 구성
JSON 데이터를 기반으로 SQLite DB(live_data.db)를 생성하는 db.py
중복된 방송 데이터가 시간대별로 여러 번 수집될 수 있어, live_id와 collected_at을 복합키로 설정하여 동일한 live_id 내에 각기 다른 collected_at(수집시간) 데이터 응집
![image](https://github.com/user-attachments/assets/a1188c7e-005b-4419-8336-756f93f1781b)

# 데이터 분석 및 쿼리
방송별, 채널별, 태그별, 시간대별 분석을 위한 다양한 SQL 쿼리를 작성


