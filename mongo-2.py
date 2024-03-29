from bson.son import SON

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

# 聚合查询：计算每门课程平均分最高的10名学生
pipeline = [
    {
        '$lookup': {
            'from': '学生信息',
            'localField': 'student_id',
            'foreignField': '_id',
            'as': 'student_info'
        }
    },
    {
        '$unwind': '$student_info'
    },
    {
        '$group': {
            '_id': {
                'course_id': '$course_id',
                'student_id': '$student_id',
                'student_name': '$student_info.name'
            },
            'average_score': {
                '$avg': '$score'
            }
        }
    },
    {
        '$sort': SON([('average_score', -1), ('_id.course_id', 1)])
    },
    {
        '$group': {
            '_id': '$_id.course_id',
            'top_students': {
                '$push': {
                    'student_id': '$_id.student_id',
                    'student_name': '$_id.student_name',
                    'average_score': '$average_score'
                }
            }
        }
    },
    {
        '$project': {
            'top_students': {
                '$slice': ['$top_students', 10]
            }
        }
    }
]

top_students_by_course = list(enrollments_collection.aggregate(pipeline))

# 输出结果
for course in top_students_by_course:
    print(f"Course ID: {course['_id']}")
    for student in course['top_students']:
        print(f"Student ID: {student['student_id']}, Name: {student['student_name']}, Average Score: {student['average_score']}")
    print()


# 更新70分以上的成绩为70
result = enrollments_collection.update_many(
    {'score': {'$gt': 70}},  # 匹配所有70分以上的文档
    {'$set': {'score': 70}}  # 将分数设置为70
)

print(f"更新了 {result.modified_count} 条文档。")
