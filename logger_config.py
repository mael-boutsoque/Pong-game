import logging
import colorlog

def setup_logger(name='app', level=logging.DEBUG, log_file='app.log'):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evite les handlers dupliqués
    if logger.handlers:
        return logger

    # Format de base
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler fichier
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Handler console avec couleurs
    color_formatter = colorlog.ColoredFormatter(
        fmt='%(log_color)s[%(asctime)s] [%(levelname)s]%(reset)s %(message)s',
        datefmt='%H:%M:%S',
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_red',
        }
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(color_formatter)
    logger.addHandler(console_handler)

    return logger
