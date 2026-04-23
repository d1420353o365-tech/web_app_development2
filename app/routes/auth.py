from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    輸入：GET 無, POST: email, password
    處理：驗證信箱密碼，設定 User Session
    輸出：成功導回首頁，失敗回到 login.html
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('請填寫信箱與密碼！', 'warning')
            return redirect(url_for('auth.login'))
            
        user = User.get_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'歡迎回來，{user.username}！', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('信箱或密碼錯誤，請重新輸入。', 'danger')
            return redirect(url_for('auth.login'))
            
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    輸入：GET 無, POST: username, email, password
    處理：密碼加密後建立 User Model
    輸出：成功導向 login，失敗回到 register.html
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not username or not email or not password:
            flash('所有欄位皆為必填項。', 'warning')
            return redirect(url_for('auth.register'))
            
        if User.get_by_email(email):
            flash('此信箱已被註冊過！', 'danger')
            return redirect(url_for('auth.register'))
            
        password_hash = generate_password_hash(password)
        new_user = User.create(username=username, email=email, password_hash=password_hash)
        
        if new_user:
            flash('會員註冊成功！請登入您的帳號以繼續。', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('建立帳號時發生錯誤，請稍後再試。', 'danger')
            return redirect(url_for('auth.register'))
            
    return render_template('auth/register.html')

@bp.route('/logout', methods=['GET'])
def logout():
    """
    輸入：無
    處理：清除 Session
    輸出：重導向至 login.html
    """
    session.clear()
    flash('您已成功登出。', 'info')
    return redirect(url_for('auth.login'))
