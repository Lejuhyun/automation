from hdfs import InsecureClient
import os # 운영체제
client = InsecureClient('http://localhost:9870', user= 'ubuntu')
# client.makedirs('/input/logs') input 폴더에 logs 라는 폴더 생성하기

local_file_path= '/home/ubuntu/damf2/data/bitcoin/'# logs 폴더의 경로
hdfs_file_path= '/input/bitcoin/' # hdfs 경로

local_files = os.listdir(local_file_path) # 모든 로컬 파일들을 가져오기

for file_name in local_files:
    if not client.content(hdfs_file_path + file_name, strict = False):
        client.upload(hdfs_file_path+file_name, local_file_path+file_name)
    # else:
        # pass   