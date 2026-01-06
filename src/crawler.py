"""
爬虫核心模块
"""

from src.utils import safe_request, get_timestamp


class MetroCrawler:
    def __init__(self):
        self.base_url = "https://map.amap.com/service/subway"

    def get_city_list(self):
        url = f"{self.base_url}?_={get_timestamp()}&srhdata=citylist.json"
        result = safe_request(url)
        return result.get("citylist", [])

    def get_metro_data(self, adcode, spell):
        url = f"{self.base_url}?_={get_timestamp()}&srhdata={adcode}_drw_{spell}.json"
        return safe_request(url)
