from pymongo import MongoClient
from faker import Faker
import random

# 初始化 Faker 生成虚拟数据
fake = Faker()

# 连接到 MongoDB 实例
client = MongoClient('mongodb://localhost:27017/')

print('connected!')

# 创建或获取 "课程信息" 数据库
db = client['课程信息']

# 创建四个集合
students_collection = db['学生信息']
teachers_collection = db['教师信息']
courses_collection = db['课程信息']
enrollments_collection = db['选课信息']

# 生成并插入虚拟的学生信息
for _ in range(1000):
    student = {
        'name': fake.name(),
        'age': random.randint(18, 25),
        'email': fake.email()
    }
    students_collection.insert_one(student)

# 生成并插入虚拟的教师信息
for _ in range(100):
    teacher = {
        'name': fake.name(),
        'department': fake.job(),
        'email': fake.email()
    }
    teachers_collection.insert_one(teacher)

# 生成并插入虚拟的课程信息
for _ in range(100):
    course = {
        'title': fake.catch_phrase(),
        'description': fake.text(),
        'teacher_id': teachers_collection.aggregate([{'$sample': {'size': 1}}]).next()['_id']
    }
    courses_collection.insert_one(course)

# 生成并插入虚拟的选课信息
for _ in range(4000):
    enrollment = {
        'student_id': students_collection.aggregate([{'$sample': {'size': 1}}]).next()['_id'],
        'course_id': courses_collection.aggregate([{'$sample': {'size': 1}}]).next()['_id']
    }
    enrollments_collection.insert_one(enrollment)

print("数据生成并插入完成。")

for enrollment in enrollments_collection.find():
    enrollments_collection.update_one(
        {'_id': enrollment['_id']},
        {'$set': {'score': random.randint(0, 100)}}
    )