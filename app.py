from flask import Flask, render_template, request, jsonify
from diagnosis_system import MedicalDiagnosisSystem
import json

app = Flask(__name__)
diagnosis_system = MedicalDiagnosisSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_symptoms')
def get_symptoms():
    symptoms = diagnosis_system.get_all_symptoms()
    return jsonify(symptoms)

@app.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.json
    selected_symptoms = data.get('symptoms', [])
    severity = data.get('severity', 'moderate')
    duration_days = int(data.get('duration_days', 1))
    
    results = diagnosis_system.diagnose(selected_symptoms, severity, duration_days)
    
    # Format recommendations as HTML list
    for result in results:
        result['recommendations_html'] = '<ul>' + \
            ''.join([f'<li>{rec}</li>' for rec in result['recommendations']]) + \
            '</ul>'
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)