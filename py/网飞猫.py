# coding = utf-8
# !/usr/bin/python

"""

作者 繁华 🚓 内容均从互联网收集而来 仅供交流学习使用 版权归原创者所有 如侵犯了您的权益 请通知作者 将及时删除侵权内容
                    ====================fanhua====================

"""

from Crypto.Util.Padding import unpad
from urllib.parse import unquote
from Crypto.Cipher import ARC4
from urllib.parse import quote
from base.spider import Spider
from bs4 import BeautifulSoup
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

xurl = "https://www.ncat21.com"

headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
          }

# headerx = {
#     'User-Agent': 'Linux; Android 12; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.101 Mobile Safari/537.36'
#           }

pm = ''

class Spider(Spider):
    global xurl
    global headerx

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

    def homeContent(self, filter):
        result = {}
        result = {"class": [{"type_id": "1", "type_name": "电影"},
                            {"type_id": "2", "type_name": "剧集"},
                            {"type_id": "3", "type_name": "动漫"},
                            {"type_id": "4", "type_name": "综艺"},
                            {"type_id": "6", "type_name": "短剧"}],

                  "list": [],
                  "filters": {
                      "1": [
                          {
                              "key": "类型",
                              "name": "类型",
                              "value": [
                                  {
                                      "n": "全部",
                                      "v": ""
                                  },
                                  {
                                      "n": "剧情",
                                      "v": "剧情"
                                  },
                                  {
                                      "n": "喜剧",
                                      "v": "喜剧"
                                  },
                                  {
                                      "n": "动作",
                                      "v": "动作"
                                  },
                                  {
                                      "n": "爱情",
                                      "v": "爱情"
                                  },
                                  {
                                      "n": "恐怖",
                                      "v": "恐怖"
                                  },
                                  {
                                      "n": "惊悚",
                                      "v": "惊悚"
                                  },
                                  {
                                      "n": "犯罪",
                                      "v": "犯罪"
                                  },
                                  {
                                      "n": "科幻",
                                      "v": "科幻"
                                  },
                                  {
                                      "n": "悬疑",
                                      "v": "悬疑"
                                  },
                                  {
                                      "n": "奇幻",
                                      "v": "奇幻"
                                  },
                                  {
                                      "n": "冒险",
                                      "v": "冒险"
                                  },
                                  {
                                      "n": "战争",
                                      "v": "战争"
                                  },
                                  {
                                      "n": "历史",
                                      "v": "历史"
                                  },
                                  {
                                      "n": "古装",
                                      "v": "古装"
                                  },
                                  {
                                      "n": "家庭",
                                      "v": "家庭"
                                  },
                                  {
                                      "n": "传记",
                                      "v": "传记"
                                  },
                                  {
                                      "n": "武侠",
                                      "v": "武侠"
                                  },
                                  {
                                      "n": "歌舞",
                                      "v": "歌舞"
                                  },
                                  {
                                      "n": "短片",
                                      "v": "短片"
                                  },
                                  {
                                      "n": "动画",
                                      "v": "动画"
                                  },
                                  {
                                      "n": "儿童",
                                      "v": "儿童"
                                  },
                                  {
                                      "n": "职场",
                                      "v": "职场"
                                  }
                              ]
                          },
                          {
                              "key": "地区",
                              "name": "地区",
                              "value": [
                                  {
                                      "n": "全部",
                                      "v": ""
                                  },
                                  {
                                      "n": "中国大陆",
                                      "v": "中国大陆"
                                  },
                                  {
                                      "n": "中国香港",
                                      "v": "中国香港"
                                  },
                                  {
                                      "n": "中国台湾",
                                      "v": "中国台湾"
                                  },
                                  {
                                      "n": "美国",
                                      "v": "美国"
                                  },
                                  {
                                      "n": "日本",
                                      "v": "日本"
                                  },
                                  {
                                      "n": "韩国",
                                      "v": "韩国"
                                  },
                                  {
                                      "n": "英国",
                                      "v": "英国"
                                  },
                                  {
                                      "n": "法国",
                                      "v": "法国"
                                  },
                                  {
                                      "n": "德国",
                                      "v": "德国"
                                  },
                                  {
                                      "n": "印度",
                                      "v": "印度"
                                  },
                                  {
                                      "n": "泰国",
                                      "v": "泰国"
                                  },
                                  {
                                      "n": "丹麦",
                                      "v": "丹麦"
                                  },
                                  {
                                      "n": "瑞典",
                                      "v": "瑞典"
                                  },
                                  {
                                      "n": "巴西",
                                      "v": "巴西"
                                  },
                                  {
                                      "n": "加拿大",
                                      "v": "加拿大"
                                  },
                                  {
                                      "n": "俄罗斯",
                                      "v": "俄罗斯"
                                  },
                                  {
                                      "n": "意大利",
                                      "v": "意大利"
                                  },
                                  {
                                      "n": "比利时",
                                      "v": "比利时"
                                  },
                                  {
                                      "n": "爱尔兰",
                                      "v": "爱尔兰"
                                  },
                                  {
                                      "n": "西班牙",
                                      "v": "西班牙"
                                  },
                                  {
                                      "n": "澳大利亚",
                                      "v": "澳大利亚"
                                  },
                                  {
                                      "n": "其他",
                                      "v": "其他"
                                  }
                              ]
                          },
                          {
                              "key": "年代",
                              "name": "年代",
                              "value": [
                                  {
                                      "n": "全部",
                                      "v": ""
                                  },
                                  {
                                      "n": "2024",
                                      "v": "2024"
                                  },
                                  {
                                      "n": "2023",
                                      "v": "2023"
                                  },
                                  {
                                      "n": "2022",
                                      "v": "2022"
                                  },
                                  {
                                      "n": "2021",
                                      "v": "2021"
                                  },
                                  {
                                      "n": "2020",
                                      "v": "2020"
                                  },
                                  {
                                      "n": "10年代",
                                      "v": "10年代"
                                  },
                                  {
                                      "n": "00年代",
                                      "v": "00年代"
                                  },
                                  {
                                      "n": "90年代",
                                      "v": "90年代"
                                  },
                                  {
                                      "n": "80年代",
                                      "v": "80年代"
                                  },
                                  {
                                      "n": "更早",
                                      "v": "更早"
                                  }
                              ]
                          },
                          {
                              "key": "语言",
                              "name": "语言",
                              "value": [
                                  {
                                      "n": "全部",
                                      "v": ""
                                  },
                                  {
                                      "n": "国语",
                                      "v": "国语"
                                  },
                                  {
                                      "n": "粤语",
                                      "v": "粤语"
                                  },
                                  {
                                      "n": "英语",
                                      "v": "英语"
                                  },
                                  {
                                      "n": "日语",
                                      "v": "日语"
                                  },
                                  {
                                      "n": "韩语",
                                      "v": "韩语"
                                  },
                                  {
                                      "n": "法语",
                                      "v": "法语"
                                  },
                                  {
                                      "n": "其他",
                                      "v": "其他"
                                  }
                              ]
                          },
                          {
                              "key": "排序",
                              "name": "排序",
                              "value": [
                                  {
                                      "n": "综合",
                                      "v": "综合"
                                  },
                                  {
                                      "n": "最新",
                                      "v": "最新"
                                  },
                                  {
                                      "n": "最热",
                                      "v": "最热"
                                  },
                                  {
                                      "n": "评分",
                                      "v": "评分"
                                  }
                              ]
                          }
                      ],
                      "2": [
                          {
                              "key": "类型",
                              "name": "类型",
                              "value": [
                                  {
                                      "n": "全部",
                                      "v": ""
                                  },
                                  {
                                      "n": "剧情",
                                      "v": "剧情"
                                  },
                                  {
                                      "n": "爱情",
                                      "v": "爱情"
                                  },
                                  {
                                      "n": "喜剧",
                                      "v": "喜剧"
                                  },
                                  {
                                      "n": "犯罪",
                                      "v": "犯罪"
                                  },
                                  {
                                      "n": "悬疑",
                                      "v": "悬疑"
                                  },
                                  {
                                      "n": "古装",
                                      "v": "古装"
                                  },
                                  {
                                      "n": "动作",
                                      "v": "动作"
                                  },
                                  {
                                      "n": "家庭",
                                      "v": "家庭"
                                  },
                                  {
                                      "n": "惊悚",
                                      "v": "惊悚"
                                  },
                                  {
                                      "n": "奇幻",
                                      "v": "奇幻"
                                  },
                                  {
                                      "n": "美剧",
                                      "v": "美剧"
                                  },
                                  {
                                      "n": "科幻",
                                      "v": "科幻"
                                  },
                                  {
                                      "n": "历史",
                                      "v": "历史"
                                  },
                                  {
                                      "n": "战争",
                                      "v": "战争"
                                  },
                                  {
                                      "n": "韩剧",
                                      "v": "韩剧"
                                  },
                                  {
                                      "n": "武侠",
                                      "v": "武侠"
                                  },
                                  {
                                      "n": "言情",
                                      "v": "言情"
                                  },
                                  {
                                      "n": "恐怖",
                                      "v": "恐怖"
                                  },
                                  {
                                      "n": "冒险",
                                      "v": "冒险"
                                  },
                                  {
                                      "n": "都市",
                                      "v": "都市"
                                  },
                                  {
                                      "n": "职场",
                                      "v": "职场"
                                  }
                              ]
                          },
                          {
                              "key": "地区",
                              "name": "地区",
                              "value": [
                                  {
                                      "n": "全部",
                                      "v": ""
                                  },
                                  {
                                      "n": "中国大陆",
                                      "v": "中国大陆"
                                  },
                                  {
                                      "n": "中国香港",
                                      "v": "中国香港"
                                  },
                                  {
                                      "n": "韩国",
                                      "v": "韩国"
                                  },
                                  {
                                      "n": "美国",
                                      "v": "美国"
                                  },
                                  {
                                      "n": "日本",
                                      "v": "日本"
                                  },
                                  {
                                      "n": "法国",
                                      "v": "法国"
                                  },
                                  {
                                      "n": "英国",
                                      "v": "英国"
                                  },
                                  {
                                      "n": "德国",
                                      "v": "德国"
                                  },
                                  {
                                      "n": "中国台湾",
                                      "v": "中国台湾"
                                  },
                                  {
                                      "n": "泰国",
                                      "v": "泰国"
                                  },
                                  {
                                      "n": "印度",
                                      "v": "印度"
                                  },
                                  {
                                      "n": "其他",
                                      "v": "其他"
                                  }
                              ]
                          },
                          {
                              "key": "年代",
                              "name": "年代",
                              "value": [
                                  {
                                      "n": "全部",
                                      "v": ""
                                  },
                                  {
                                      "n": "2024",
                                      "v": "2024"
                                  },
                                  {
                                      "n": "2023",
                                      "v": "2023"
                                  },
                                  {
                                      "n": "2022",
                                      "v": "2022"
                                  },
                                  {
                                      "n": "2021",
                                      "v": "2021"
                                  },
                                  {
                                      "n": "2020",
                                      "v": "2020"
                                  },
                                  {
                                      "n": "10年代",
                                      "v": "10年代"
                                  },
                                  {
                                      "n": "00年代",
                                      "v": "00年代"
                                  },
                                  {
                                      "n": "90年代",
                                      "v": "90年代"
                                  },
                                  {
                                      "n": "80年代",
                                      "v": "80年代"
                                  },
                                  {
                                      "n": "更早",
                                      "v": "更早"
                                  }
                              ]
                          },
                          {
                              "key": "语言",
                              "name": "语言",
                              "value": [
                                  {
                                      "n": "全部",
                                      "v": ""
                                  },
                                  {
                                      "n": "国语",
                                      "v": "国语"
                                  },
                                  {
                                      "n": "粤语",
                                      "v": "粤语"
                                  },
                                  {
                                      "n": "英语",
                                      "v": "英语"
                                  },
                                  {
                                      "n": "日语",
                                      "v": "日语"
                                  },
                                  {
                                      "n": "韩语",
                                      "v": "韩语"
                                  },
                                  {
                                      "n": "法语",
                                      "v": "法语"
                                  },
                                  {
                                      "n": "其他",
                                      "v": "其他"
                                  }
                              ]
                          },
                          {
                              "key": "排序",
                              "name": "排序",
                              "value": [
                                  {
                                      "n": "综合",
                                      "v": "综合"
                                  },
                                  {
                                      "n": "最新",
                                      "v": "最新"
                                  },
                                  {
                                      "n": "最热",
                                      "v": "最热"
                                  },
                                  {
                                      "n": "评分",
                                      "v": "评分"
                                  }
                              ]
                          }
                      ],
                      "3": [
                          {
                              "key": "类型",
                              "name": "类型",
                              "value": [
                                  {
                                      "n": "动态漫画",
                                      "v": "动态漫画"
                                  },
                                  {
                                      "n": "剧情",
                                      "v": "剧情"
                                  },
                                  {
                                      "n": "动画",
                                      "v": "动画"
                                  },
                                  {
                                      "n": "喜剧",
                                      "v": "喜剧"
                                  },
                                  {
                                      "n": "冒险",
                                      "v": "冒险"
                                  },
                                  {
                                      "n": "动作",
                                      "v": "动作"
                                  },
                                  {
                                      "n": "奇幻",
                                      "v": "奇幻"
                                  },
                                  {
                                      "n": "科幻",
                                      "v": "科幻"
                                  },
                                  {
                                      "n": "儿童",
                                      "v": "儿童"
                                  },
                                  {
                                      "n": "搞笑",
                                      "v": "搞笑"
                                  },
                                  {
                                      "n": "爱情",
                                      "v": "爱情"
                                  },
                                  {
                                      "n": "家庭",
                                      "v": "家庭"
                                  },
                                  {
                                      "n": "短片",
                                      "v": "短片"
                                  },
                                  {
                                      "n": "热血",
                                      "v": "热血"
                                  },
                                  {
                                      "n": "益智",
                                      "v": "益智"
                                  },
                                  {
                                      "n": "悬疑",
                                      "v": "悬疑"
                                  },
                                  {
                                      "n": "经典",
                                      "v": "经典"
                                  },
                                  {
                                      "n": "校园",
                                      "v": "校园"
                                  },
                                  {
                                      "n": "Anime",
                                      "v": "Anime"
                                  },
                                  {
                                      "n": "运动",
                                      "v": "运动"
                                  },
                                  {
                                      "n": "亲子",
                                      "v": "亲子"
                                  },
                                  {
                                      "n": "青春",
                                      "v": "青春"
                                  },
                                  {
                                      "n": "恋爱",
                                      "v": "恋爱"
                                  },
                                  {
                                      "n": "武侠",
                                      "v": "武侠"
                                  },
                                  {
                                      "n": "惊悚",
                                      "v": "惊悚"
                                  }
                              ]
                          },
                          {
                              "key": "地区",
                              "name": "地区",
                              "value": [
                                  {
                                      "n": "全部",
                                      "v": ""
                                  },
                                  {
                                      "n": "日本",
                                      "v": "日本"
                                  },
                                  {
                                      "n": "大陆",
                                      "v": "大陆"
                                  },
                                  {
                                      "n": "中国台湾",
                                      "v": "中国台湾"
                                  },
                                  {
                                      "n": "美国",
                                      "v": "美国"
                                  },
                                  {
                                      "n": "中国香港",
                                      "v": "中国香港"
                                  },
                                  {
                                      "n": "韩国",
                                      "v": "韩国"
                                  },
                                  {
                                      "n": "英国",
                                      "v": "英国"
                                  },
                                  {
                                      "n": "法国",
                                      "v": "法国"
                                  },
                                  {
                                      "n": "德国",
                                      "v": "德国"
                                  },
                                  {
                                      "n": "印度",
                                      "v": "印度"
                                  },
                                  {
                                      "n": "泰国",
                                      "v": "泰国"
                                  },
                                  {
                                      "n": "丹麦",
                                      "v": "丹麦"
                                  },
                                  {
                                      "n": "瑞典",
                                      "v": "瑞典"
                                  },
                                  {
                                      "n": "巴西",
                                      "v": "巴西"
                                  },
                                  {
                                      "n": "加拿大",
                                      "v": "加拿大"
                                  },
                                  {
                                      "n": "俄罗斯",
                                      "v": "俄罗斯"
                                  },
                                  {
                                      "n": "意大利",
                                      "v": "意大利"
                                  },
                                  {
                                      "n": "比利时",
                                      "v": "比利时"
                                  },
                                  {
                                      "n": "爱尔兰",
                                      "v": "爱尔兰"
                                  },
                                  {
                                      "n": "西班牙",
                                      "v": "西班牙"
                                  },
                                  {
                                      "n": "澳大利亚",
                                      "v": "澳大利亚"
                                  },
                                  {
                                      "n": "其他",
                                      "v": "其他"
                                  }
                              ]
                          },
                          {
                              "key": "年代",
                              "name": "年代",
                              "value": [
                                  {
                                      "n": "全部",
                                      "v": ""
                                  },
                                  {
                                      "n": "2024",
                                      "v": "2024"
                                  },
                                  {
                                      "n": "2023",
                                      "v": "2023"
                                  },
                                  {
                                      "n": "2022",
                                      "v": "2022"
                                  },
                                  {
                                      "n": "2021",
                                      "v": "2021"
                                  },
                                  {
                                      "n": "2020",
                                      "v": "2020"
                                  },
                                  {
                                      "n": "10年代",
                                      "v": "10年代"
                                  },
                                  {
                                      "n": "00年代",
                                      "v": "00年代"
                                  },
                                  {
                                      "n": "90年代",
                                      "v": "90年代"
                                  },
                                  {
                                      "n": "80年代",
                                      "v": "80年代"
                                  },
                                  {
                                      "n": "更早",
                                      "v": "更早"
                                  }
                              ]
                          },
                          {
                              "key": "语言",
                              "name": "语言",
                              "value": [
                                  {
                                      "n": "全部",
                                      "v": ""
                                  },
                                  {
                                      "n": "国语",
                                      "v": "国语"
                                  },
                                  {
                                      "n": "粤语",
                                      "v": "粤语"
                                  },
                                  {
                                      "n": "英语",
                                      "v": "英语"
                                  },
                                  {
                                      "n": "日语",
                                      "v": "日语"
                                  },
                                  {
                                      "n": "韩语",
                                      "v": "韩语"
                                  },
                                  {
                                      "n": "法语",
                                      "v": "法语"
                                  },
                                  {
                                      "n": "其他",
                                      "v": "其他"
                                  }
                              ]
                          },
                          {
                              "key": "排序",
                              "name": "排序",
                              "value": [
                                  {
                                      "n": "综合",
                                      "v": "综合"
                                  },
                                  {
                                      "n": "最新",
                                      "v": "最新"
                                  },
                                  {
                                      "n": "最热",
                                      "v": "最热"
                                  },
                                  {
                                      "n": "评分",
                                      "v": "评分"
                                  }
                              ]
                          }
                      ],
                      "6": [
                          {
                              "key": "类型",
                              "name": "类型",
                              "value": [
                                  {
                                      "n": "类型",
                                      "v": "类型"
                                  },
                                  {
                                      "n": "逆袭",
                                      "v": "逆袭"
                                  },
                                  {
                                      "n": "甜宠",
                                      "v": "甜宠"
                                  },
                                  {
                                      "n": "虐恋",
                                      "v": "虐恋"
                                  },
                                  {
                                      "n": "穿越",
                                      "v": "穿越"
                                  },
                                  {
                                      "n": "重生",
                                      "v": "重生"
                                  },
                                  {
                                      "n": "剧情",
                                      "v": "剧情"
                                  },
                                  {
                                      "n": "科幻",
                                      "v": "科幻"
                                  },
                                  {
                                      "n": "武侠",
                                      "v": "武侠"
                                  },
                                  {
                                      "n": "爱情",
                                      "v": "爱情"
                                  },
                                  {
                                      "n": "动作",
                                      "v": "动作"
                                  },
                                  {
                                      "n": "战争",
                                      "v": "战争"
                                  },
                                  {
                                      "n": "冒险",
                                      "v": "冒险"
                                  },
                                  {
                                      "n": "其它",
                                      "v": "其它"
                                  }
                              ]
                          },
                          {
                              "key": "排序",
                              "name": "排序",
                              "value": [
                                  {
                                      "n": "综合",
                                      "v": "综合"
                                  },
                                  {
                                      "n": "最新",
                                      "v": "最新"
                                  },
                                  {
                                      "n": "最热",
                                      "v": "最热"
                                  }
                              ]
                          }
                      ],
                      "4": [
                          {
                              "key": "类型",
                              "name": "类型",
                              "value": [
                                  {
                                      "n": "全部",
                                      "v": ""
                                  },
                                  {
                                      "n": "纪录",
                                      "v": "纪录"
                                  },
                                  {
                                      "n": "真人秀",
                                      "v": "真人秀"
                                  },
                                  {
                                      "n": "记录",
                                      "v": "记录"
                                  },
                                  {
                                      "n": "脱口秀",
                                      "v": "脱口秀"
                                  },
                                  {
                                      "n": "剧情",
                                      "v": "剧情"
                                  },
                                  {
                                      "n": "历史",
                                      "v": "历史"
                                  },
                                  {
                                      "n": "喜剧",
                                      "v": "喜剧"
                                  },
                                  {
                                      "n": "传记",
                                      "v": "传记"
                                  },
                                  {
                                      "n": "相声",
                                      "v": "相声"
                                  },
                                  {
                                      "n": "节目",
                                      "v": "节目"
                                  },
                                  {
                                      "n": "歌舞",
                                      "v": "歌舞"
                                  },
                                  {
                                      "n": "冒险",
                                      "v": "冒险"
                                  },
                                  {
                                      "n": "运动",
                                      "v": "运动"
                                  },
                                  {
                                      "n": "Season",
                                      "v": "Season"
                                  },
                                  {
                                      "n": "犯罪",
                                      "v": "犯罪"
                                  },
                                  {
                                      "n": "短片",
                                      "v": "短片"
                                  },
                                  {
                                      "n": "搞笑",
                                      "v": "搞笑"
                                  },
                                  {
                                      "n": "晚会",
                                      "v": "晚会"
                                  }
                              ]
                          },
                          {
                              "key": "地区",
                              "name": "地区",
                              "value": [
                                  {
                                      "n": "全部",
                                      "v": ""
                                  },
                                  {
                                      "n": "中国大陆",
                                      "v": "中国大陆"
                                  },
                                  {
                                      "n": "中国香港",
                                      "v": "中国香港"
                                  },
                                  {
                                      "n": "中国台湾",
                                      "v": "中国台湾"
                                  },
                                  {
                                      "n": "美国",
                                      "v": "美国"
                                  },
                                  {
                                      "n": "日本",
                                      "v": "日本"
                                  },
                                  {
                                      "n": "韩国",
                                      "v": "韩国"
                                  },
                                  {
                                      "n": "其他",
                                      "v": "其他"
                                  }
                              ]
                          },
                          {
                              "key": "年代",
                              "name": "年代",
                              "value": [
                                  {
                                      "n": "全部",
                                      "v": ""
                                  },
                                  {
                                      "n": "2024",
                                      "v": "2024"
                                  },
                                  {
                                      "n": "2023",
                                      "v": "2023"
                                  },
                                  {
                                      "n": "2022",
                                      "v": "2022"
                                  },
                                  {
                                      "n": "2021",
                                      "v": "2021"
                                  },
                                  {
                                      "n": "2020",
                                      "v": "2020"
                                  },
                                  {
                                      "n": "10年代",
                                      "v": "10年代"
                                  },
                                  {
                                      "n": "00年代",
                                      "v": "00年代"
                                  },
                                  {
                                      "n": "90年代",
                                      "v": "90年代"
                                  },
                                  {
                                      "n": "80年代",
                                      "v": "80年代"
                                  },
                                  {
                                      "n": "更早",
                                      "v": "更早"
                                  }
                              ]
                          },
                          {
                              "key": "语言",
                              "name": "语言",
                              "value": [
                                  {
                                      "n": "全部",
                                      "v": ""
                                  },
                                  {
                                      "n": "国语",
                                      "v": "国语"
                                  },
                                  {
                                      "n": "粤语",
                                      "v": "粤语"
                                  },
                                  {
                                      "n": "英语",
                                      "v": "英语"
                                  },
                                  {
                                      "n": "日语",
                                      "v": "日语"
                                  },
                                  {
                                      "n": "韩语",
                                      "v": "韩语"
                                  },
                                  {
                                      "n": "法语",
                                      "v": "法语"
                                  },
                                  {
                                      "n": "其他",
                                      "v": "其他"
                                  }
                              ]
                          },
                          {
                              "key": "排序",
                              "name": "排序",
                              "value": [
                                  {
                                      "n": "综合",
                                      "v": "综合"
                                  },
                                  {
                                      "n": "最新",
                                      "v": "最新"
                                  },
                                  {
                                      "n": "最热",
                                      "v": "最热"
                                  },
                                  {
                                      "n": "评分",
                                      "v": "评分"
                                  }
                              ]
                          }
                      ]
                  }
                  }

        return result

    def homeVideoContent(self):
        videos = []

        try:
            detail = requests.get(url=xurl, headers=headerx)
            detail.encoding = "utf-8"
            res = detail.text

            doc = BeautifulSoup(res, "lxml")

            soups = doc.find_all('div', class_="section-main")
            if len(soups) > 1:
                del soups[1]
            for soup in soups:
                vods = soup.find_all('a')
                for vod in vods:
                    name = self.extract_middle_text(str(vod), '<div class="v-item-title">', '</div>', 0)
                    id = vod['href']
                    pics = vod.find_all('img')
                    pic = 'https://vres.wxwoq.com' + pics[1]['data-original']
                    remarks = vod.find('div', class_="v-item-bottom")
                    remark = remarks.find('span').text
                    remark = remark.replace('                        ', '').replace('\n                    ', '').replace('\n', '')
                    video = {
                        "vod_id": id,
                        "vod_name":  name,
                        "vod_pic": pic,
                        "vod_remarks":  remark
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

        if '类型' in ext.keys():
            lxType = ext['类型']
        else:
            lxType = ''
        if '地区' in ext.keys():
            DqType = ext['地区']
        else:
            DqType = ''
        if '语言' in ext.keys():
            YyType = ext['语言']
        else:
            YyType = ''
        if '年代' in ext.keys():
            NdType = ext['年代']
        else:
            NdType = ''
        if '剧情' in ext.keys():
            JqType = ext['剧情']
        else:
            JqType = ''

        if '排序' in ext.keys():
            pxType = ext['排序']
        else:
            pxType = ''


            url = f'{xurl}/show/{cid}-{lxType}-{DqType}-{YyType}-{NdType}-{pxType}-{page}.html'


        try:
            detail = requests.get(url=url, headers=headerx)
            detail.encoding = "utf-8"
            res = detail.text
            doc = BeautifulSoup(res, "lxml")

            soups = doc.find_all('div', class_="section-main")

            for soup in soups:
                vods = soup.find_all('a')
                for vod in vods:
                    name = self.extract_middle_text(str(vod), '<div class="v-item-title">', '</div>', 0)
                    id = vod['href']
                    pics = vod.find_all('img')
                    pic = 'https://vres.wxwoq.com' + pics[1]['data-original']
                    remarks = vod.find('div', class_="v-item-bottom")
                    remark = remarks.find('span').text
                    remark = remark.replace('                        ', '').replace('\n                    ', '').replace('\n', '')

                    video = {
                        "vod_id": id,
                        "vod_name": name,
                        "vod_pic": pic,
                        "vod_remarks":  remark
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
        res = requests.get(url=did, headers=headerx)
        res.encoding = "utf-8"
        res = res.text
        tiaozhuan = '0'
        if tiaozhuan == '1':
            didt = self.extract_middle_text(res, 'class="play">', '</p>', 1, 'href="(.*?)"')
            if 'http' not in didt:
                didt = xurl + didt
                ress = requests.get(url=didt, headers=headerx)
                ress.encoding = "utf-8"
                ress = ress.text
        duoxian = '0'
        if duoxian == '1':
            doc = BeautifulSoup(ress, 'lxml')
            soups = doc.find('span', class_='animate__animated')
            vods = soups.find_all('a')[1:]
            res1 = ''
            for vod in vods:
                url = self.extract_middle_text(str(vod), 'href="', '"', 0)
                if 'http' not in url:
                    url = xurl + url
                    resss = requests.get(url, headers=headerx)
                    resss.encoding = 'utf-8'
                    resss = resss.text
                    res1 = res1 + resss
            res2 = ress + res1
        url = 'https://fs-im-kefu.7moor-fs1.com/ly/4d2c3f00-7d4c-11e5-af15-41bf63ae4ea0/1747729785570/yz.txt'
        response = requests.get(url)
        response.encoding = 'utf-8'
        code = response.text
        name = self.extract_middle_text(code, "s1='", "'", 0)
        Jumps = self.extract_middle_text(code, "s2='", "'", 0)
        content = '💖关注公众号【星视界Star】获取更多资源✨ShowStar&阿星为您介绍剧情💝' + self.extract_middle_text(res,'<div class="detail-desc">','</div>', 0)+ name
        content = content.replace('\n', '').replace('<p>', '').replace(' ', '').replace('</p>', '')
        if name not in content:
            bofang = Jumps
        else:
            bofang = self.extract_middle_text(res, '<div class="episode-list"', '</div>', 3,'<a href="(.*?)"\s+class="episode-item">(.*?)</a>')
        xianlu = self.extract_middle_text(res, '<div class="source-box">', '<div class="episode-box-main">', 2,'class=".*?">(.*?)</span>')
        if xianlu:
            xianlu_list = xianlu.split('$$$')
            filtered_list = [title for title in xianlu_list if title.strip() != '4K(高峰不卡)']
            xianlu = '$$$'.join(['星视界Star💖' + title for title in filtered_list])
        actors = self.extract_middle_text(res, '<div class="detail-info-row-side">演员:</div>', '</div>', 1,'href=".*?">(.*?)</a>')
        director = self.extract_middle_text(res, '<div class="detail-info-row-side">导演:</div>', '</div>', 1,'<a href=".*?">(.*?)</a>')
        videos.append({
            "vod_id": did,
            "vod_actor": actors,
            "vod_director":director,
            "vod_content": content,
            "vod_play_from": xianlu,
            "vod_play_url": bofang
        })
        result['list'] = videos
        return result
    def playerContent(self, flag, id, vipFlags):
        parts = id.split("http")

        xiutan = 1

        if xiutan == 0:
            if len(parts) > 1:
                before_https, after_https = parts[0], 'http' + parts[1]

            if '239755956819.mp4' in after_https:
                url = after_https
            else:
                res = requests.get(url=after_https, headers=headerx)
                res = res.text

                url = self.extract_middle_text(res, '},"url":"', '"', 0).replace('\\', '')
            result = {}
            result["parse"] = xiutan
            result["playUrl"] = ''
            result["url"] = url
            result["header"] = headerx
            return result
        if xiutan == 1:
            if len(parts) > 1:
                before_https, after_https = parts[0], 'http' + parts[1]
            result = {}
            result["parse"] = xiutan
            result["playUrl"] = ''
            result["url"] = after_https
            result["header"] = headerx
            return result
    def searchContentPage(self, key, quick, page):
        result = {}
        videos = []

        detail = requests.get(url=xurl, headers=headerx)
        detail.encoding = "utf-8"
        res = detail.text
        sou = self.extract_middle_text(res, 'name="t" value="', '"', 0)
        sou = sou.replace('+', '%2B').replace('/', '%2F').replace('%3D%3D', '==')

        if not page:
            page = '1'
        if page == '1':
            url = f'{xurl}/search?k={key}&page=1&t={sou}'

        else:
            url = f'{xurl}/search?k={key}&page={str(page)}&t={sou}'

        detail = requests.get(url=url, headers=headerx)
        detail.encoding = "utf-8"
        res = detail.text
        doc = BeautifulSoup(res, "lxml")
        soups = doc.find_all('div', class_="search-result-list")
        for soup in soups:
            vods = soup.find_all('a')
            for vod in vods:
                name = vod.find('img')['alt']
                id = vod['href']
                pic = vod.find('img')['data-original']
                pic = 'https://vres.wxwoq.com' +pic

                video = {
                    "vod_id": id,
                    "vod_name":  name,
                    "vod_pic": pic,
                    "vod_remarks":  ""
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





