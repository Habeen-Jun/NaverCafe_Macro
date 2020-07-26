매크로 프로그램 아키텍쳐

# ui shell
ui files:
    macro0704.ui
    login.ui
    naverlogin.ui
# Gui 상 시그널 슬롯 연결 
window files:
    mainwindow.py
    loginwindow.py
    naverloginwindow.py
# 브라우저에서 실제 동작하는 클래스 
execution files:
    main.py
    login.py
    naverlogin.py



https://youtu.be/CPoqmHBxpr4


사용 라이브러리
selenium
bs4
schedule
sqlite

참고하기 좋은 예제 
https://freeprog.tistory.com/333

threading 
https://coding-yoon.tistory.com/45

1. Qt designer 사용 ui 제작
2. sqlite db 설계 (pk?)
3. schedule 모듈 사용 
4. login


주요 요구 사항

1. 이미지 처리?? success!!! 
2. 본문내용 (html로 넣기)
3. 작업 스케쥴링 
4. 


7/15
1. 디테일 작업 (등록시 예외 처리, 옵션 지정)
2. 스케줄링 (스레드 처리로 GUI freeze 현상 방지) 
3. 카테고리 콤보박스 생성
