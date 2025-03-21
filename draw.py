import pandas as pd
from collections import defaultdict
import json
from urllib.parse import urlparse

# 讀取 CSV
df = pd.read_csv("url.csv")

# 存儲網站結構的樹狀字典
tree = {}

# 建立遞迴插入函式，並新增 currentName
def insert_into_tree(path_parts, node, current_path=""):
    if not path_parts:
        return
    part = path_parts.pop(0)
    current_path += f"/{part}"
    if part not in node:
        node[part] = {"currentName": current_path, "children": {}}
    insert_into_tree(path_parts, node[part]["children"], current_path)

# 解析 URL 並插入樹狀結構
for url in df["URL"]:
    parsed = urlparse(url)
    path_parts = parsed.path.strip("/").split("/")
    insert_into_tree(path_parts, tree)

# 更新轉換為 JSON 格式函式
def convert_to_json(node):
    return [
        {"name": key, "currentName": value["currentName"], "children": convert_to_json(value["children"])}
        for key, value in node.items()
    ]

tree_json = {"name": "root", "children": convert_to_json(tree)}

# 存成 JSON 檔案
with open("site_structure.json", "w", encoding="utf-8") as f:
    json.dump(tree_json, f, indent=2, ensure_ascii=False)

print("JSON 轉換完成！")