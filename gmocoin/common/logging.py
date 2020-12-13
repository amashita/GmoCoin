#!python3
import inspect
import logging
from functools import wraps
from pathlib import Path


def get_logger() -> logging.Logger:
    """
    logging.Loggerを作成します。

    Returns:
        logger (logging.Logger):
            logging.Loggerのインスタンス
    """

    logger = logging.getLogger(__name__)
    return logger


def log(logger, log_func_args: bool = True):
    """
    デコレーターでloggerを引数にとるためのラッパー関数

    Args:
        logger (logging.Logger)
        log_func_args (bool)

    Returns:
        _decoratorの返り値
    """

    def _decorator(func):
        """
        デコレーターを使用する関数を引数とする

        Args:
            func (function)
        Returns:
            wrapperの返り値
        """

        # funcのメタデータを引き継ぐ
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            実際の処理を書くための関数

            Args:
                *args, **kwargs:
                    funcの引数

            Returns:
                funcの返り値
            """

            func_name = func.__name__
            file_name = inspect.getfile(func)
            line_no = inspect.currentframe().f_back.f_lineno
            real_func_info = f'{file_name}[{line_no}]:{func_name}'

            if log_func_args and (args is not None) and (len(args) != 0):
                args_str = ','.join([str(a) for a in args])
                message = f'[START] {real_func_info}({args_str})'
            else:
                message = f'[START] {real_func_info}()'
            logger.debug(message)

            try:
                # funcの実行
                ret = func(*args, **kwargs)
                if log_func_args and ret is not None:
                    logger.debug(f'[END] {real_func_info}() = {ret}')
                else:
                    logger.debug(f'[END] {real_func_info}()')
                return ret
            except Exception as err:
                # funcのエラーハンドリング
                logger.error(err, exc_info=True)
                logger.error(f'[KILLED] {real_func_info}()')
                raise

        return wrapper
    return _decorator
