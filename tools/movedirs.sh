#!/bin/bash

# 源目录
SOURCE_DIR="/root/nfs_client/"

# 目标目录
DESTINATION_DIR="/mnt/nfs_client/"

# 创建目的地目录，如果它不存在的话
mkdir -p "$DESTINATION_DIR"

# 移动每个目录
for dir in "$SOURCE_DIR"/*; do
  if [ -d "$dir" ]; then # 只有当它是一个目录时
    dirname=$(basename "$dir")
    rsync -a ${SOURCE_DIR}/${dirname}/ ${DESTINATION_DIR}/${dirname}/

    # # 使用 tar 通过管道移动目录
    # tar -C "$SOURCE_DIR" -cf - "$dirname" | tar -C "$DESTINATION_DIR" -xf -

    # 检查上条命令是否成功
    if [ $? -eq 0 ]; then
      # 删除原始目录
      echo ok "$dir"
    #   rm -rf "$dir"
    else
      echo "错误：无法移动 $dir 到 $DESTINATION_DIR"
      exit 1
    fi
  fi
done

echo "所有目录已从 $SOURCE_DIR 移动到 $DESTINATION_DIR."