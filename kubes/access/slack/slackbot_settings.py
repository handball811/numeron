# -*- coding: utf-8 -*-
import os

# トークンの指定
API_TOKEN = os.environ["SLACK_API_TOKEN"]

# 認識できない入力の際の応答の方法
DEFAULT_REPLY = "ごめんなさい、こちらで認識できませんでした..."

# 利用するスクリプトのプラグイン
PLUGINS = ['plugins']