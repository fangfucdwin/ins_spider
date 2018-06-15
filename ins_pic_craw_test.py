#from Eaphan Liu
#mailto:fangfucdwin@qq.com




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
            'cookie':'获取登陆cookie'
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
    fout.write("<li>")
    #fout.write("<td>%s</td>" % data['URL'])
    #fout.write("<td>%s</td>" % data['Like_Count'])
    #fout.write("<td>%s</td>" % data['Commen_Count'])
    fout.write('<a href="%s" target="_blank">%s</a>' % (data['URL'],data['Num']))
    fout.write('<img src="%s">' % data['URL'])
    fout.write("</li>")
fout.write("</ul>")
fout.write("</body>")
fout.write("</html>")
fout.close()




