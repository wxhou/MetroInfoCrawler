"""
数据解析模块 - 将高德API数据转换为subwayData.js格式
"""

from src.utils import format_color


class DataParser:
    def __init__(self):
        self.station_coords = {}

    def convert_to_subway_format(self, raw_data):
        lines = []
        lines_data = raw_data.get("l", [])

        for line_idx, line_data in enumerate(lines_data, start=1):
            line = self._convert_line(line_data, line_idx, lines_data)
            lines.append(line)

        return lines

    def _convert_line(self, line_data, line_idx, all_lines):
        line_name = line_data.get("ln", "")
        line_id = line_data.get("ls", "")
        line_color = format_color(line_data.get("cl", ""))
        stations_data = line_data.get("st", [])
        pixel_coords = line_data.get("c", [])

        line = {
            "name": line_name,
            "id": line_idx,
            "coords": self._convert_coords(pixel_coords, line_data, all_lines),
            "lineStyle": {
                "normal": {
                    "color": line_color
                }
            },
            "station": self._convert_stations(stations_data, line_id, all_lines)
        }

        return line

    def _convert_coords(self, pixel_coords, line_data, all_lines):
        """从站点的真实GPS坐标构建线路坐标数组"""
        coords = []
        stations_data = line_data.get("st", [])
        
        for station_data in stations_data:
            coord_str = station_data.get("sl", "")
            geo = self._parse_coords(coord_str)
            if geo and geo != [0, 0]:
                coords.append(geo)
        
        return coords

    def _convert_stations(self, stations_data, line_id, all_lines):
        stations = []
        for station_data in stations_data:
            station = self._convert_station(station_data, line_id, all_lines)
            stations.append(station)
        return stations

    def _convert_station(self, station_data, line_id, all_lines):
        station_name = station_data.get("n", "")
        coord_str = station_data.get("sl", "")
        is_transfer = station_data.get("t", "0") == "1"
        station_id = station_data.get("sid", "")

        geo = self._parse_coords(coord_str)

        station = {
            "name": station_name,
            "isHC": is_transfer,
            "geo": geo
        }

        if is_transfer:
            geo1 = self._get_transfer_station_coord(station_data, line_id, all_lines)
            if geo1:
                station["geo1"] = geo1

        return station

    def _parse_coords(self, coord_str):
        if not coord_str:
            return [0, 0]
        parts = coord_str.split(',')
        if len(parts) >= 2:
            try:
                return [float(parts[0]), float(parts[1])]
            except ValueError:
                return [0, 0]
        return [0, 0]

    def _get_transfer_station_coord(self, station_data, line_id, all_lines):
        station_name = station_data.get("n", "")

        for other_line in all_lines:
            if other_line.get("ls") == line_id:
                continue
            other_stations = other_line.get("st", [])
            for other_station in other_stations:
                if other_station.get("n") == station_name:
                    other_coord = other_station.get("sl", "")
                    return self._parse_coords(other_coord)

        return None
