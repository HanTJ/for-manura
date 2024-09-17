안드로이드에서 광고창이 나오면 adb 를 이용해 클릭 이벤트를 발생시켜줍니다.

# 사용방법
1. git clone 이 프로젝트 
2. cd for-manura
3. capture 폴더 생성
4. python 설치 ( 개발 환경 3.10.6 )
5. venv 생성 ( python -m venv .venv )
6. 모듈 설치 ( pip install -r requirements.txt )
7. 안드로이드 sdk 설치
8. 소스에 안드로이드 sdk 내 adb 위치 설정 ( main.py )
9. 안드로이드폰을 usb 디버깅 가능하게 설정 ( 개발자모드 , usb 디버깅 온 )
10. venv 환경으로 진입후 python main.py 로 실행!

# 운영 주의 사항
## capture 폴더에 화면 스샷이 30초마다 찍히고, 찾을경우 네모 표시 
## capture 폴더는 주기적으로 삭제 필요
## 닫기 버튼을 못찾는 경우, shapes 폴더에 x_shapeXX.png 이름으로 이미지를 넣으면 추가적으로 검색해서 닫기 버튼 누름
