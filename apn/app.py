from flask import Flask, request, render_template, send_file, session
import joblib
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import datetime

app = Flask(__name__)
app.secret_key = 'exam-results-secret-key-2026'

# Mapping for converting numeric form values to readable text
VALUE_MAPPINGS = {
    'Resources': {
        '0': 'No Resources',
        '1': 'Some Resources',
        '2': 'Many Resources'
    },
    'Internet': {
        '0': 'No Internet',
        '1': 'Yes'
    },
    'Gender': {
        '0': 'Female',
        '1': 'Male'
    },
    'StressLevel': {
        '0': 'Low',
        '1': 'Medium',
        '2': 'High'
    }
}

def convert_details_to_readable(details):
    """Convert numeric form values to human-readable text"""
    readable_details = {}
    for key, value in details.items():
        if key in VALUE_MAPPINGS:
            readable_details[key] = VALUE_MAPPINGS[key].get(str(value), str(value))
        else:
            readable_details[key] = str(value)
    return readable_details

model = joblib.load("best_random_forest_model.pkl")
feature_names = ['StudyHours', 'Attendance', 'Resources', 'Internet', 'Gender', 'Age', 'AssignmentCompletion', 'OnlineCourses', 'StressLevel']

@app.route("/")
def home():
    return render_template("index.html")



@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = pd.DataFrame([[
            float(request.form["StudyHours"]),
            float(request.form["Attendance"]),
            float(request.form["Resources"]),
            float(request.form["Internet"]),
            float(request.form["Gender"]),
            float(request.form["Age"]),
            float(request.form["AssignmentCompletion"]),
            float(request.form["OnlineCourses"]),
            float(request.form["StressLevel"])
        ]], columns=feature_names)
        

        prediction = model.predict(input_data)

        if prediction[0] == 0:
            result = "Excellent"
        elif prediction[0] == 1:
            result = "Good"
        elif prediction[0] == 2:
            result = "Satisfactory"  
        else:            
            result = "Fail"
        
        # Store result and details in session for PDF download
        entered_details = {name: request.form.get(name, "") for name in feature_names}
        readable_details = convert_details_to_readable(entered_details)
        
        session['prediction_result'] = result
        session['prediction_details'] = readable_details

        return render_template("results.html", prediction_text=result, details=readable_details)

    except Exception as e:
        return f"Error: {str(e)}"


@app.route("/download_result")
def download_result():
    """Generate and download prediction result as PDF"""
    result = session.get('prediction_result', 'Unknown')
    details = session.get('prediction_details', {})
    
    if not result or not details:
        return "No prediction data available. Please run a prediction first.", 400
    
    # Create PDF in memory
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=1
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Build document elements
    elements = []
    
    # Title
    elements.append(Paragraph("Exam Prediction Result", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Result Section
    elements.append(Paragraph("Prediction Result", heading_style))
    result_color = {
        "Excellent": colors.HexColor('#27ae60'),
        "Good": colors.HexColor('#3498db'),
        "Satisfactory": colors.HexColor('#f39c12'),
        "Fail": colors.HexColor('#e74c3c')
    }.get(result, colors.black)
    
    result_style = ParagraphStyle(
        'ResultText',
        parent=styles['Normal'],
        fontSize=18,
        textColor=result_color,
        fontName='Helvetica-Bold'
    )
    elements.append(Paragraph(result, result_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Details Section
    elements.append(Paragraph("Entered Details", heading_style))
    
    # Create table for details
    detail_data = [["Parameter", "Value"]]
    for key, value in details.items():
        detail_data.append([key, str(value)])
    
    detail_table = Table(detail_data, colWidths=[3*inch, 2*inch])
    detail_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
    ]))
    elements.append(detail_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer with date
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=1
    )
    elements.append(Paragraph(f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", footer_style))
    
    # Build PDF
    doc.build(elements)
    pdf_buffer.seek(0)
    
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'exam_prediction_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    )

if __name__ == "__main__":
    app.run(debug=True)