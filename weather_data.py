# 未来的预测温度和过去的温度数据，但是过去数据不好处理，没有很好的过去时间识别方法
import requests
import json
import xlsxwriter

# 101021700为杨浦区代码
url='http://www.weather.com.cn/weather1dn/101021700.shtml'
headers = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Mobile Safari/537.36'
}
response=requests.get(url, headers=headers)
response.encoding='utf-8'
html = response.text

# 得到预测的温度,预测温度白天大概预测8点到明天7点，下午4点过后数据是晚上8点到明天7点
# 找到数据起始点，截取出网页完整数据
start1 = html.find('var hour3data=[')
# print(len('var hour3data=['))
start2 = start1 + 16
# print(start2)
end = start2 + 1700
# print(end)
hour24_data = html[start2:end]
hour24_data = hour24_data.split('],')[0]
# 分割出各组json，后面填上'}'，转成完整json格式
list1 = hour24_data.split('},')
# 字符串转成列表
data24 = []
length_data = len(list1)
for index in range(length_data):
    if index != length_data-1:
        data24.append(list1[index]+"}")
    if index == length_data-1:
        data24.append(list1[length_data-1])
# 字符串转成词典，列表存储了24个字典，jf为时间，jb为温度
data24_dict_list = []
for index in range(length_data):
    data24_dict = json.loads(data24[index])
    # print(data24_dict)
    data24_dict_list.append(data24_dict)
print(data24_dict_list)
# print('   时间    温度')
# for index in range(len(list1)):
#     print('%s %s'%(data24_dict_list[index]['jf'],data24_dict_list[index]['jb']))

# 得到过去24小时数据
start_over24 = html.find('observe24h_data = ')
start_over24 = start_over24 + 18
end_over24 = start_over24 + 2500
over24_data = html[start_over24:end_over24]
over24_data = over24_data.split('}};')[0] + '}}'
# over24_data为完整数据，其中有些信息无用
# 截取今天日期
data_time = over24_data.split('","od1')[0]
data_time = data_time.split('od0":"')[1]
data_time = data_time[0:8]
# 截取每小时数据，over24_data过去每个小时所有信息，
data_over24data = over24_data.split('"od1":"","od2":[')[1]
over24_data = data_over24data.split(']}')[0]
# 字符串转成列表
list_over24_data = over24_data.split('},')
data24_over24 = []
length_data_over24 = len(list_over24_data)
for index in range(length_data_over24):
    if index != length_data_over24-1:
        data24_over24.append(list_over24_data[index]+"}")
    if index == length_data_over24-1:
        data24_over24.append(list_over24_data[length_data_over24-1])
# 字符串转成词典
data24_over24_dict_list = []
for index in range(length_data_over24):
    data24_over24_dict = json.loads(data24_over24[index])
    # print(data24_dict)
    data24_over24_dict_list.append(data24_over24_dict)
# 列表内含词典，通过index和key
# od21时间（只有几点信息）,od22气温,od25风力,od27相对湿度
print(data24_over24_dict_list)
# 这里只含有小时，不含日期列表下标越小，代表越近时间，因为昨天和今天有相同小时，所以需要区分
# 先找出0时刻下标，小于该下标为今天日期，大于该下标为昨日日期
# data_time = int(data_time) - 1
# data_time = str(data_time)