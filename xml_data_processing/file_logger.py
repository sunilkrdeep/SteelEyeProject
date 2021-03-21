import logging


class file_logger():
    """"
    This is logger class which logs all event in log file.
    """
    def __init__(self, logdir, logfile):
        self.logdir = logdir
        self.logfile = logfile

    def logger(self):
        logs = self.logdir + self.logfile
        logging.basicConfig(filename=logs, format='%(asctime)s %(message)s',
                            datefmt='%m-%d-%Y %I:%M:%S %p', level=logging.INFO)
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        return logger
