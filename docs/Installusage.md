# 安装使用


## 环境配置
- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+


## PIP安装
在终端运行如下命令即可(请保证python在环境变量中):
```sh
pip install pikachuwechat --upgrade
```


## 源代码安装

#### 在线安装
运行如下命令即可在线安装:
```sh
pip install git+https://github.com/CharlesPikachu/pikachuwechat.git@master
```

#### 离线安装
利用如下命令下载videodl源代码到本地:
```sh
git clone https://github.com/CharlesPikachu/pikachuwechat.git
```
接着, 切到musicdl目录下:
```sh
cd pikachuwechat
```
最后运行如下命令进行安装:
```sh
python setup.py install
```


## 快速开始
安装完成后，简单写一段脚本：
```python
import random
from pikachuwechat import pikachuwechat

wechat_helper = pikachuwechat.pikachuwechat()
wechat_helper.execute(func_type="AntiWithdrawal", config={})
```
即可运行我们的微信小助手。各参数含义如下:
```
func_type: 功能类型, 目前支持AntiWithdrawal, AnalysisFriends和AutoReply
config: 实例化对应功能的配置文件, 例如在消息自动回复功能(func_type="AutoReply")中, 你可以定义config={'auto_reply_rules': {'皮卡丘': '恭喜你, 答对暗号啦~'}}来指定自动回复的规则。
```