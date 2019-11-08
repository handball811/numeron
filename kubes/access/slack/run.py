import time
from slackbot.bot import Bot

from logging import getLogger
import logging

logger = getLogger(__name__)

BORDER_END_TIME = 60


def run():
	# 基本的に止めるつもりはない
	# ログを出して、続行するただし、前回の停止から1分いないなら、終了する
	bef_time = 0
	while time.time() - bef_time > BORDER_END_TIME:
		bef_time = time.time()
		try:
			logger.debug("run!")
			bot = Bot()
			bot.run()
		except:
			import traceback
			logger.warning(traceback.format_exc())


if __name__ == "__main__":
	# 簡単なログ設定を利用する
	logging.basicConfig(level=logging.DEBUG)
	logger.debug("activate bot")
	run()
	logger.debug("deactivate bot")