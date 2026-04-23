from datetime import datetime
from app.models import db

class Plan(db.Model):
    __tablename__ = 'plans'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    goal = db.Column(db.String(200), nullable=False)
    time_allocated = db.Column(db.Integer, nullable=False) # In minutes
    schedule_content = db.Column(db.Text, nullable=False) # JSON or text representing the plan
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, user_id, goal, time_allocated, schedule_content):
        """新增學習計畫"""
        try:
            new_plan = cls(user_id=user_id, goal=goal, time_allocated=time_allocated, schedule_content=schedule_content)
            db.session.add(new_plan)
            db.session.commit()
            return new_plan
        except Exception as e:
            db.session.rollback()
            print(f"Error creating plan: {e}")
            return None

    @classmethod
    def get_by_id(cls, plan_id):
        """根據 ID 取得學習計畫"""
        try:
            return cls.query.get(plan_id)
        except Exception as e:
            print(f"Error fetching plan by id: {e}")
            return None

    @classmethod
    def get_all_by_user(cls, user_id):
        """取得某使用者的所有學習計畫"""
        try:
            return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()
        except Exception as e:
            print(f"Error fetching plans for user: {e}")
            return []

    def update(self, **kwargs):
        """更新學習計畫"""
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error updating plan: {e}")
            return None

    def delete(self):
        """刪除學習計畫"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting plan: {e}")
            return False
