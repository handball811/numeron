
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply

from logging import getLogger

import os
import requests
import socket
import json

logger = getLogger(__name__)

SERVICE_HOST = os.environ["PROCESS_NETWORK_SERVICE_HOST"]
# SERVICE_HOST = os.environ["PROCESS_NETWORK_PORT"]

@respond_to(r"ヌメロン[!！]")
def start_numeron(message):
	logger.debug("request to start numeron!")
	print("message info:",message.body)
	reply_message = ["気が早いねぇ　kubernetesのデプロイチェック中だよ！"]
	print("current service host is",SERVICE_HOST)
	# ヌメロンサーバーに接続
	url = "http://"+SERVICE_HOST+":5000"
	# まずは、テーブルの内容を初期化する
	resp = requests.get(url+"/init")
	print("numeron init response is",resp.text)
	# その後、Userを取得する
	user_id = message.body["user"]
	user_name = "user_"+user_id
	service_name = "slack"
	print(user_id,user_name,service_name)
	# ユーザーの登録ヌメロン
	mutation = """
	mutation { 
	  createService(name:\"%s\")
	  {
	    uuid
	    name
	  }
	  createUser(
	  	name: \"%s\",
	  	serviceName: \"%s\"
	  	serviceUserId: \"%s\")
	  {
  	    uuid
  	    name
  	    serviceName
  	    serviceUserId
  	  }
	}
	""" % (service_name, user_name, service_name, user_id)

	resp = requests.post(url+"/graphql",data={
		"query":mutation
	})
	logger.debug("start connection to numeron")
	resp = json.loads(resp.text)
	print("numeron json response is",json.dumps(resp,indent=2,ensure_ascii=False))

	message.reply("\n".join(reply_message))
	message.react("+1")




