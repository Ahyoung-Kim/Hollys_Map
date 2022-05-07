from http import client
import urllib.request
import folium  # 지도 시각화 라이브러리 
import requests  # 크롤링을 위한 라이브러리 
import json
from bs4 import BeautifulSoup # 크롤링 & 파싱을 위한 라이브러리 
import os  # 환경 변수 접근하기 위한 라이브러리 
from dotenv import load_dotenv  # 환경 변수를 위한 모듈 

# .env 파일에 저장한 환경변수 불러오기 
load_dotenv()
client_id = os.environ.get("CLIENT_ID")
client_key = os.environ.get("CLIENT_KEY")

# 매장 주소 크롤링 
def make_address_list():
  # 할리스 페이지 url
  url_front = 'https://www.hollys.co.kr/store/korea/korStore2.do?pageNo='
  page_num = 11
  url_back = '&sido=&gugun=&store='

  # 매장 주소 리스트 
  addr_list = []

  for i in range(1, page_num):
    url = url_front + str(i) + url_back
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    table = soup.find('table', 'tb_store')
    tbody = table.find('tbody')
    trs = tbody.find_all('tr')

    for tr in trs:
      address = tr.select_one("td:nth-of-type(4) > a").text
      addr_list.append(address)

  return addr_list


# NAVER API 사용해서 주소를 보고 gecoding 하기 
def geocoding(addr):
  # 주소에서 특수 문자를 문자열로 변환
  encText = urllib.parse.quote(str(addr))

  url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query=' + encText
  
  request = urllib.request.Request(url)
  # request를 보낼때 cline_id, cline_key 넘겨줘서 자격얻기
  request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
  request.add_header('X-NCP-APIGW-API-KEY', client_key)

  # 응답 얻기
  response = urllib.request.urlopen(request)
  status = response.getcode()

  if(status == 200):
    body = response.read()
    return body.decode('utf-8')
  else:
    print("Error Code: " + status)


# gecoding 한 결과로 경도, 위도 얻기 
def get_lon_lat(addr_list):
  x = [] #경도 리스트
  y = [] #위도 리스트

  for addr in addr_list:
    geocode = geocoding(addr)
    geocode = json.loads(geocode)

    try:
      lon_lat = geocode['addresses'][0]
      x.append(float(lon_lat['x']))
      y.append(float(lon_lat['y']))
    except IndexError:
      pass
  return x, y


def marking(hollys_map, x, y):
  # 마커 찍기
  for i in range(len(x)):
    folium.Marker([y[i], x[i]], 
      icon=folium.Icon(color='red', icon='star')).add_to(hollys_map)


if __name__ == "__main__" :
  addr_list = make_address_list()
  x_list, y_list = get_lon_lat(addr_list)

  hollys_map = folium.Map(location=[37.4729081, 127.039306])
  marking(hollys_map, x_list, y_list)

  hollys_map.save("hollys.html")