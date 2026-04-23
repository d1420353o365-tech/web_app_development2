from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    輸入：GET 無, POST: email, password
    處理：驗證信箱密碼，設定 User Session
    輸出：成功導回首頁，失敗回到 login.html
    """
    pass

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    輸入：GET 無, POST: username, email, password
    處理：密碼加密後建立 User Model
    輸出：成功導向 login，失敗回到 register.html
    """
    pass

@bp.route('/logout', methods=['GET'])
def logout():
    """
    輸入：無
    處理：清除 Session
    輸出：重導向至 login.html
    """
    pass
