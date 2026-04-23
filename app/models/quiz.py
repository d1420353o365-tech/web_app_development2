from datetime import datetime
from app.models import db

class Quiz(db.Model):
    __tablename__ = 'quizes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'), nullable=True)
    total_score = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    questions = db.relationship('QuizQuestion', backref='quiz', lazy=True, cascade="all, delete-orphan")

    @classmethod
    def create(cls, user_id, note_id=None, total_score=None):
        """建立測驗單"""
        try:
            new_quiz = cls(user_id=user_id, note_id=note_id, total_score=total_score)
            db.session.add(new_quiz)
            db.session.commit()
            return new_quiz
        except Exception as e:
            db.session.rollback()
            print(f"Error creating quiz: {e}")
            return None

    @classmethod
    def get_by_id(cls, quiz_id):
        """取得測驗單"""
        try:
            return cls.query.get(quiz_id)
        except Exception as e:
            print(f"Error fetching quiz by id: {e}")
            return None

    @classmethod
    def get_all_by_user(cls, user_id):
        """取得某使用者的所有歷史測驗"""
        try:
            return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()
        except Exception as e:
            print(f"Error fetching quizes: {e}")
            return []

    def update(self, **kwargs):
        """更新測驗資料(如總分)"""
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error updating quiz: {e}")
            return None

    def delete(self):
        """刪除測驗單"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting quiz: {e}")
            return False


class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizes.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    options_json = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.String(200), nullable=False)
    explanation = db.Column(db.Text, nullable=True)

    mistakes = db.relationship('Mistake', backref='question', lazy=True)

    @classmethod
    def create(cls, quiz_id, question_text, options_json, correct_answer, explanation=None):
        """建立題目"""
        try:
            new_q = cls(quiz_id=quiz_id, question_text=question_text, options_json=options_json, correct_answer=correct_answer, explanation=explanation)
            db.session.add(new_q)
            db.session.commit()
            return new_q
        except Exception as e:
            db.session.rollback()
            print(f"Error creating quiz question: {e}")
            return None

    @classmethod
    def get_by_id(cls, q_id):
        """取得單一題目"""
        try:
            return cls.query.get(q_id)
        except Exception as e:
            print(f"Error fetching question by id: {e}")
            return None


class Mistake(db.Model):
    __tablename__ = 'mistakes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_question_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.id'), nullable=False)
    user_answer = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, user_id, quiz_question_id, user_answer):
        """建立錯題紀錄"""
        try:
            new_mistake = cls(user_id=user_id, quiz_question_id=quiz_question_id, user_answer=user_answer)
            db.session.add(new_mistake)
            db.session.commit()
            return new_mistake
        except Exception as e:
            db.session.rollback()
            print(f"Error creating mistake: {e}")
            return None

    @classmethod
    def get_all_by_user(cls, user_id):
        """獲取該用戶的錯題本"""
        try:
            return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()
        except Exception as e:
            print(f"Error fetching mistakes: {e}")
            return []
