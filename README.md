# 할리스 매장 위치 마커 찍기


### -사용한 라이브러리 및 API
<br/>

1. 환경 변수를 위한 라이브러리, 모듈
    * os, load_dotenv
2. 크롤링 & 파싱을 위한 라이브러리, 모듈
    * requests, BeautifulSoup, urllib.request
3. 지오코딩을 위한 API, 라이브러리
    * 네이버 Map API, json
4. 지도를 위한 라이브러리
    * folium


<br/>
<br/>

### - 함수 설명
<br/>

1. 할리스 매장 주소 크롤링 해오기 - make_address_list()
2. 네이버 Map API를 이용하여 주소 gecoding 하기 - geocoding(addr)
3. 주소 리스트에 대한 경도, 위도 리스트 얻기 - get_lon_lat(addr_list)
4. 경도, 위도 리스트로 지도에 마커 찍기 - marking(hollys_map, x, y)

<br/>  
<br/>

![default](/result.PNG)