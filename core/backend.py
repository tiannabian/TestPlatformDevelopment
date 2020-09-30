#coding: utf-8
#author = hewangtong
#date = 2020/9/19
#111d38e8dafde5fe6770149abbd8a90d39    curl -u hewangtong:111d38e8dafde5fe6770149abbd8a90d39 http://stuq.ceshiren.com:8020/job/demo_01/build?token=hogwarts
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from jenkinsapi.jenkins import Jenkins

app = Flask(__name__)
#输出中文json
app.config["JSON_AS_ASCII"] = False

#使用了restful扩展扩展
api = Api(app)

#数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://python14:python14@stuq.ceshiren.com:23306/python14'

#使用sqlalchemy
db = SQLAlchemy(app)

#token管理
app.config['JWT_SECRET_KEY'] = 'ceshiren.com'  # Change this!
jwt = JWTManager(app)

jenkins = Jenkins(
    'http://stuq.ceshiren.com:8020/',
     username='hewangtong',
     password='111d38e8dafde5fe6770149abbd8a90d39'
)

class heyang(db.Model):
    #指定对应的表
    __tablename__ = 'heyang_demo'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class TestCase(db.Model):
    # 测试用例存储表结构
    __tablename__ = 'heyang_testcase'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    data = db.Column(db.String(1024), unique=False, nullable=False)

    def __repr__(self):
        return '<TestCase %r>' % self.name

class Task(db.Model):
    #jenkins任务列表
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    taskname = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.taskname

class TestCaseApi(Resource):
    #需要token验证
    @jwt_required
    def get(self):
        r = []
        #查询所有表内数据
        for t in TestCase.query.all():
            res = {}
            res['id'] = t.id
            res['name'] = t.name
            res['description'] = t.description
            res['data'] = t.data
            r.append(res)
        return r

    @jwt_required
    def post(self):
        t = TestCase(
            name = request.json['name'],
            description = request.json['description'],
            data = request.json['data']
        )
        db.session.add(t)
        db.session.commit()
        return {
            'msg': 'ok'
        }
    #done:更新用例
    @jwt_required
    def put(self):
        name = request.json.get('name', None)
        description = request.json.get('description', None)
        update_name = request.json.get('update_name', None)
        update_description = request.json.get('update_description', None)
        update_data = request.json.get('update_data', None)
        case = TestCase.query.filter_by(name = name, description = description).first()
        print(case)
        if case is None:
            return {
                'errodcode': 1,
                'errmsg': "用例数据为空"
            }
        else:
            case.name = update_name
            case.description = update_description
            case.data = update_data
            db.session.commit()
            return {
                'errcode':200,
                'errmsg':"更新成功"
            }

    #done:删除用例
    @jwt_required
    def delete(self):
        name = request.json.get('name', None)
        description = request.json.get('description', None)
        case = TestCase.query.filter_by(name = name, description = description).first()
        if case is None:
            return {
                'errodcode': 1,
                'errmsg': "数据为空，无法删除"
            }
        else:
            db.session.delete(case)
            db.session.commit()
            return {
                'errcode':2,
                'errmsg':"删除成功"
            }

class LoginApi(Resource):
    def get(self):
        heyang.query.all()
        return {'hello': 'world'}

    def post(self):
        #查询数据库
        username = request.json.get('username', None)
        #todo：通常密码不建议明文
        password = request.json.get('password', None)
        user = heyang.query.filter_by(username = username, password = password).first()
        #生成返回结构体
        if user is None:
            return jsonify(
                errcode=1,
                errmsg='用户名密码不正确'
            )
        else:
            return {
                'errcode': 0,
                'errmsg': 'ok',
                'username': user.username,
                #生成token,用于后续访问
                'token': create_access_token(identity = user.username)
            }
class RegisterApi(Resource):

    def post(self):
        """用户注册"""
        t = heyang(
            username = request.json['username'],
            password = request.json['password'],
            email = request.json['email']
        )
        db.session.add(t)
        db.session.commit()
        return {
            'errmsg': '注册成功'
        }

class TaskApi(Resource):
    #todo:查询所有接口
    @jwt_required
    def get(self):
        print(Task.query.all())
        r = []
        for i in Task.query.all():
            res = {}
            res['taskname'] = i.taskname
            r.append(res)
        return r

    @jwt_required
    def post(self):
        #todo:用例获取
        testcases = request.json.get('testcases', None)
        # done：调度jenkins
        jenkins['testcase_01'].invoke(
            securitytoken='111d38e8dafde5fe6770149abbd8a90d39',
            build_params={
                'testcases': testcases
            }
        )
        # done：将调度jenkins任务存入数据库中
        t = Task(
            taskname=jenkins['testcase_01'].get_last_completed_build().get_number()
        )
        db.session.add(t)
        db.session.commit()
        return {
            'errcode': 0,
            'errmsg': 'ok'
        }

        #todo:结果交给其他接口进行处理

class ResportApi(Resource):
    def get(self):
        pass

    def post(self):
        #todo:pull模式，主动从jenkins中拉取数据
        jenkins['testcase_01'].get_last_build().get_resultset()
        #todo:push模式，让jenkins node主动push到服务器
        #todo:把测试报告文件和测试报告数据保存
        pass

api.add_resource(TestCaseApi, '/testcase')
api.add_resource(LoginApi, '/login')
api.add_resource(TaskApi, '/task')
api.add_resource(RegisterApi, '/register')

if __name__ == '__main__':
    app.run(debug=True)