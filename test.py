from flask import Flask, render_template, request, abort, redirect
from flask_pymongo import PyMongo
from time import time
import os

app = Flask(__name__)

''' https://www.cnblogs.com/weijiangping/p/9358123.html '''
app.config['MONGO_DBNAME'] = 'todolist'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/t'
app.url_map.strict_slashes = False
mongo = PyMongo(app)


@app.route('/t')
def hello_world():
    return render_template('t.html')


@app.route('/oss/file/uploadFiles', methods=["GET", "POST"])
def uploadFiles():
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    f = request.files['file']
    # upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))
    upload_path = os.path.join(basepath, 'static/images/', f.filename)
    # 重复加1
    f.save(upload_path)
    if request.method == 'POST':
        add({'url': '/static/images/' + f.filename, 'name': f.filename})
        return '上传成功'
    else:
        return '上传失败'


class Todo(object):
    @classmethod
    def create_doc(cls, content):
        content.update({
            'created_at': time(),
            'is_finished': False,
            'finished_at': None
        })
        return content


def add(content):
    if not content:
        abort(400)
    mongo.db.commodity.insert(Todo.create_doc(content))
    return True


@app.route('/index')
def find():
    commodity = mongo.db.commodity.find()
    return render_template('index.html', todos=commodity)


@app.route('/delete/index')
def find():
    commodity = mongo.db.commodity.find()
    return render_template('delete.html', todos=commodity)

@app.route('/delete')
def delete():
    url = request.args.get('url', '')
    result = mongo.db.commodity.delete_one(
        {'url': url}
    )
    return redirect('/index/')


@app.route('/todo/<content>/finished')
def finish(content):
    result = mongo.db.todos.update_one(
        {'content':content},
        {
            '$set': {
                'is_finished': True,
                'finished_at': time()
            }
        }
    )
    return redirect('/index')


if __name__ == '__main__':
    app.run(host="0.0.0.0")

    '''
    问题记录：
    1.图片名称重复不可保存
    
    初版未做功能：
    1.商品展示界面
    2.商品删除和修改
    '''
    '''
    1.每次上传后刷新界面，不然新增的上传文件会上传失败
    2.商品备注可以修改图片名称，不要太长不然文字会溢出
    '''
    '''
    我是谁我在那我在做什么,我是谁我在那我在做什么,我是谁我在那我在做什么,我是谁我在那我在做什么,我是谁我在那我在做什么,我是谁我在那我在做什么,我是谁我在那我在做什么,我是谁我在那我在做什么
    '''