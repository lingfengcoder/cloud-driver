import json
import sqlite3

db = "cloud_driver.db"


class BaseDao:
    path = ""

    def create_tb(self):
        return

    def __init__(self):
        sql = self.create_tb()
        self.exe_sql(sql)

    def exe_sql(self, sql, param=()):
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            cur.execute(sql, param)
            conn.commit()
            list = cur.fetchall()
            if len(list) > 0:
                # 将每一行转换为 Python 字典
                results = []
                for row in list:
                    result = {}
                    for i, col in enumerate(cur.description):
                        result[col[0]] = row[i]
                    results.append(result)
                # 将 Python 字典转换为 JSON 字符串
                # json_str = json.dumps(results)
                return results
            return list
