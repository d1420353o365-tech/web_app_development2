from flask import Blueprint

bp = Blueprint('plans', __name__, url_prefix='/plan')

@bp.route('/', methods=['GET'])
def index():
    """
    輸入：無
    處理：取得該用戶所有 Plan
    輸出：渲染 plans/index.html
    """
    pass

@bp.route('/generate', methods=['GET', 'POST'])
def generate():
    """
    輸入：GET 無, POST: goal, time_allocated
    處理：呼叫 AI 產出 schedule，並存為 Plan
    輸出：重導向至 plans/index.html
    """
    pass

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    輸入：計畫 ID
    處理：刪除特定 Plan
    輸出：重導向至 plans/index.html
    """
    pass
