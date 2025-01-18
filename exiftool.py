

import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
 
def remove_metadata(input_path):
    command = ["exiftool", "-all=", "-overwrite_original", input_path]
    try:
        subprocess.run(command, check=True)
        print(f"已成功去除 {input_path} 的元数据信息")
    except subprocess.CalledProcessError as e:
        print(f"处理失败: {input_path}，错误信息: {e}")
 
def process_files(input_folder, max_workers=5):
    file_paths = []
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            input_path = os.path.join(root, filename)
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.avi')):
                file_paths.append(input_path)
 
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(remove_metadata, path): path for path in file_paths}
        for future in as_completed(futures):
            path = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"处理文件 {path} 时发生错误: {e}")
 
if __name__ == "__main__":
    input_folder = input("请输入文件夹的路径: ")
    process_files(input_folder)