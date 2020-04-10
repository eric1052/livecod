import requests
import re
from bs4 import BeautifulSoup
import json
from previousWorldData import previous_data
import os

# 대륙이름 삭제 
def remove_continent(lst_of_dic, continent):
    lst_of_dic = list(filter(lambda x: x['Name']!= continent, lst_of_dic))
    return lst_of_dic

# 세계 데이터 크롤링 함수
def get_data(datas):

    world_confirmed = []

    for d in datas:
        country = d.find_all('td')[0].text
        if country.strip() == 'S. Korea':
            continue
        confirmed = d.find_all('td')[1].text
        deaths = d.find_all('td')[3].text
        recovered = d.find_all('td')[5].text

        # test code : print("strip data : \t",country\t, confirmed\t, deaths\t, recovered)

        country_kr = ''
        country_cn = ''

        for value in previous_data:
            if value['Name_en'] == country.strip():
                country_kr = value['Name']
                name_ch = value['Name_ch']

        #지도 SVG 이름 동기화(아래 USA는 크롤링된 영어이름)
        if country.strip() == 'USA':
            #여기에 SVG파일에 있는 국가명으로 변경
            country = 'United States'

        #잘못된 영어이름 수정
        if country.strip() == 'USA':
            #여기에 SVG파일에 있는 국가명으로 변경
            country = 'United States'

        if country.strip() == 'Total:':
          print("Skipping total")
          continue

        #한국어 이름이 필드에 없을 경우 영어이름 삽입
        if country_kr == '':
            country_kr = country.strip()

        world_confirmed.append({
            'Name' : country_kr,
            'Name_ch' : country_cn,
            'Name_en' : country.strip(),
            '확진자수' : int(0 if confirmed.strip().replace(',', '') == "" else confirmed.strip().replace(',', '')),
            '사망자수' : int(0 if deaths.strip().replace(',', '') == "" else deaths.strip().replace(',', '')),
            '완치자수' : int(0 if recovered.strip().replace(',', '') == "" else recovered.strip().replace(',', '')),
        })

    #대륙이름 필터링  
    world_confirmed = remove_continent(world_confirmed, 'North America')
    world_confirmed = remove_continent(world_confirmed, 'Europe')
    world_confirmed = remove_continent(world_confirmed, 'Asia')
    world_confirmed = remove_continent(world_confirmed, 'South America')
    world_confirmed = remove_continent(world_confirmed, 'Oceania')
    world_confirmed = remove_continent(world_confirmed, 'Africa')
    world_confirmed = remove_continent(world_confirmed, 'World')
    world_confirmed = remove_continent(world_confirmed, '')

    return world_confirmed

# 받아온 세계 현황 js로 내보내는 함수

import requests
import re
from bs4 import BeautifulSoup
import json
from previousWorldData import previous_data
import os

# 대륙이름 삭제 
def remove_continent(lst_of_dic, continent):
    lst_of_dic = list(filter(lambda x: x['Name']!= continent, lst_of_dic))
    return lst_of_dic

# 세계 데이터 크롤링 함수
def get_data(datas):

    world_confirmed = []

    for d in datas:
        country = d.find_all('td')[0].text
        if country.strip() == 'S. Korea':
            continue
        confirmed = d.find_all('td')[1].text
        deaths = d.find_all('td')[3].text
        recovered = d.find_all('td')[5].text

        # test code : print("strip data : \t",country\t, confirmed\t, deaths\t, recovered)

        country_kr = ''
        country_cn = ''

        for value in previous_data:
            if value['Name_en'] == country.strip():
                country_kr = value['Name']
                name_ch = value['Name_ch']

        #지도 SVG 이름 동기화(아래 USA는 크롤링된 영어이름)
        if country.strip() == 'USA':
            #여기에 SVG파일에 있는 국가명으로 변경
            country = 'United States'

        #잘못된 영어이름 수정
        if country.strip() == 'USA':
            #여기에 SVG파일에 있는 국가명으로 변경
            country = 'United States'

        if country.strip() == 'Total:':
          print("Skipping total")
          continue

        #한국어 이름이 필드에 없을 경우 영어이름 삽입
        if country_kr == '':
            country_kr = country.strip()

        world_confirmed.append({
            'Name' : country_kr,
            'Name_ch' : country_cn,
            'Name_en' : country.strip(),
            '확진자수' : int(0 if confirmed.strip().replace(',', '') == "" else confirmed.strip().replace(',', '')),
            '사망자수' : int(0 if deaths.strip().replace(',', '') == "" else deaths.strip().replace(',', '')),
            '완치자수' : int(0 if recovered.strip().replace(',', '') == "" else recovered.strip().replace(',', '')),
        })

    #대륙이름 필터링  
    world_confirmed = remove_continent(world_confirmed, 'North America')
    world_confirmed = remove_continent(world_confirmed, 'Europe')
    world_confirmed = remove_continent(world_confirmed, 'Asia')
    world_confirmed = remove_continent(world_confirmed, 'South America')
    world_confirmed = remove_continent(world_confirmed, 'Oceania')
    world_confirmed = remove_continent(world_confirmed, 'Africa')
    world_confirmed = remove_continent(world_confirmed, 'World')
    world_confirmed = remove_continent(world_confirmed, '')

    return world_confirmed

# 받아온 세계 현황 js로 내보내는 함수

def write_data(world_confirmed):
    # cur_path = os.getcwd()       # test code for Windows

    with open("./data/worldData.js", "w", encoding='UTF-8-sig') as json_file:
    # with open(cur_path+"\worldData.js", "w", encoding='UTF-8-sig') as json_file:      # test code for Windows
        json.dump(world_confirmed, json_file, ensure_ascii=False, indent=4)
        # file.write(json.dumps(dict, ensure_ascii=False))

    data = ''

    with open("./data/worldData.js", "r", encoding='UTF-8-sig') as f:
    # with open(cur_path+"\worldData.js", "r", encoding='UTF-8-sig') as f:      # test code for Windows
        while True:
            line = f.readline()
            if not line: break
            data += line
    data = '//Auto-generated by crawlWorldData.py\nvar marker = ' + data + ';'

    with open("./data/worldData.js", "w", encoding='UTF-8-sig') as f_write:
    # with open(cur_path+"\worldData.js", "w", encoding='UTF-8-sig') as f_write:        # test code for Windows
        f_write.write(data)


if __name__ == "__main__":
    print("#####################################")
    print("############ 세계 데이터 #############")
    print("######## worldData.js #########")

    html = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.select('#main_table_countries_today > tbody > tr')

    world_confirmed = get_data(datas)
    write_data(world_confirmed)

    print("############### 완료!! ###############")
    print("#####################################")