# Cagongjoke-DRF
[BACKEND] A website where you can easily find information about cafes for the Cagong people

❖ library ❖

- requirements.txt참고

실행방법

1. 로컬
  ```
  python manage.py runserver
  ```

2. 도커
  ```
  docker compose up --build -d
  ```

3. 초기 로컬 세팅
   
  데이터베이스 스키마를 맞추고, 초기 데이터를 로드합니다.
  ```
  ./run migrate
  ./run load-dataset
  ```
  Superuser를 생성하고, Google 소셜앱 생성 및 사이트 생성, 연결을 합니다.
  ```
  ./run initial_settings
  ```

## Git Convention

| 태그 이름 |                         설명                          |
| :-------: | :---------------------------------------------------: |
|   Feat    |              새로운 기능을 추가하는 경우              |
|    Fix    |                   버그를 고친 경우                    |
|   Style   | 코드 포맷 변경, 세미 콜론 누락, 코드 수정이 없는 경우 |
| Refactor  |         리팩토링 (코드 및 환경변수 설정 변경)         |
|  Comment  |               필요한 주석 추가 및 변경                |
|   Docs    |                  문서를 수정한 경우                   |
|  Rename   |  파일 혹은 폴더명을 수정하거나 옮기는 작업만인 경우   |
|  Remove   |          파일을 삭제하는 작업만 수행한 경우           |


## Docs
- DB Schema
  - [DB Schema Google Docs Link](https://docs.google.com/spreadsheets/d/1EEiiEO7KGeMH0MVtWZn8n6Bga3IoATPCZ8WUFlflurA/edit#gid=0)
