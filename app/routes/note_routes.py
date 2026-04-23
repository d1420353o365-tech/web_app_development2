from flask import Blueprint

bp = Blueprint('notes', __name__, url_prefix='/notes')

@bp.route('/', methods=['GET'])
def index():
    """
    輸入：無
    處理：查詢該用戶所有 Note 紀錄
    輸出：渲染 notes/index.html
    """
    pass

@bp.route('/create', methods=['GET', 'POST'])
def create():
    """
    輸入：GET 無, POST: title, original_content
    處理：呼叫 AI 產生 summary，並建立 Note 資料
    輸出：成功則重導向至 notes/<id>，失敗則留在表單
    """
    pass

@bp.route('/<int:id>', methods=['GET'])
def detail(id):
    """
    輸入：筆記 ID (URL 參數)
    處理：從 DB 抓取 Note 詳情
    輸出：渲染 notes/detail.html，若找不到則 404
    """
    pass

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    輸入：筆記 ID
    處理：刪除指定的 Note
    輸出：重導向至 notes/index.html
    """
    pass
