# 文件路径: .github/scripts/sync_json.py
import json
import os

# 获取当前工作目录 (GitHub Action 运行时即为仓库根目录)
BASE_DIR = os.getcwd()

# === 修改点：路径不需要包含仓库名 Icons ===
JSON_FILE_PATH = os.path.join(BASE_DIR, 'Emby/icons.json')
IMAGES_DIR = os.path.join(BASE_DIR, 'Emby/icons')

def sync_icons():
    if not os.path.exists(JSON_FILE_PATH):
        print(f"错误: 找不到 JSON 文件: {JSON_FILE_PATH}")
        # 这里打印一下当前目录结构帮助排错
        print(f"当前目录下文件: {os.listdir(BASE_DIR)}")
        return

    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_count = len(data.get('icons', []))
    valid_icons = []

    print(f"正在读取目录: {IMAGES_DIR}")
    
    # 遍历 JSON 中的 icons
    for icon in data.get('icons', []):
        file_name = f"{icon['name']}.png"
        file_path = os.path.join(IMAGES_DIR, file_name)
        
        # 检查图片是否存在
        if os.path.exists(file_path):
            valid_icons.append(icon)
        else:
            print(f"[-] 图片已删除，移除条目: {icon['name']}")

    # 如果有变动，写入文件
    if len(valid_icons) < original_count:
        data['icons'] = valid_icons
        with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
            # indent=2 保持缩进，ensure_ascii=False 保持中文可读
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"更新完成，移除了 {original_count - len(valid_icons)} 个条目。")
    else:
        print("JSON 与图片文件夹一致，无需修改。")

if __name__ == "__main__":
    sync_icons()
