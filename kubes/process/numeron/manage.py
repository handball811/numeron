from gateway import local_api_connection


# flask app の登録
app = local_api_connection.app

if __name__ == "__main__":
	# Flask の接続を行う
	local_api_connection.activate()