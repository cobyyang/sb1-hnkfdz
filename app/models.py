from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from app.utils.lead_scoring import LeadScorer, LeadData

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    leads = db.relationship('Lead', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    contact_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    status = db.Column(db.String(20), default='New')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Fields for lead scoring
    company_size = db.Column(db.Integer, default=0)
    industry = db.Column(db.String(50))
    lead_score = db.Column(db.Integer)
    lead_grade = db.Column(db.String(1))
    website = db.Column(db.String(200))
    location = db.Column(db.String(100))
    revenue = db.Column(db.Float)

    def calculate_score(self):
        """Calculate and update lead score"""
        scorer = LeadScorer()
        lead_data = LeadData(
            company_size=self.company_size,
            industry=self.industry,
            has_email=bool(self.email),
            has_phone=bool(self.phone),
            website=self.website,
            location=self.location,
            revenue=self.revenue
        )
        score_data = scorer.score_lead(lead_data)
        self.lead_score = score_data['total_score']
        self.lead_grade = score_data['grade']
        return score_data