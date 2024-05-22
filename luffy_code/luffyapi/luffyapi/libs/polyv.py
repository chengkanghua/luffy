
from django.conf import settings
import time
import requests
import hashlib

class PolyvPlayer(object):
    def __init__(self,userId,secretkey,tokenUrl):
        """初始化，提供用户id和秘钥"""
        self.userId = userId  # e3a65556c5
        self.secretKey = secretkey # g9mNe0IYDT
        self.tokenUrl = tokenUrl #https://hls.videocc.net/service/v1/token

    def tomd5(self, value):  #生成sign请求参数的值的
        """取md5值"""
        return hashlib.md5(value.encode()).hexdigest()

    # 获取视频数据的token
    def get_video_token(self, videoId, viewerIp, viewerId=None, viewerName='', extraParams='HTML5'):

        """
        :param videoId: 视频id
        :param viewerId: 看视频用户id
        :param viewerIp: 看视频用户ip
        :param viewerName: 看视频用户昵称
        :param extraParams: 扩展参数
        :param sign: 加密的sign
        :return: 返回点播的视频的token
        """
        ts = int(time.time() * 1000)  # 时间戳

        plain = {
            "userId": self.userId,
            'videoId': videoId,
            'ts': ts,
            'viewerId': viewerId,
            'viewerIp': viewerIp,
            'viewerName': viewerName,
            'extraParams': extraParams
        }

        # 按照ASCKII升序 key + value + key + value... + value 拼接
        plain_sorted = {}  #python3.6以上的python，如果是python3.5和以下版本，需要用OrderDict 有序字典

        key_temp = sorted(plain)
        for key in key_temp:
            plain_sorted[key] = plain[key]
        print(plain_sorted)

        plain_string = ''
        for k, v in plain_sorted.items():
            plain_string += str(k) + str(v)
        print(plain_string)

        # 首尾拼接上秘钥
        sign_data = self.secretKey + plain_string + self.secretKey

        # 取sign_data的md5的大写
        sign = self.tomd5(sign_data).upper()

        # 新的带有sign的字典
        plain.update({'sign': sign})

        # python 提供的发送http请求的模块，js ajax，爬虫requests模块

        result = requests.post(
            url=self.tokenUrl,
            headers={"Content-type": "application/x-www-form-urlencoded"},
            data=plain
        ).json()  #json.loads 反序列化

        token = {} if isinstance(result, str) else result.get("data", {})

        return token


