from flask import Blueprint

bp = Blueprint('quizes', __name__, url_prefix='/quiz')

@bp.route('/generate', methods=['GET', 'POST'])
def generate():
    """
    輸入：GET 無, POST: note_id (可選) 等測驗設定
    處理：呼叫 AI 產生測驗題目，存入 Quiz 與 QuizQuestion
    輸出：重導向至 quiz/<id> 開始測驗
    """
    pass

@bp.route('/<int:id>', methods=['GET', 'POST'])
def take(id):
    """
    輸入：GET 無, POST: 選項答案表單
    處理：GET 渲染測驗畫面。POST 比對答案，算總分，答錯的寫入 Mistake 表。
    輸出：POST 完成後重導向 quiz/<id>/result
    """
    pass

@bp.route('/<int:id>/result', methods=['GET'])
def result(id):
    """
    輸入：測驗 ID
    處理：取出此次測驗的分數與各題詳解
    輸出：渲染 quizes/result.html
    """
    pass

@bp.route('/mistakes', methods=['GET'])
def mistakes():
    """
    輸入：無
    處理：查詢該用戶所有的 Mistake 記錄並提供相關 QuizQuestion 的解釋
    輸出：渲染 quizes/mistakes.html
    """
    pass
