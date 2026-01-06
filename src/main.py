"""
主程序入口
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.crawler import MetroCrawler
from src.data_parser import DataParser
from src.utils import save_json, NetworkError, DataParseError


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    print("=" * 50)
    print("       高德地铁数据爬虫 v1.0")
    print("=" * 50)


def print_cities(cities):
    print("\n可用城市列表:")
    print("-" * 45)
    print(f"{'序号':<6}{'城市名称':<15}{'城市编码':<10}")
    print("-" * 45)
    for idx, city in enumerate(cities, 1):
        print(f"{idx:<6}{city.get('cityname', ''):<15}{city.get('adcode', ''):<10}")
    print("-" * 45)


def get_user_choice(cities):
    while True:
        try:
            choice = input("\n请输入城市序号、名称或编码 (输入 q 退出): ").strip()
            if choice.lower() == 'q':
                return None

            for city in cities:
                if choice == city.get('cityname') or choice == city.get('spell') or choice == city.get('adcode'):
                    return city

            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(cities):
                    return cities[idx - 1]

            print(f"无效选择，请输入 1-{len(cities)} 之间的数字、城市名称或城市编码")
        except KeyboardInterrupt:
            return None


def main():
    try:
        clear_screen()
        print_header()

        print("正在获取城市列表...")
        crawler = MetroCrawler()
        cities = crawler.get_city_list()

        if not cities:
            print("获取城市列表失败，请检查网络连接")
            return

        print_cities(cities)
        selected_city = get_user_choice(cities)

        if not selected_city:
            print("\n程序已退出")
            return

        city_name = selected_city.get('cityname', '')
        spell = selected_city.get('spell', '')
        adcode = selected_city.get('adcode', '')

        print(f"\n正在下载 [{city_name}] 地铁数据...")

        raw_data = crawler.get_metro_data(adcode, spell)

        if not raw_data:
            print("获取地铁数据失败")
            return

        print("正在解析数据...")

        parser = DataParser()
        subway_data = parser.convert_to_subway_format(raw_data)

        output_dir = os.path.dirname(sys.executable)
        if not output_dir:
            output_dir = os.path.dirname(os.path.dirname(__file__))
        
        output_file = os.path.join(output_dir, f"{city_name}_subway.json")
        save_json(subway_data, output_file)

        print(f"\n下载完成！")
        print(f"\n数据已保存至: {output_file}")

        line_count = len(subway_data)
        station_count = sum(len(line.get('station', [])) for line in subway_data)
        print(f"线路数量: {line_count}")
        print(f"站点数量: {station_count}")

    except NetworkError as e:
        print(f"\n网络错误: {e}")
    except DataParseError as e:
        print(f"\n数据解析错误: {e}")
    except Exception as e:
        print(f"\n发生错误: {e}")


if __name__ == "__main__":
    main()
