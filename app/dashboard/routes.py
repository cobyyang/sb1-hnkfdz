from flask import Blueprint, render_template, send_file
from flask_login import login_required, current_user
from app.models import Lead
from app.utils.export import generate_leads_csv
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    leads = Lead.query.filter_by(user_id=current_user.id).order_by(Lead.created_at.desc()).all()
    return render_template('dashboard/index.html', leads=leads)

@dashboard_bp.route('/export-leads')
@login_required
def export_leads():
    # Get all leads for current user
    leads = Lead.query.filter_by(user_id=current_user.id).order_by(Lead.created_at.desc()).all()
    
    # Generate CSV file
    output = generate_leads_csv(leads)
    
    # Generate filename with timestamp
    filename = f"leads_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    # Return file for download
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )