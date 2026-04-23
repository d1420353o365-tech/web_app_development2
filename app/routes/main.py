from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def index():
    """
    輸入：無 (依賴 Session)
    處理：未登入時可導向登入頁，登入則查詢使用者近期的學習數據與總覽。
    輸出：渲染 index.html (儀表板)
    """
    pass
