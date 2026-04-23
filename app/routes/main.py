from flask import Blueprint, render_template, session, redirect, url_for
from app.models.note import Note
from app.models.plan import Plan

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def index():
    """
    輸入：無 (依賴 Session)
    處理：未登入時可導向登入頁，登入則查詢使用者近期的學習數據與總覽。
    輸出：渲染 index.html (儀表板)
    """
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
        
    username = session.get('username', '學習者')
    
    # 取得最近的教學計畫與筆記，提供儀表板顯示
    recent_notes = Note.get_all_by_user(user_id)[:3]
    recent_plans = Plan.get_all_by_user(user_id)[:3]
    
    return render_template('index.html', username=username, notes=recent_notes, plans=recent_plans)
