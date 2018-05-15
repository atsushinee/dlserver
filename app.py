# _*_ coding:utf-8 _*_
import os
from flask import request, redirect, Flask, render_template

app = Flask(__name__)
static = "./static/"

SP = '''/'''
spe_dir = 'lichun'
key = 'lc'


def isdir(path):
    return os.path.isdir(path)


def pre(arr, s):
    return [s + x + '/' for x in arr]


def to_redirect(msg, v=static):
    return '/show?v=%s&msg=%s' % (v, msg)


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect('/show?v=' + static)


@app.route('/show', methods=['GET', 'POST'])
def show():
    v = request.args.get("v")
    msg = request.args.get("msg")
    if v is not None and spe_dir in v and request.args.get('key') != key:
        return redirect(to_redirect('权限不足!'))

    if v is None or not v.startswith(static):
        return redirect(to_redirect("Bad request!"))
    if os.path.isdir(v):
        a = os.listdir(v)
        print(v)
        return render_template(
            "index.html",
            dir=a,
            h=pre(a, v),
            isdir=isdir,
            pre=SP.join(v.split(SP)[0:-2]) + SP,
            haspre=v != static,
            pwd=SP.join(v.split(SP)[2:]),
            v=v,
            msg=msg)
    else:
        return v


@app.route('/upload', methods=['POST'])
def upload():
    v = request.args["v"]
    if request.method == 'POST':
        f = request.files['file']
        if f.filename == '':
            return redirect(to_redirect('文件名不可为空!'))
        f.save(v + f.filename)
        if spe_dir in v:
            return redirect(
                to_redirect("文件[%s]上传成功!%s" % (f.filename, '&key=%s' % key), v))
        else:
            return redirect(to_redirect("文件[%s]上传成功!" % f.filename, v))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9996, threaded=True)
