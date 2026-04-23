from flask import Blueprint

bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.route('/', methods=['GET', 'POST'])
def index():
    """
    輸入：GET 無, POST: 使用者輸入的提問文字
    處理：呼叫 AI 對話 API 取得回覆
    輸出：若為網頁重整則渲染 chat/chat.html。亦可設計成回傳 JSON 給前端 JS 處理。
    """
    pass
