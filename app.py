import os
import uuid
from flask import Flask, request, redirect, url_for, flash, render_template, Response, session
from typing import Union, List
from werkzeug.datastructures import FileStorage

# The frontend directory path
FRONT_DIR = 'front'

# Define the upload folder inside the 'front' directory
UPLOAD_FOLDER = os.path.join(FRONT_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'json', 'xml', 'xls', 'xlsx'}

app = Flask(__name__, template_folder=os.path.join(FRONT_DIR, 'templates'), static_folder=os.path.join(FRONT_DIR, 'static'))
app.secret_key = 'super_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 20 * 1024 * 1024

# 登录凭据
LOGIN_CREDENTIALS = {
    'username': 'test',
    'password': '123456'
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == LOGIN_CREDENTIALS['username'] and password == LOGIN_CREDENTIALS['password']:
            session['logged_in'] = True
            flash('登录成功！')
            print(f"DEBUG: 用户 {username} 登录成功，session['logged_in'] = {session.get('logged_in')}")  # 调试日志
            return redirect(url_for('upload_file'))
        else:
            flash('用户名或密码错误！')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('您已成功登出。')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def upload_file() -> Union[Response, str]:
    print(f"DEBUG: 进入上传页面，session['logged_in'] = {session.get('logged_in')}")  # 调试日志
    if not session.get('logged_in'):
        flash('请先登录！')
        return redirect(url_for('login'))

    if request.method == 'POST':
        files: List[FileStorage] = request.files.getlist('files[]')
        
        if not files or all(f.filename == '' for f in files):
            flash('未选择任何文件')
            return redirect(request.url)

        if len(files) > 20:
            flash('一次最多只能上传 20 个文件')
            return redirect(request.url)
            
        successful_uploads = []
        failed_uploads = []

        for file in files:
            if file and allowed_file(file.filename):
                file.seek(0, os.SEEK_END)
                file_length = file.tell()
                file.seek(0, 0)
                if file_length > 20 * 1024 * 1024:
                    failed_uploads.append((file.filename, "文件超过 20MB"))
                    continue

                original_filename = file.filename
                extension = original_filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{uuid.uuid4()}.{extension}"
                
                upload_path = app.config['UPLOAD_FOLDER']
                os.makedirs(upload_path, exist_ok=True)
                file_path = os.path.join(upload_path, unique_filename)
                
                file.save(file_path)
                successful_uploads.append(original_filename)
            elif file.filename != '':
                failed_uploads.append((file.filename, "不允许的文件类型"))
        
        if successful_uploads:
            flash(f'成功上传 {len(successful_uploads)} 个文件: {", ".join(successful_uploads)}')
        if failed_uploads:
            for filename, reason in failed_uploads:
                flash(f'文件 "{filename}" 上传失败: {reason}')

        return redirect(request.url)

    return render_template('upload.html')

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)