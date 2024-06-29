# **# robot**

> *为微信接入本地大模型*

## overview

> tips:特别鸣谢 GPT



### feature--已经实现的功能：

> 1. [X]  调用微信消息转发
> 2. [X]  可以调用语言模型对消息进行回复

### Future Feature--没有实现的功能：

> 1. [ ]  多模态的输入
> 2. [ ]  上下文



## 食用指南

准备工作：下载并安装[链接🔗](https://github.com/lich0821/WeChatFerry?tab=readme-ov-file)

终端：`pip install --upgrade wcferry` 安装[WeChatFerry](https://github.com/lich0821/WeChatFerry?tab=readme-ov-file)

> 注意：安装时要确保电脑微信版本必须为3.9.2.23记得取消自动更新  具体请看[WeChatFerry](https://github.com/lich0821/WeChatFerry?tab=readme-ov-file)

终端：`python path/tp/demo.py`

终端：`wcfhttp --cb http://localhost:9998/text` *（消息转发的地址 可以更改）*

```
#demo.py
from flask import Flask, request
import requests # type: ignore
import json

```

## 鸣谢

> * [ollama](https://ollama.com/)
> * [WeChatFerry](https://github.com/lich0821/WeChatFerry?tab=readme-ov-file)
