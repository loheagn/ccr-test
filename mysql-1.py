import mysql.connector
from mysql.connector import Error
import random

# 连接MySQL数据库
try:
    connection = mysql.connector.connect(
        host='172.22.0.155',       # 数据库主机地址
        user='root',   # 数据库用户名
        password='123456' # 数据库密码
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # 创建“课程信息”数据库
        cursor.execute("CREATE DATABASE IF NOT EXISTS 课程信息;")
        cursor.execute("USE 课程信息;")

        # 创建学生信息表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS 学生信息 (
                学生ID INT PRIMARY KEY AUTO_INCREMENT,
                姓名 VARCHAR(255) NOT NULL,
                年龄 INT NOT NULL,
                性别 VARCHAR(1) NOT NULL
            );
        """)

        # 创建教师信息表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS 教师信息 (
                教师ID INT PRIMARY KEY AUTO_INCREMENT,
                姓名 VARCHAR(255) NOT NULL,
                职称 VARCHAR(255) NOT NULL
            );
        """)

        # 创建课程信息表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS 课程信息 (
                课程ID INT PRIMARY KEY AUTO_INCREMENT,
                课程名称 VARCHAR(255) NOT NULL,
                教师ID INT NOT NULL,
                FOREIGN KEY (教师ID) REFERENCES 教师信息(教师ID)
            );
        """)

        # 创建选课信息表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS 选课信息 (
                选课ID INT PRIMARY KEY AUTO_INCREMENT,
                学生ID INT NOT NULL,
                课程ID INT NOT NULL,
                分数 DECIMAL(5,2),
                FOREIGN KEY (学生ID) REFERENCES 学生信息(学生ID),
                FOREIGN KEY (课程ID) REFERENCES 课程信息(课程ID)
            );
        """)

        # 插入数据
        for _ in range(1000):
            cursor.execute("INSERT INTO 学生信息 (姓名, 年龄, 性别) VALUES (%s, %s, %s);", 
                           (f"学生{_}", random.randint(18, 25), random.choice(['男', '女'])))

        for _ in range(100):
            cursor.execute("INSERT INTO 教师信息 (姓名, 职称) VALUES (%s, %s);", 
                           (f"教师{_}", random.choice(['助教', '讲师', '副教授', '教授'])))

        for _ in range(200):
            cursor.execute("INSERT INTO 课程信息 (课程名称, 教师ID) VALUES (%s, %s);", 
                           (f"课程{_}", random.randint(1, 100)))

        for _ in range(4000):
            cursor.execute("INSERT INTO 选课信息 (学生ID, 课程ID, 分数) VALUES (%s, %s, %s);", 
                           (random.randint(1, 1000), random.randint(1, 200), round(random.uniform(60, 100), 2)))

        connection.commit()

        cursor.execute("FLUSH TABLES")

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")