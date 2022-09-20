
#该类作为常量类

# Android项目常量配置
class AppConstVal:
    APP_APK_PATH = "D:/ide/workspace/android3/android/android/build/outputs/apk/betaInternal/debug/android-beta-internal-debug.apk" #配置你的apk本地路径
    APP_ICON_PATH = "D:/ide/workspace/android3/android/android/src/main/res/mipmap-xxhdpi/ic_launcher.png" #配置你的应用图标本地路径
    APP_PROJECT_PATH = 'D:/ide/workspace/android3/android' #配置你的工程本地路径
    APP_GRADLE_BUILD_TYPE = ':android:assembleDebug' #配置你构建的包体类型

    APP_DATA_MAP = {"name": "进门财经",
                    "versionShort": "3.9.0501",
                    "build": "151",
                    "changelog": "bug修复",
                    }


# 内测分发平台常量配置 https://www.betaqr.com/
class BetaqrConstVal:
    baseUrl = "http://api.bq04.com/apps" #配置你构建的包体类型
    appFirId = "5df0984856767897f32"#配置你的测试平台id
    appBundleId = "cn.android.test" #配置你applicationId
    apiToken = "5c5e8234f1234564d11c43fc186b4"#配置你的测试平台token


# 通知平台常量配置
class NotifyConstVal:
    wx_send_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=123418d7-1234-1234-1324-1234f85fbaab"
    sendContent = """Android {} {}
    fir地址：http://firapp.android.cn/testandroid
    更新内容：{}
        """.format(AppConstVal.APP_DATA_MAP["name"], AppConstVal.APP_DATA_MAP["versionShort"], AppConstVal.APP_DATA_MAP["changelog"])