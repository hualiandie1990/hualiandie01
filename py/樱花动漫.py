# coding = utf-8
# !/usr/bin/python

"""

作者 繁华 内容均从互联网收集而来 仅供交流学习使用 版权归原创者所有 如侵犯了您的权益 请通知作者 将及时删除侵权内容
                    ====================fanhua====================

"""

from Crypto.Util.Padding import unpad
from urllib.parse import unquote
from Crypto.Cipher import ARC4
from urllib.parse import quote
from base.spider import Spider
from Crypto.Cipher import AES
from datetime import datetime
from bs4 import BeautifulSoup
from base64 import b64decode
import urllib.request
import urllib.parse
import binascii
import requests
import base64
import json
import time
import sys
import re
import os

sys.path.append('..')

xurl = "https://yinghua8.ee"

headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
          }

headers = {
    'Host': 'bfq.lggys.com',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua-platform': '"Windows"',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'sec-ch-ua-mobile': '?0',
    'Origin': 'https://bfq.lggys.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Length': '139'
           }

pm = ''

class Spider(Spider):
    global xurl
    global headerx
    global headers

    def getName(self):
        return "首页"

    def init(self, extend):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def extract_middle_text(self, text, start_str, end_str, pl, start_index1: str = '', end_index2: str = ''):
        if pl == 3:
            plx = []
            while True:
                start_index = text.find(start_str)
                if start_index == -1:
                    break
                end_index = text.find(end_str, start_index + len(start_str))
                if end_index == -1:
                    break
                middle_text = text[start_index + len(start_str):end_index]
                plx.append(middle_text)
                text = text.replace(start_str + middle_text + end_str, '')
            if len(plx) > 0:
                purl = ''
                for i in range(len(plx)):
                    matches = re.findall(start_index1, plx[i])
                    output = ""
                    for match in matches:
                        match3 = re.search(r'(?:^|[^0-9])(\d+)(?:[^0-9]|$)', match[1])
                        if match3:
                            number = match3.group(1)
                        else:
                            number = 0
                        if 'http' not in match[0]:
                            output += f"#{match[1]}${number}{xurl}{match[0]}"
                        else:
                            output += f"#{match[1]}${number}{match[0]}"
                    output = output[1:]
                    purl = purl + output + "$$$"
                purl = purl[:-3]
                return purl
            else:
                return ""
        else:
            start_index = text.find(start_str)
            if start_index == -1:
                return ""
            end_index = text.find(end_str, start_index + len(start_str))
            if end_index == -1:
                return ""

        if pl == 0:
            middle_text = text[start_index + len(start_str):end_index]
            return middle_text.replace("\\", "")

        if pl == 1:
            middle_text = text[start_index + len(start_str):end_index]
            matches = re.findall(start_index1, middle_text)
            if matches:
                jg = ' '.join(matches)
                return jg

        if pl == 2:
            middle_text = text[start_index + len(start_str):end_index]
            matches = re.findall(start_index1, middle_text)
            if matches:
                new_list = [f'{item}' for item in matches]
                jg = '$$$'.join(new_list)
                return jg

    def process_url(self, decoded_url, after_https, res, headerx, headers):

        url = re.sub(r'%u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), decoded_url)

        name = self.extract_middle_text(res, '"name":"', '"', 0).replace('\\', '')

        urls = f'https://bfq.lggys.com/?url={url}&next={after_https}&tittle={name}'
        res = requests.get(url=urls, headers=headerx)
        res = res.text

        time = self.extract_middle_text(res, '"time": "', '"', 0).replace('\\', '')
        vkey = self.extract_middle_text(res, '"vkey": "', '"', 0).replace('\\', '')

        payload = {
            "url": url,
            "time": time,
            "key": "",
            "vkey": vkey
                   }

        urlz = 'https://bfq.lggys.com/admin/mizhi_json.php'
        response = requests.post(url=urlz, headers=headers, data=payload)

        if response.status_code == 200:
            response_data = response.json()
            url = response_data['url']

        return url

    def homeContent(self, filter):
        result = {}
        result = {"class": [{"type_id": "1", "type_name": "电影"},
                            {"type_id": "2", "type_name": "剧集"},
                            {"type_id": "4", "type_name": "动漫"},
                            {"type_id": "3", "type_name": "综艺"}],

                  "list": [],
                  "filters": {"1": [{"key": "年代",
                                     "name": "年代",
                                     "value": [{"n": "全部", "v": ""},
                                               {"n": "2025", "v": "2025"},
                                               {"n": "2024", "v": "2024"},
                                               {"n": "2023", "v": "2023"},
                                               {"n": "2022", "v": "2022"},
                                               {"n": "2021", "v": "2021"},
                                               {"n": "2020", "v": "2020"},
                                               {"n": "2019", "v": "2019"},
                                               {"n": "2018", "v": "2018"}]}],
                              "2": [{"key": "年代",
                                     "name": "年代",
                                     "value": [{"n": "全部", "v": ""},
                                               {"n": "2025", "v": "2025"},
                                               {"n": "2024", "v": "2024"},
                                               {"n": "2023", "v": "2023"},
                                               {"n": "2022", "v": "2022"},
                                               {"n": "2021", "v": "2021"},
                                               {"n": "2020", "v": "2020"},
                                               {"n": "2019", "v": "2019"},
                                               {"n": "2018", "v": "2018"}]}],
                              "3": [{"key": "年代",
                                     "name": "年代",
                                     "value": [{"n": "全部", "v": ""},
                                               {"n": "2025", "v": "2025"},
                                               {"n": "2024", "v": "2024"},
                                               {"n": "2023", "v": "2023"},
                                               {"n": "2022", "v": "2022"},
                                               {"n": "2021", "v": "2021"},
                                               {"n": "2020", "v": "2020"},
                                               {"n": "2019", "v": "2019"},
                                               {"n": "2018", "v": "2018"}]}],
                              "4": [{"key": "年代",
                                     "name": "年代",
                                     "value": [{"n": "全部", "v": ""},
                                               {"n": "2025", "v": "2025"},
                                               {"n": "2024", "v": "2024"},
                                               {"n": "2023", "v": "2023"},
                                               {"n": "2022", "v": "2022"},
                                               {"n": "2021", "v": "2021"},
                                               {"n": "2020", "v": "2020"},
                                               {"n": "2019", "v": "2019"},
                                               {"n": "2018", "v": "2018"}]}]}}

        return result

    def homeVideoContent(self):
        videos = []

        try:
            detail = requests.get(url=xurl, headers=headerx)
            detail.encoding = "utf-8"
            res = detail.text

            doc = BeautifulSoup(res, "lxml")

            soups = doc.find_all('ul', class_="stui-vodlist")

            for soup in soups:
                vods = soup.find_all('li')

                for vod in vods:
                    names = vod.find('a', class_="lazyload")

                    name = names['title']

                    id = names['href']

                    pic = names['data-original']

                    if 'http' not in pic:
                        pic = xurl + pic

                    remarks = vod.find('span', class_="text-right")
                    remark = remarks.text.strip()

                    video = {
                        "vod_id": id,
                        "vod_name": name,
                        "vod_pic": pic,
                        "vod_remarks": remark
                             }
                    videos.append(video)

            result = {'list': videos}
            return result
        except:
            pass

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []

        if pg:
            page = int(pg)
        else:
            page = 1

        if '年代' in ext.keys():
            NdType = ext['年代']
        else:
            NdType = ''

        if page == 1:
            url = f'{xurl}/vodshow/{cid}-----------.html'

        else:
            url = f'{xurl}/vodshow/{cid}--------{str(page)}---{NdType}.html'

        try:
            detail = requests.get(url=url, headers=headerx)
            detail.encoding = "utf-8"
            res = detail.text
            doc = BeautifulSoup(res, "lxml")

            soups = doc.find_all('ul', class_="stui-vodlist")

            for soup in soups:
                vods = soup.find_all('li')

                for vod in vods:
                    names = vod.find('a', class_="lazyload")

                    name = names['title']

                    id = names['href']

                    pic = names['data-original']

                    if 'http' not in pic:
                        pic = xurl + pic

                    remarks = vod.find('span', class_="text-right")
                    remark = remarks.text.strip()

                    video = {
                        "vod_id": id,
                        "vod_name": name,
                        "vod_pic": pic,
                        "vod_remarks": remark
                            }
                    videos.append(video)

        except:
            pass
        result = {'list': videos}
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        global pm
        did = ids[0]
        result = {}
        videos = []

        if 'http' not in did:
            did = xurl + did

        res1 = requests.get(url=did, headers=headerx)
        res1.encoding = "utf-8"
        res = res1.text

        url = 'https://fs-im-kefu.7moor-fs1.com/ly/4d2c3f00-7d4c-11e5-af15-41bf63ae4ea0/1747729785570/yz.txt'
        response = requests.get(url)
        response.encoding = 'utf-8'
        code = response.text
        name = self.extract_middle_text(code, "s1='", "'", 0)
        Jumps = self.extract_middle_text(code, "s2='", "'", 0)

        content = '💖关注公众号【星视界Star】获取更多资源✨ShowStar&阿星为您介绍剧情💝' + self.extract_middle_text(res, 'detail-sketch">', '</span>', 0) + name

        director = self.extract_middle_text(res, '导演：', '</div>',1,'target=".*?">(.*?)</a>')

        actor = self.extract_middle_text(res, '主演：', '</div>', 1, 'target=".*?">(.*?)</a>')

        remarks = self.extract_middle_text(res,'时间：</span>','</p>', 0)

        year = self.extract_middle_text(res, '年份：</span>', '</p>', 0)
        year = year.replace('\t', '').replace('\n', '')

        area = self.extract_middle_text(res, '地区：</span>', '<span', 0)
        area = area.replace('\t', '').replace('\n', '')

        if name not in content:
            bofang = Jumps
            xianlu = '1'
        else:
            doc = self.extract_middle_text(res, 'end 详情', '播放地址', 0)
            doc = BeautifulSoup(doc, "lxml")

            soup = doc.find_all('h3')

            jishu = 0
            xian = []
            xianlu = ''
            bofang = ''
            gl = []

            for sou in soup:
                jishu = jishu + 1

                names = sou.text.strip()

                if any(item in names for item in gl):
                    continue

                xian.append(jishu)

                xianlu = xianlu + "星视界Star💖" + names + '$$$'

            xianlu = xianlu[:-3]

            for psou in xian:
                jishu = psou - 1

                soups = doc.find_all('ul', class_="stui-content__playlist")[jishu]

                soup = soups.find_all('a')

                for sou in soup:

                    id = sou['href']

                    if 'http' not in id:
                        id = xurl + id

                    name = sou.text.strip()

                    bofang = bofang + name + '$' + id + '#'

                bofang = bofang[:-1] + '$$$'

            bofang = bofang[:-3]

        videos.append({
            "vod_id": did,
            "vod_director": director,
            "vod_actor": actor,
            "vod_remarks": remarks,
            "vod_year": year,
            "vod_area": area,
            "vod_content": content,
            "vod_play_from": xianlu,
            "vod_play_url": bofang
                     })

        result['list'] = videos
        return result

    def playerContent(self, flag, id, vipFlags):
        parts = id.split("http")
        xiutan = 0

        if xiutan == 0:
            if len(parts) > 1:
                before_https, after_https = parts[0], 'http' + parts[1]

            if '239755956819.mp4' in after_https:
                url = after_https
            else:
                res = requests.get(url=after_https, headers=headerx)
                res = res.text
                url = self.extract_middle_text(res, '},"url":"', '"', 0).replace('\\', '')

                decoded_url = urllib.parse.unquote(url)

                url = self.process_url(decoded_url, after_https, res, headerx, headers)

            result = {}
            result["parse"] = xiutan
            result["playUrl"] = ''
            result["url"] = url
            result["header"] = headerx
            return result

    def searchContentPage(self, key, quick, page):
        result = {}
        videos = []

        if not page:
            page = '1'
        if page == '1':
            url = f'{xurl}/vodsearch/-------------.html?wd={key}&submit='

        else:
            url = f'{xurl}/vodsearch/{key}----------{str(page)}---.html'

        detail = requests.get(url=url, headers=headerx)
        detail.encoding = "utf-8"
        res = detail.text
        doc = BeautifulSoup(res, "lxml")

        soups = doc.find_all('ul', class_="stui-vodlist__media")

        for soup in soups:
            vods = soup.find_all('li')

            for vod in vods:
                names = vod.find('a', class_="lazyload")

                name = names['title']

                id = names['href']

                pic = names['data-original']

                if 'http' not in pic:
                    pic = xurl + pic

                remark = self.extract_middle_text(str(vod), 'class="pic-text text-right">', '</span>', 0)

                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark
                        }
                videos.append(video)

        result['list'] = videos
        result['page'] = page
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def searchContent(self, key, quick, pg="1"):
        return self.searchContentPage(key, quick, '1')

    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None



