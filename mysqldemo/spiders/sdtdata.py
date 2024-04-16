from typing import Iterable

import scrapy
import json
from scrapy import Request
from mysqldemo.items import SdtdataItem


class SdtdataSpider(scrapy.Spider):
    name = "sdtdata"
    allowed_domains = ["sdtdata.com"]
    index_url = "http://www.sdtdata.com/"
    search_url = "https://sdtdata.com/fx/foodcodex?p=tsLibList&s=fcv1&act=doSearch"
    search_params = {
        "isCurrent": "2",
        "isCompulsive": "2",
        "pageNum": "1"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Cookie": "JSESSIONID=aaaD-LXWK949OaY9EAC5y"
    }

    def start_requests(self) -> Iterable[Request]:
        yield scrapy.FormRequest(url=self.search_url,
                                 headers=self.headers,
                                 method="POST",
                                 encoding='utf-8',
                                 formdata=self.search_params,
                                 callback=self.parse_search)

    def parse_search(self, response):
        body = json.loads(response.text)
        if body["retCode"] != "200":
            print(f"response error, retCode:{response.text['retCode']}")
            return None

        for body_item in body["data"]["datas"]:
            """
                {
                    "TS_SHOP_URL": "",
                    "TS_IMPLEMENT_DATE": "2023-05-11",
                    "TS_HAS_FILE": "yes",
                    "$ROW_NUM$": "2",
                    "TS_NO": "GB 2763.1-2022",
                    "TS_NAME": "食品安全国家标准 食品中2,4-滴丁酸钠盐等112种农药最大残留限量",
                    "$TABLE_CODE$": "V_FC_TS_LIB",
                    "TS_VIEWS": "11670",
                    "$PK_CODE$": "194155`yes",
                    "TS_PUBLISH_DEPT": "国家卫生健康委&农业农村部&市场监管总局",
                    "TS_VALIDITY": "现行",
                    "TS_ID": "194155",
                    "TS_RELEASE_DATE": "2022-11-11"
                }
            """
            item = SdtdataItem()
            item["inner_id"] = body_item["TS_ID"]
            item["no"] = body_item["TS_NO"]
            item["table_code"] = body_item["$TABLE_CODE$"]
            item["name"] = body_item["TS_NAME"]
            item["release_date"] = body_item["TS_RELEASE_DATE"]
            item["implement_date"] = body_item["TS_IMPLEMENT_DATE"]
            item["has_file"] = body_item["TS_HAS_FILE"]
            item["is_validity"] = body_item["TS_VALIDITY"]
            item["views"] = body_item["TS_VIEWS"]
            item["shop_url"] = body_item["TS_SHOP_URL"]
            item["publish_dept"] = body_item["TS_PUBLISH_DEPT"]
            item["pk_code"] = body_item["$PK_CODE$"]

            yield item
