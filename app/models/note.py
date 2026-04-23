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
        new_note = cls(user_id=user_id, title=title, original_content=original_content, summary=summary)
        db.session.add(new_note)
        db.session.commit()
        return new_note

    @classmethod
    def get_by_id(cls, note_id):
        return cls.query.get(note_id)

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
