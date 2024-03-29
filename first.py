import redis
import random
import string

keysList = []

# 连接本地Redis服务器，默认端口是6379
r = redis.Redis(host='localhost', port=6379)

# 定义一个辅助函数，用于生成随机字符串
def get_random_string(length=10):
    # 选择所有的ascii字母和数字
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

# 写入1000个随机键值对
for _ in range(1000):
    # 使用随机生成的键和值
    key = get_random_string(10)
    value = get_random_string(10)
    r.set(key, value)
    keysList.append(key)

print("1000 random key-value pairs have been inserted into Redis.")
print(keysList)