# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem
from mysqldemo import settings


class MysqldemoPipeline:

    def __init__(self):
        self.connection = pymysql.connect(
            host=settings.MYSQL_HOST,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            db=settings.MYSQL_DATABASE,
            port=settings.MYSQL_PORT,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        try:
            sql = ("INSERT INTO `sdtdata` (`inner_id`,"
                   "`no`,"
                   "`table_code`,"
                   "`name`,"
                   "`release_date`,"
                   "`implement_date`,"
                   "`has_file`,"
                   "`is_validity`,"
                   "`views`,"
                   "`shop_url`,"
                   "`publish_dept`,"
                   "`pk_code`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            values = (
                item["inner_id"],
                item["no"],
                item["table_code"],
                item["name"],
                item["release_date"],
                item["implement_date"],
                item["has_file"],
                item["is_validity"],
                item["views"],
                item["shop_url"],
                item["publish_dept"],
                item["pk_code"]
            )
            self.cursor.execute(sql, values)
            self.connection.commit()
            return item
        except Exception as e:
            spider.logger.error(f"Error saving item to database: {e}")
            raise DropItem(f"Failed to save item {item}")

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()
