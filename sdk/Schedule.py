from log import logger
import time
import threading


class Schedule:
    job = {
        "1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 23, 24],
        "2": [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 23, 24],
        "3": [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 23, 24],
        "4": [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 23, 24],
        "5": [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 23, 24],
        "6": [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 23, 24],
        "7": [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 23, 24],
    }

    def get_job(self, x):
        return self.job[x]

    def check(self):
        w = time.strftime("%w")
        h = time.strftime("%H")
        logger.info("周 %s" % (schedule.get_job(w)))
        list = schedule.get_job(w)
        if list.count(h) < 0:
            return False
        return True

    def deamon_check(self, callback):
        count = 0
        while (1):
            # if count % 20 == 0:
            #     callback(False)
            # else:
            #     callback(True)
            if not self.check():
                callback(False)
            else:
                callback(True)
            count += 10
            # time.sleep(5)
            time.sleep(10 * 60)

    def schedule(self, callback):
        threading.Thread(target=self.deamon_check, args=[callback]).start()
schedule = Schedule()
