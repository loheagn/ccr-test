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
        cursor.execute("USE 课程信息;")
        # 定义一个查询语句，用于找到每门课程分数最高的5名学生
        query = """
        SELECT 
            kc.课程名称,
            s.姓名,
            xc.分数
        FROM 
            选课信息 xc
        JOIN 
            学生信息 s ON xc.学生ID = s.学生ID
        JOIN 
            课程信息 kc ON xc.课程ID = kc.课程ID
        WHERE 
            xc.分数 IS NOT NULL
        ORDER BY 
            kc.课程名称, xc.分数 DESC
        LIMIT 5;
        """

        # 执行查询
        cursor.execute(query)

        # 获取所有结果
        results = cursor.fetchall()

        # 打印结果
        for row in results:
            print(row)

        update_query = """
        UPDATE 选课信息
        SET 分数 = 90
        WHERE 分数 > 70;
        """
        
        # 执行更新语句
        cursor.execute(update_query)

      

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

        # 关闭游标和连接
        cursor.close()
        connection.close()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")