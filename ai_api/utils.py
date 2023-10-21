import logging
import logging.handlers

def createLogger(logger_name):
    logger = logging.getLogger(logger_name)
 
    if len(logger.handlers) > 0:
        return logger
 
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(asctime)s - %(message)s')
    
    streamHandler = logging.StreamHandler()
    file_handler = logging.FileHandler(logger_name + '.log', mode='a')
    
    streamHandler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(streamHandler)
    logger.addHandler(file_handler)
    return logger