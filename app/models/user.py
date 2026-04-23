from datetime import datetime
from app.models import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    notes = db.relationship('Note', backref='author', lazy=True)
    plans = db.relationship('Plan', backref='user', lazy=True)
    quizes = db.relationship('Quiz', backref='user', lazy=True)
    mistakes = db.relationship('Mistake', backref='user', lazy=True)

    @classmethod
    def create(cls, username, email, password_hash):
        """新增使用者"""
        try:
            new_user = cls(username=username, email=email, password_hash=password_hash)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            return None

    @classmethod
    def get_by_id(cls, user_id):
        """根據 ID 取得使用者"""
        try:
            return cls.query.get(user_id)
        except Exception as e:
            print(f"Error fetching user by id: {e}")
            return None

    @classmethod
    def get_by_email(cls, email):
        """根據 Email 取得使用者，用於登入驗證"""
        try:
            return cls.query.filter_by(email=email).first()
        except Exception as e:
            print(f"Error fetching user by email: {e}")
            return None

    def update(self, **kwargs):
        """更新使用者資料"""
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error updating user: {e}")
            return None

    def delete(self):
        """刪除使用者"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting user: {e}")
            return False
