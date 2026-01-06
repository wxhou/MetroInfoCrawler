# MetroInfoCrawler

高德地图地铁数据爬虫工具，从高德地图 API 获取中国各城市的地铁线路和站点数据，并转换为标准 JSON 格式。

## 功能特性

- 获取支持地铁的中国城市列表
- 爬取指定城市的地铁线路和站点数据
- 自动转换为 subwayData.js 标准格式
- 支持像素坐标到经纬度坐标转换
- 完善的异常处理和重试机制

## 技术栈

- Python 3.8+
- requests - HTTP 请求库
- PyInstaller - 打包工具

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python src/main.py
```

### 打包为可执行文件

```bash
pyinstaller --onefile --name MetroCrawler src/main.py
```

## 项目结构

```
MetroInfoCrawler/
├── src/
│   ├── main.py              # 程序入口，CLI 界面
│   ├── crawler.py           # 爬虫核心逻辑
│   ├── data_parser.py       # 数据解析/格式转换模块
│   └── utils.py             # 工具函数
├── output/                  # 数据输出目录
├── openspec/                # 项目规范文档
│   ├── project.md           # 项目上下文
│   └── AGENTS.md            # AI 助手规范
├── test/                    # 测试文件
├── requirements.txt
└── README.md
```

## 输出格式

爬取的数据保存为 `{城市名称}_subway.json`，格式如下：

```json
[
  {
    "name": "1号线",
    "id": 1,
    "coords": [[经度, 纬度], ...],
    "lineStyle": {
      "normal": {
        "color": "#0077c9"
      }
    },
    "station": [
      {
        "name": "站点名称",
        "isHC": false,
        "geo": [经度, 纬度]
      },
      {
        "name": "换乘站名称",
        "isHC": true,
        "geo": [经度, 纬度],
        "geo1": [经度, 纬度]
      }
    ]
  }
]
```

## License

MIT
