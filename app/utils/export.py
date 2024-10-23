import csv
from io import StringIO
from datetime import datetime
from typing import List
from app.models import Lead

def generate_leads_csv(leads: List[Lead]) -> StringIO:
    """Generate a CSV file from leads data"""
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header row
    headers = [
        'Company Name',
        'Contact Name',
        'Email',
        'Phone',
        'Industry',
        'Company Size',
        'Lead Score',
        'Grade',
        'Status',
        'Location',
        'Website',
        'Notes',
        'Created Date'
    ]
    writer.writerow(headers)
    
    # Write data rows
    for lead in leads:
        row = [
            lead.company_name,
            lead.contact_name,
            lead.email,
            lead.phone or '',
            lead.industry.title(),
            lead.company_size,
            lead.lead_score,
            lead.lead_grade,
            lead.status,
            lead.location or '',
            lead.website or '',
            lead.notes or '',
            lead.created_at.strftime('%Y-%m-%d')
        ]
        writer.writerow(row)
    
    output.seek(0)
    return output