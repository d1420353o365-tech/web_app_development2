from datetime import datetime
from app.models import db

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    original_content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    quizes = db.relationship('Quiz', backref='note', lazy=True)

    @classmethod
    def create(cls, user_id, title, original_content, summary=None):
        """新增筆記"""
        try:
            new_note = cls(user_id=user_id, title=title, original_content=original_content, summary=summary)
            db.session.add(new_note)
            db.session.commit()
            return new_note
        except Exception as e:
            db.session.rollback()
            print(f"Error creating note: {e}")
            return None

    @classmethod
    def get_by_id(cls, note_id):
        """根據 ID 取得筆記"""
        try:
            return cls.query.get(note_id)
        except Exception as e:
            print(f"Error fetching note by id: {e}")
            return None

    @classmethod
    def get_all_by_user(cls, user_id):
        """取得某使用者的所有筆記"""
        try:
            return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()
        except Exception as e:
            print(f"Error fetching notes for user: {e}")
            return []

    def update(self, **kwargs):
        """更新筆記片段(如摘要)"""
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error updating note: {e}")
            return None

    def delete(self):
        """刪除筆記"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting note: {e}")
            return False
