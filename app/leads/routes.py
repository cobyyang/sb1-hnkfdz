from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Lead, db
from app.leads.forms import LeadForm

leads_bp = Blueprint('leads', __name__)

@leads_bp.route('/leads/new', methods=['GET', 'POST'])
@login_required
def new_lead():
    form = LeadForm()
    if form.validate_on_submit():
        lead = Lead(
            company_name=form.company_name.data,
            contact_name=form.contact_name.data,
            email=form.email.data,
            phone=form.phone.data,
            company_size=form.company_size.data,
            industry=form.industry.data,
            notes=form.notes.data,
            owner=current_user
        )
        # Calculate lead score before saving
        lead.calculate_score()
        db.session.add(lead)
        db.session.commit()
        flash('Lead added successfully!')
        return redirect(url_for('dashboard.index'))
    return render_template('leads/new.html', form=form)

@leads_bp.route('/leads/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_lead(id):
    lead = Lead.query.get_or_404(id)
    if lead.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('dashboard.index'))
    
    form = LeadForm(obj=lead)
    if form.validate_on_submit():
        lead.company_name = form.company_name.data
        lead.contact_name = form.contact_name.data
        lead.email = form.email.data
        lead.phone = form.phone.data
        lead.company_size = form.company_size.data
        lead.industry = form.industry.data
        lead.notes = form.notes.data
        # Recalculate lead score after updates
        lead.calculate_score()
        db.session.commit()
        flash('Lead updated successfully!')
        return redirect(url_for('dashboard.index'))
    return render_template('leads/edit.html', form=form, lead=lead)