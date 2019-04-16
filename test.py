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
# print(start1)
# print(len('var hour3data=['))
start2 = start1 + 16
# print(start2)
# print(len('[{"jc":"0","jb":"15","je":"63","jd":"3","jf":"2019041608","ja":"02"},{"jc":"0","jb":"15","je":"66","jd":"4","jf":"2019041609","ja":"07"},{"jc":"0","jb":"15","je":"69","jd":"4","jf":"2019041610","ja":"07"},{"jc":"0","jb":"16","je":"72","jd":"4","jf":"2019041611","ja":"07"},{"jc":"0","jb":"17","je":"72","jd":"4","jf":"2019041612","ja":"07"},{"jc":"0","jb":"18","je":"73","jd":"4","jf":"2019041613","ja":"07"},{"jc":"0","jb":"18","je":"73","jd":"4","jf":"2019041614","ja":"07"},{"jc":"0","jb":"18","je":"73","jd":"4","jf":"2019041615","ja":"07"},{"jc":"0","jb":"17","je":"74","jd":"4","jf":"2019041616","ja":"01"},{"jc":"0","jb":"16","je":"74","jd":"4","jf":"2019041617","ja":"07"},{"jc":"0","jb":"16","je":"76","jd":"4","jf":"2019041618","ja":"01"},{"jc":"0","jb":"15","je":"79","jd":"4","jf":"2019041619","ja":"01"},{"jc":"0","jb":"15","je":"81","jd":"4","jf":"2019041620","ja":"01"},{"jc":"0","jb":"14","je":"82","jd":"4","jf":"2019041621","ja":"01"},{"jc":"0","jb":"13","je":"84","jd":"4","jf":"2019041622","ja":"01"},{"jc":"0","jb":"14","je":"85","jd":"4","jf":"2019041623","ja":"00"},{"jc":"0","jb":"14","je":"84","jd":"4","jf":"2019041700","ja":"00"},{"jc":"0","jb":"14","je":"84","jd":"4","jf":"2019041701","ja":"00"},{"jc":"0","jb":"13","je":"84","jd":"4","jf":"2019041702","ja":"00"},{"jc":"0","jb":"13","je":"83","jd":"4","jf":"2019041703","ja":"00"},{"jc":"0","jb":"14","je":"82","jd":"4","jf":"2019041704","ja":"00"},{"jc":"0","jb":"14","je":"82","jd":"4","jf":"2019041705","ja":"00"},{"jc":"0","jb":"14","je":"81","jd":"4","jf":"2019041706","ja":"00"},{"jc":"0","jb":"14","je":"80","jd":"4","jf":"2019041707","ja":"00"}]'))
end = start2 + 1631
# print(end)
hour24_data = html[start2:end]
list1 = hour24_data.split('},')
data24 = []
for index in range(24):
    if index != 23:
        data24.append(list1[index]+"}")
    if index == 23:
        data24.append(list1[23])
data24_dict_list = []
for index in range(24):
    data24_dict = json.loads(data24[index])
    # print(data24_dict)
    data24_dict_list.append(data24_dict)
print('   时间    温度')
for index in range(24):
    print('%s %s'%(data24_dict_list[index]['jf'],data24_dict_list[index]['jb']))