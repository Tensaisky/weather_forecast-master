import requests
import json

url='http://www.weather.com.cn/weathern/101021700.shtml'
headers = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Mobile Safari/537.36'
}
response=requests.get(url, headers=headers)
response.encoding='utf-8'
html = response.text
start1 = html.find('var hour3data=[')
start2 = start1 + 16
end = start2 + 1631
hour24_data = html[start2:end]
list1 = hour24_data.split('},')
# 字符串转成列表
data24 = []
for index in range(24):
    if index != 23:
        data24.append(list1[index]+"}")
    if index == 23:
        data24.append(list1[23])
# 字符串转成词典
data24_dict_list = []
for index in range(24):
    data24_dict = json.loads(data24[index])
    # print(data24_dict)
    data24_dict_list.append(data24_dict)
print('   时间    温度')
for index in range(24):
    print('%s %s'%(data24_dict_list[index]['jf'],data24_dict_list[index]['jb']))