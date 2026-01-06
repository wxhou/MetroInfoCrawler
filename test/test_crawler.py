import sys
sys.path.insert(0, 'g:/wxhouD/MetroInfoCrawler')

from src.crawler import MetroCrawler
from src.data_parser import DataParser
from src.utils import save_json
import os

crawler = MetroCrawler()
raw_data = crawler.get_metro_data('1100', 'beijing')
print('获取数据成功')

parser = DataParser()
subway_data = parser.convert_to_subway_format(raw_data)
print(f'解析成功，共{len(subway_data)}条线路')

output_dir = 'g:/wxhouD/MetroInfoCrawler/output'
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, '北京_subway.json')
save_json(subway_data, output_file)
print(f'保存成功: {output_file}')
