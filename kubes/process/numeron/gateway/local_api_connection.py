import os
from flask import Flask, jsonify
from flask_graphql import GraphQLView
# from .mysql_handler import mysql_handler_factory
from .models import models, connection_base, schema
from logging import getLogger

logger = getLogger(__name__)

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
handler = connection_base.mysql_handler_factory()

def activate(*args, **kwargs):
	logger.debug("connection gateway activated")
	app.run(*args, **kwargs)
	logger.debug("connection gateway deactivated")

@app.route("/init")
def init():
	# Tableの初期化
	logger.debug("creating tables")
	BASE = models.Base
	ENGINE = handler.get_engine()
	BASE.metadata.create_all(bind=ENGINE)
	"""
	# Serviceの作成
	logger.debug("creating services")
	slack_service = models.Service(name="slack")
	handler.add(slack_service)
	origin_service = models.Service(name="origin")
	handler.add(origin_service)

	# Userの作成
	logger.debug("creating users")
	user1 = models.User(name="sasakuna",service=slack_service,service_user_id="aaabbbccc")
	handler.add(user1)
	user2 = models.User(name="sasa",service=origin_service,service_user_id="aaabbbccc")
	handler.add(user2)
	#user3 = models.User(name="sasakuna",service=slack_service,service_user_id="aaabbbccc")
	#handler.add(user3)
	"""
	try:
		handler.commit()
	except:
		pass

	return jsonify({
		"message": "Init Done"
	})



@app.route("/")
def index():
	logger.debug ("access detected")
	# mysqlにアクセスしてみる
	# handler = mysql_handler_factory()

	resp = handler.exec("show tables;")
	print("database tables are",resp.fetchall())
	return jsonify({
		"message": "テストやで"
	})

app.add_url_rule(
	"/graphql",
	view_func=GraphQLView.as_view(
		"graphql",
		schema=schema.schema,
		graphql=True
	)
)

@app.teardown_appcontext
def shutdown_session(exception=None):
	handler.get_session().remove()

