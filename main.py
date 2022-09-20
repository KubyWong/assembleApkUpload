#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

import requests

import sys

# gradle打包apk需要用到
import os
import subprocess
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

from ConstVal import AppConstVal, BetaqrConstVal, NotifyConstVal

appData = AppConstVal.APP_DATA_MAP
inputUpdateContent = input("请输入更新内容：")
appData["changelog"] = inputUpdateContent

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
    'Content-Type': "application/json",
    "Connection": "keep-alive",
    "Accept-Language": "zh-CN,zh;q=0.9"
}


# 获取上传应用url
def _getUploadAppUrl():
    # 获取上传的目标服务器
    params = {"type": "android", "bundle_id": BetaqrConstVal.appBundleId, "api_token": BetaqrConstVal.apiToken}
    uploadTokenResponse = requests.post(url=BetaqrConstVal.baseUrl, params=params, headers=headers)
    jsonData = json.loads(uploadTokenResponse.text)
    print("getUploadAppUrl()--->", jsonData)
    return jsonData


# 上传apk ，分两步：1、获取apk上传url 2、上传apk到获取到的url中
def uploadApk():
    uploadUrl = _getUploadAppUrl()
    uploadApkAndShow(uploadUrl)


def uploadApkAndShow(jsonData):
    # 获取上传的目标服务器
    uploadIconUrl = jsonData["cert"]["icon"]["upload_url"]
    iconKey = jsonData["cert"]["icon"]["key"]
    iconToken = jsonData["cert"]["icon"]["token"]

    uploadApkUrl = jsonData["cert"]["binary"]["upload_url"]
    key = jsonData["cert"]["binary"]["key"]
    token = jsonData["cert"]["binary"]["token"]

    iconPath = AppConstVal.APP_ICON_PATH
    iconFile = {'file': open(iconPath, "rb")}
    iconParams = {
        "key": iconKey,
        "token": iconToken,
    }

    uploadIconResult = requests.post(uploadIconUrl, files=iconFile, data=iconParams)
    print("icon上传结果：", uploadIconResult.text)

    print("=============apk正在上传，清耐心等待==============")
    # 上传安装包
    e = MultipartEncoder(
        fields={
            'key': key,
            'token': token,
            'x:name': appData['name'],
            'x:version': appData['versionShort'],
            'x:build': appData['build'],
            'x:changelog': appData['changelog'],
            'file': (
                'upload.apk', open(AppConstVal.APP_APK_PATH, 'rb'), 'application/octet-stream'),
        }
    )
    m = MultipartEncoderMonitor(e, my_callback)
    uploadResult = requests.post(uploadApkUrl, data=m, headers={'Content-Type': m.content_type})
    print("\napk上传结果：", uploadResult.text)
    return


def my_callback(monitor):
    progress = (monitor.bytes_read / monitor.len) * 100
    print("\r 文件上传进度：%d%%(%d/%d)" % (progress, monitor.bytes_read, monitor.len), end=" ")


# 发送企业微信通知同事
def notifyPerson(msg):
    contact_list = {
        "张三": "13824888888",
    }
    # 企业微信通知的同事
    mentioned_mobile_list = contact_list.values()
    body = {
        "msgtype": "text",
        "text": {
            "content": msg,
            "mentioned_mobile_list": list(mentioned_mobile_list),
        }
    }
    notifyResponseData = requests.post(NotifyConstVal.wx_send_url, json=body, headers=headers)
    print("发送企业微信消息：", msg)
    print("发送企业微信消息结果：", notifyResponseData.text)

    return


# Android编译打包apk
def packApk():
    os.chdir(AppConstVal.APP_PROJECT_PATH)
    iRet = subprocess.call('.\gradlew ' + AppConstVal.APP_GRADLE_BUILD_TYPE + ' --stacktrace', shell=True)  # 编译
    print("打包完成", iRet)


if __name__ == '__main__':
    print("控制台输入内容：{}".format(sys.argv))
    print("app信息：\n", appData)

    packApk()  # 打包
    uploadApk()  # 上传
    notifyPerson(NotifyConstVal.sendContent)  # 通知测试
