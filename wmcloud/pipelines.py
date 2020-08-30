# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json
import wmcloud.settings as settings;
import MySQLdb
import wmcloud.settings as settings

class JsonWriterPipeline:
    def __init__(self):
        # 参数初始化，可选实现
        self.file = open(settings.ROOT_PATH + "stock.json", 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line.encode('utf-8'))
        self.file.flush()
        return item

    def close_spider(self, spider):
        # 可选实现，当spider被关闭时，这个方法被调用
        self.file.close()

class MysqlWriterPipeline:
    def __init__(self):
        # 打开数据库连接
        self.db = MySQLdb.connect(settings.DB_SERVER_NAME, settings.DB_SERVER_USER_NAME, settings.DB_SERVER_PASSWORD, settings.DB_NAME, charset="utf8")
        sql = "truncate ticker"

        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        self.db.commit()

        pass

    def process_item(self, item, spider):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()

        # SQL 插入语句
        sql = "INSERT INTO `stock`.`ticker` (`symbol`, `total`, `percent`, `quality`, `industry`, `institution`, " \
              " `valuation`, `trend`, `quality_content`, `quality_tag`, `strategy_content`, `strategy_tag`) " \
              " VALUES ('{}', {}, {}, {}, {}, {}, {}, {},'{}', '{}', '{}', '{}')"
        sql = sql.format(item["symbol"], item["total"], item["percent"], item["quality"], item["industry"],
                         item["institution"], item["valuation"], item["trend"], item["quality_content"], item["quality_tag"],
                         item["strategy_content"], item["strategy_tag"])

        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        self.db.commit()

        return item

    def close_spider(self, spider):
        # 关闭数据库连接
        self.db.close()
        pass
