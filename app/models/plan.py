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
        new_plan = cls(user_id=user_id, goal=goal, time_allocated=time_allocated, schedule_content=schedule_content)
        db.session.add(new_plan)
        db.session.commit()
        return new_plan

    @classmethod
    def get_by_id(cls, plan_id):
        return cls.query.get(plan_id)

    @classmethod
    def get_all_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
