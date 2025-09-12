import os
import uuid
from flask import Flask, request, redirect, url_for, flash, render_template, Response
from typing import Union, List
from werkzeug.datastructures import FileStorage

# The frontend directory path
FRONT_DIR = 'front'

# Define the upload folder inside the 'front' directory
UPLOAD_FOLDER = os.path.join(FRONT_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'json', 'xml', 'xls', 'xlsx'}

app = Flask(__name__, template_folder=os.path.join(FRONT_DIR, 'templates'))

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 设置请求体最大为 400MB (20个文件 * 20MB) 来防止服务器过载
app.config['MAX_CONTENT_LENGTH'] = 20 * 20 * 1024 * 1024
# 需要设置一个密钥才能使用 flash 消息
app.secret_key = 'super_secret_key'

def allowed_file(filename: str) -> bool:
    """检查文件扩展名是否在允许的范围内。"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET', 'POST'])
def upload_file() -> Union[Response, str]:
    if request.method == 'POST':
        # 使用 getlist 获取所有名为 'files[]' 的文件
        files: List[FileStorage] = request.files.getlist('files[]')
        
        # --- 后端验证 ---
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
                # 检查单个文件大小 (20MB)
                # 我们通过移动到文件末尾来获取大小，然后再移回开头
                file.seek(0, os.SEEK_END)
                file_length = file.tell()
                file.seek(0, 0) # 移回文件开头，以便后续 .save() 操作
                if file_length > 20 * 1024 * 1024:
                    failed_uploads.append((file.filename, "文件超过 20MB"))
                    continue

                # 生成唯一文件名并保存
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
        
        # --- 根据上传结果显示提示消息 ---
        if successful_uploads:
            flash(f'成功上传 {len(successful_uploads)} 个文件: {", ".join(successful_uploads)}')
        if failed_uploads:
            for filename, reason in failed_uploads:
                flash(f'文件 "{filename}" 上传失败: {reason}')

        return redirect(request.url)

    # 对于 GET 请求，直接渲染上传表单页面
    return render_template('upload.html')

if __name__ == '__main__':
    # 确保应用可以在网络上被访问，例如，用于从其他设备进行测试
    app.run(host='0.0.0.0', port=5001, debug=True)
    
