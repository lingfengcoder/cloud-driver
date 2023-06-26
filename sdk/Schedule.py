from sdk.log import logger
import time
import threading

class Schedule:
    job = {
        "1": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 23],
        "2": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 23],
        "3": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 23],
        "4": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 23],
        "5": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 23],
        "6": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 23],
        "7": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 23],
    }

    def __init__(self):
        self.SHUT_DOWN = False
        self.THREAD = None
        self.job = Schedule.job

    def get_job(self, x):
        return self.job[x]

    def check(self):
        w = time.strftime("%w")
        h = time.strftime("%H")
        list = self.get_job(w)
        logger.info("周 %s list=%s h=%s " % (w, list, h))
        return list.count(int(h)) > 0

    def daemon_check(self, callback):
        count = 0
        while (1):
            if self.SHUT_DOWN: break
            # callback(count % 20 == 0)
            callback(self.check())
            # count += 10
            time.sleep(5)
            # time.sleep(10 * 60)
    def time_work(self, callback):
        if self.THREAD == None or not self.THREAD.is_alive():
            self.THREAD = threading.Thread(target=self.daemon_check, args=[callback], daemon=True)
        self.THREAD.start()

    def shutdown(self):
        logger.info("schedule shutdown")
        self.SHUT_DOWN = True