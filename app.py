# _*_ coding:utf-8 _*_
import os
from flask import request, redirect, Flask, render_template

app = Flask(__name__)
static = "./static/"

SP = '''/'''


def isdir(path):
    return os.path.isdir(path)


def pre(arr, s):
    return [s + x + '/' for x in arr]


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect('/show?v=' + static)


@app.route('/show', methods=['GET', 'POST'])
def show():
    v = request.args.get("v")
    if v is None or not v.startswith(static):
        return redirect('/show?v=' + static)
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
            pwd=SP.join(v.split(SP)[2:]))
    else:
        return v


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9996, threaded=True)
