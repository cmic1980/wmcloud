import scrapy
import json
import tushare as ts
from wmcloud.items import WmcloudItem


class SpWmCloud(scrapy.Spider):
    name = "sp_wmcloud"
    allowed_domains = ["gw.wmcloud.com"]
    start_urls = ["https://gw.wmcloud.com/huaanstockdiag/diagnosis/overall?ticker=688520"]

    root_url = "https://gw.wmcloud.com/huaanstockdiag/diagnosis/overall?ticker="

    def __init__(self):
        ts.set_token('c82b0e129f73c37ae7a7f225b67f00ae2ab175f9373973aaba29feff')
        pro = ts.pro_api()
        data = pro.stock_basic(exchange='', list_status='L', fields='symbol')
        for symbol in data["symbol"]:
            start_url = self.root_url + symbol
            self.start_urls.append(start_url)
            print(symbol)
        pass

    def parse(self, response):
        body = response.body.decode('utf-8')
        item = WmcloudItem()
        symbol = response.url.replace(self.root_url, "")
        item["symbol"] = symbol

        json_object = json.loads(body)
        data = json_object["data"]
        overview = data["overview"]

        item["total"] = overview["total"]
        item["percent"] = overview["percent"]
        item["quality"] = overview["quality"]
        item["industry"] = overview["industry"]
        item["institution"] = overview["institution"]
        item["valuation"] = overview["valuation"]
        item["trend"] = overview["trend"]

        quality_content = ""
        quality = data["quality"]
        quality_messages = quality["msgs"]
        for quality_message in quality_messages:
            for line in quality_message:
                quality_content = quality_content + line["str"] + "\n"
        item["quality_content"] = quality_content

        quality_tags_content = ""
        quality_tags = quality["tags"]
        for quality_tag in quality_tags:
            quality_tags_content = quality_tags_content + quality_tag + ", "
            pass
        item["quality_tag"] = quality_tags_content.strip(", ")


        strategy_content = ""
        strategy = data["strategy"]
        strategy_messages = strategy["msgs"]
        for strategy_message in strategy_messages:
            for line in strategy_message:
                strategy_content = strategy_content + line["str"] + "\n"
            pass
        item["strategy_content"] = strategy_content

        strategy_tags_content = ""
        strategy_tags = strategy["tags"]
        for strategy_tag in strategy_tags:
            strategy_tags_content = strategy_tags_content + strategy_tag + ", "
            pass
        item["strategy_tag"] = strategy_tags_content.strip(", ")

        print("parse item: " + symbol)
        yield item


