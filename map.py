from urllib import response
import folium
import requests
import json
from bs4 import BeautifulSoup

'''url = 'https://www.hollys.co.kr/store/korea/korStore2.do?pageNo=1&sido=&gugun=&store='

res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

table = soup.find('table', 'tb_store')
tbody = table.find('tbody')
trs = tbody.find_all('tr')

for tr in trs:
  address = tr.select_one("td:nth-of-type(4) > a").text
  print(address)'''

# 주소 크롤링 
def make_address_list():
  # 할리스 페이지 url
  url_front = 'https://www.hollys.co.kr/store/korea/korStore2.do?pageNo='
  page_num = 3
  url_back = '&sido=&gugun=&store='
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

addr_list = make_address_list()

for addr in addr_list:
  print(addr)  