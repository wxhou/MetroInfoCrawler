"""
工具函数模块
"""

import time
import json
import requests


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://map.amap.com/subway/index.html",
    "Origin": "https://map.amap.com",
    "X-Requested-With": "XMLHttpRequest"
}

TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 2


class CrawlerError(Exception):
    pass


class NetworkError(CrawlerError):
    pass


class DataParseError(CrawlerError):
    pass


class FileIOError(CrawlerError):
    pass


def get_timestamp():
    return int(time.time() * 1000)


def safe_request(url, max_retries=MAX_RETRIES):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                print(f"请求超时，正在重试 ({attempt + 1}/{max_retries})...")
                time.sleep(RETRY_DELAY)
            else:
                raise NetworkError("请求超时，请检查网络连接")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"网络请求失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise DataParseError(f"数据解析失败: {str(e)}")


def save_json(data, filepath):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        raise FileIOError(f"文件写入失败: {str(e)}")


def format_color(hex_color):
    if hex_color and not hex_color.startswith('#'):
        return f"#{hex_color}"
    return hex_color
