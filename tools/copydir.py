import subprocess
import os

# 需要复制的源目录路径
source_dir = "/mnt/nfs_client/this-cp-id-for-mysql-2/"

# 目标目录的基本路径
target_base_path = "/mnt/nfs_client/this-cp-id-for-mysql-2-id-"

# 确保源目录存在
if not os.path.exists(source_dir):
    print(f"Error: Source directory {source_dir} does not exist.")
    exit(1)

# 使用rsync复制目录
for i in range(1, 11):
    # 创建目标目录路径
    target_dir = f"{target_base_path}{i}/"
    
    # 构造rsync命令
    rsync_command = ["rsync", "-a", source_dir, target_dir]

    # 调用rsync命令
    print(f"Copying to {target_dir}...")
    result = subprocess.run(rsync_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # 检查命令是否执行成功
    if result.returncode == 0:
        print(f"Successfully copied to {target_dir}")
    else:
        print(f"Error copying to {target_dir}: {result.stderr.decode('utf-8')}")

print("Done.")