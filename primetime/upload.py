# hdfs dfs -mkdir -p /nielsen/tv1
import os
import subprocess

# 로컬 폴더 경로와 HDFS 업로드 경로 지정
local_folder = "/home/ubuntu/damf2/nielsen/data/tv3"  # 여기에 csv 파일들이 있는 폴더 경로 작성
hdfs_target_folder = "/nielsen/tv3"  # 원하는 HDFS 경로

# 파일 반복하면서 업로드
for filename in os.listdir(local_folder):
    if filename.endswith(".csv"):
        local_path = os.path.join(local_folder, filename)
        hdfs_path = os.path.join(hdfs_target_folder, filename)
        
        # 업로드 명령어 실행
        result = subprocess.run(["hdfs", "dfs", "-put", "-f", local_path, hdfs_path])
        
        if result.returncode == 0:
            print(f"✅ Uploaded: {filename}")
        else:
            print(f"❌ Failed to upload: {filename}")