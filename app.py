from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# sqlite数据库连接函数
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    # 返回一个简单的HTML页面，里面有指向 "/a" 的链接
    return redirect("http://127.0.0.1:5000/a")

# 登录页面
@app.route('/a', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']

        # 验证输入框内容是否为空
        if not username:
            flash('用户名不能为空')
            return redirect(url_for('login'))

        # 验证用户是否在数据库中
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user is None:
            flash('用户名不存在，请重新输入')
            return redirect(url_for('login'))

        # 验证通过，保存用户会话并跳转到页面b
        session['username'] = username
        return redirect(url_for('profile'))

    return render_template('a.html')


# 用户信息页面
@app.route('/b')
def profile():
    # 检查用户是否已登录
    if 'username' not in session:
        return redirect(url_for('login'))

    # 获取当前登录用户名
    username = session['username']
    return render_template('b.html', username=username)


# 退出登录
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
