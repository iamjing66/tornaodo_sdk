import logging
from logging import Logger

log_path = './out.log'
error_path = './error.log'
'''日志管理类 负责开发过程中的数据的追踪'''


def init_logger(logger_name):
    if logger_name not in Logger.manager.loggerDict:
        # 创建一个logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)  # 设置最低级别

        # 定义handler的输出格式
        df = '%Y-%m-%d %H:%M:%S'
        format_str = '[%(asctime)s]: %(name)s %(levelname)s %(lineno)s %(message)s'
        formatter = logging.Formatter(format_str, df)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(log_path, encoding='utf-8')  # 指定utf-8格式编码，避免输出的日志文本乱码
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)

        # 创建一个handler，用于将日志输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)

        # 给logger添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)

        # 创建一个handler，用于写入错误日志文件
        efh = logging.FileHandler(error_path, encoding='utf-8')  # 指定utf-8格式编码，避免输出的日志文本乱码
        efh.setLevel(logging.ERROR)
        efh.setFormatter(formatter)

        # 创建一个handler，用于将错误日志输出到控制台
        ech = logging.StreamHandler()
        ech.setLevel(logging.ERROR)
        ech.setFormatter(formatter)
        # 给logger添加handler
        logger.addHandler(efh)
        logger.addHandler(ech)

    logger = logging.getLogger(logger_name)
    return logger


logger = init_logger('wx_run_log')