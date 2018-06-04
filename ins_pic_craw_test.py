import requests
from bs4 import BeautifulSoup
import re
import json
from lxml import etree



# base_url：当前用户的页面
base_url = 'https://www.instagram.com/nasa/'
var_value = {"id": "", "first": 12, "after": ""}

kv = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36',
            'referer': 'https://www.instagram.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'cookie':'ds_user_id=7835676456; csrftoken=z5yp7F7g7AApLBGWQUsNDiu34c48j5NF; shbid=8778; rur=ATN; sessionid=IGSCf1391681e97905f7a957d125894583f3c191115565cd1adb4355760592be42dd%3AII76wH33uF4BeIOeXm3ZYs60V6lXUa5z%3A%7B%22_auth_user_id%22%3A7835676456%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_platform%22%3A4%2C%22_token_ver%22%3A2%2C%22_token%22%3A%227835676456%3ALYhvsUR47Z7M61ksdm0YSKUcyoBAuiO9%3Ad4440c309c046f0980db215d1066ed3002932e8e4dc98a0e3d191ba865308e1c%22%2C%22last_refreshed%22%3A1527504417.3028142452%7D; mid=WwveFwALAAHWbyG__sTFw6noH6n3; mcd=3; fbm_124024574287414=base_domain=.instagram.com; urlgen="{\"time\": 1527504407\054 \"65.49.225.176\": 25820}:1fNFnV:LtI0lwhjY-dLK3wMQfD_1sxb140"; fbsr_124024574287414=aciYeBVvspIqaeLxn2CRSx0mza0ayhjLXcWqvk6uUPU.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUURScE1tY3lPdExQMkxXb1lORDNoeTF0c3J3ZzRBSnNSZ0VqUS00a21veXhCTjlPRUd1eXd0MUItMXdiR28yX3kwS1RYU0RBMVNvbzZpcVZPOUNGQTdnbWx6Rk1Md3JMMmctOURxa3pfVHd2XzN1eGkzM0NjR3p1TDQtVnZVSmZSMW12ZkUxUFg5ZWxNT0tRdl9yMEl2Vll5UjlvTFJMRUlwaUQ4S3BxUVFmNUVkMXJwVWRkRS1laDQ4aXhXMXFtN0s0M2g1eXpaR0U3WUVmbTJCVDlxam9uMFVDOVQyZko0MjEtVXJJWGs0WXZRUzlqbzhwLVNHejdsWEdJMnEyeW5LT2NGVVppUS1BbTJoVEdvSjU0MmZvMVIzR3pucC1GVDZCZ3JMd2RfeDZqX084am1MRE4yUEw5NlhyWHhYT2NPZmNJSTRfYVg0RWRHVkVCLTZUcTZxeCIsImlzc3VlZF9hdCI6MTUyNzUwNTAzOCwidXNlcl9pZCI6IjEwMDAyNTY3NzM1MDc5NSJ9'
}
pics_list = []

#base_url
r = requests.get(base_url, headers=kv)
r.encoding = r.apparent_encoding
print(r.status_code)
html = etree.HTML(r.content.decode())
h = html.xpath('''//script[@type="text/javascript"]''')[3].text.replace('window._sharedData = ', '').strip()[:-1]
pic_data = json.loads(h, encoding='utf-8')
end_cursor = pic_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
#print(end_cursor)
has_next_page = pic_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]
pics = pic_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
num = 1
for pic in pics:
    if pic['node'] != None:
        pic_data_dic = {}
        pic_data_dic['Num'] = num
        num += 1
        id = pic['node']['owner']['id']
        pic_url = pic['node']['display_url']
        like_count = pic['node']['edge_media_preview_like']['count']
        comment_count = pic['node']['edge_media_to_comment']['count']
        pic_data_dic['URL'] = pic_url
        pic_data_dic['Like_Count'] = like_count
        pic_data_dic['Commen_Count'] = comment_count
        pics_list.append(pic_data_dic)

var_value['id'] = id
count = 2
#print(pics_list)



# next_url
while has_next_page and count <= 10: #next_page输出数量或没有下一页取消
    print('crawing{0}'.format(count))
    var_value['after'] = end_cursor
    next_url = 'https://www.instagram.com/graphql/query/?query_hash=42323d64886122307be10013ad2dcc44&variables=&variables={0}'.format(json.dumps(var_value))
    #print(next_url)
    r = requests.get(next_url, headers=kv)
    r.encoding = r.apparent_encoding
    #print(r.status_code)
    pic_data = json.loads(r.text, encoding='uft-8')
    end_cursor = pic_data["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
    has_next_page = pic_data["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]
    pics = pic_data['data']['user']['edge_owner_to_timeline_media']['edges']
    for pic in pics:
        if pic['node'] != None:
            pic_data_dic = {}
            pic_data_dic['Num'] = num
            num += 1
            pic_url = pic['node']['display_url']
            like_count = pic['node']['edge_media_preview_like']['count']
            comment_count = pic['node']['edge_media_to_comment']['count']
            pic_data_dic['URL'] = pic_url
            pic_data_dic['Like_Count'] = like_count
            pic_data_dic['Commen_Count'] = comment_count
            pics_list.append(pic_data_dic)

    count += 1
#print(pics_list)

# next_url 2
#var_value['after'] = end_cursor
#next_url = 'https://www.instagram.com/graphql/query/?query_hash=42323d64886122307be10013ad2dcc44&variables=&variables={0}'.format(json.dumps(var_value))
#print(next_url)
#r = requests.get(next_url, headers=kv)
#r.encoding = r.apparent_encoding
#print(r.status_code)
#pic_data = json.loads(r.text, encoding='uft-8')
#end_cursor = pic_data["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
#pics = pic_data['data']['user']['edge_owner_to_timeline_media']['edges']
#for pic in pics:
#    if pic['node'] != None:
#         pic_data_dic = {}
#         pic_url = pic['node']['display_url']
#         like_count = pic['node']['edge_media_preview_like']['count']
#         comment_count = pic['node']['edge_media_to_comment']['count']
#         pic_data_dic['URL'] = pic_url
#         pic_data_dic['Like_Count'] = like_count
#         pic_data_dic['Commen_Count'] = comment_count
#         pics_list.append(pic_data_dic)

#print(pics_list)


#output.html:HTML格式输出
fout = open('output.html', 'w', encoding='utf-8')
fout.write("<html>")
fout.write("<body>")
fout.write("<ul>")
for data in pics_list:
    # 屏蔽掉原来的，重新写一个更美观的输出效果
    fout.write("<li>")
    #fout.write("<td>%s</td>" % data['URL'])
    #fout.write("<td>%s</td>" % data['Like_Count'])
    #fout.write("<td>%s</td>" % data['Commen_Count'])
    fout.write('<a href="%s" target="_blank">%s</a>' % (data['URL'],data['Num']))
    fout.write('<img src="%s">' % data['URL'])
    #fout.write('<p>%s</p>' % data['summary'])
    fout.write("</li>")
fout.write("</ul>")
fout.write("</body>")
fout.write("</html>")
fout.close()




