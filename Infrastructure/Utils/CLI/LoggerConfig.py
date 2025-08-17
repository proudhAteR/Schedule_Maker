from logging import *

SUCCESS_LEVEL_NUM = 25
addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")


def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kwargs)


Logger.success = success