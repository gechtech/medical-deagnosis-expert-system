class MedicalDiagnosisSystem:
    def __init__(self):
        self.symptoms = {
            'headache': {
                'description': 'Pain in the head or neck region',
                'associated_conditions': {
                    'tension_headache': 0.8,
                    'migraine': 0.7,
                    'concussion': 0.3
                }
            },
            'fever': {
                'description': 'Elevated body temperature',
                'associated_conditions': {
                    'flu': 0.9,
                    'common_cold': 0.5,
                    'pneumonia': 0.6
                }
            },
            'cough': {
                'description': 'Expulsion of air from lungs',
                'associated_conditions': {
                    'common_cold': 0.8,
                    'flu': 0.7,
                    'pneumonia': 0.6
                }
            },
            'nausea': {
                'description': 'Feeling of sickness with stomach discomfort',
                'associated_conditions': {
                    'migraine': 0.6,
                    'food_poisoning': 0.8,
                    'pregnancy': 0.5
                }
            }
        }
        
        self.conditions = {
            'tension_headache': {
                'description': 'Common headache often related to stress',
                'recommendations': [
                    'Rest in a quiet room',
                    'Over-the-counter pain relievers',
                    'Apply warm or cold compress to neck'
                ]
            },
            'migraine': {
                'description': 'Severe headache often with nausea and light sensitivity',
                'recommendations': [
                    'Rest in a dark, quiet room',
                    'Prescription migraine medication if available',
                    'Avoid strong smells and bright lights'
                ]
            },
            'flu': {
                'description': 'Viral infection affecting respiratory system',
                'recommendations': [
                    'Rest and stay hydrated',
                    'Antiviral medications if early in illness',
                    'Over-the-counter fever reducers'
                ]
            },
            'common_cold': {
                'description': 'Mild viral upper respiratory infection',
                'recommendations': [
                    'Rest and fluids',
                    'Over-the-counter cold medicines',
                    'Saltwater gargle for sore throat'
                ]
            }
        }
        
        self.additional_factors = {
            'severity': {
                'mild': 0.5,
                'moderate': 0.75,
                'severe': 1.0
                
            },
            'duration': {
                'acute': 1.0,    # <3 days
                'subacute': 0.8,  # 3-14 days
                'chronic': 0.6    # >14 days
            }
        }

    def diagnose(self, selected_symptoms, severity, duration_days):
        """Perform diagnosis based on symptoms and additional factors"""
        condition_scores = {}
        
        # Calculate base scores from symptoms
        for symptom in selected_symptoms:
            if symptom in self.symptoms:
                for condition, score in self.symptoms[symptom]['associated_conditions'].items():
                    if condition not in condition_scores:
                        condition_scores[condition] = []
                    condition_scores[condition].append(score)
        
        # Apply severity factor
        severity_factor = self.additional_factors['severity'].get(severity, 0.75)
        
        # Determine duration category
        if duration_days < 3:
            duration_category = 'acute'
        elif duration_days <= 14:
            duration_category = 'subacute'
        else:
            duration_category = 'chronic'
        duration_factor = self.additional_factors['duration'].get(duration_category, 0.8)
        
        # Calculate final scores
        results = []
        for condition, scores in condition_scores.items():
            avg_score = sum(scores) / len(scores)
            weighted_score = avg_score * severity_factor * duration_factor
            results.append({
                'condition': condition,
                'confidence': min(round(weighted_score * 100, 1), 100),  # Cap at 100%
                'description': self.conditions.get(condition, {}).get('description', ''),
                'recommendations': self.conditions.get(condition, {}).get('recommendations', [])
            })
        
        # Sort by confidence (highest first)
        results.sort(key=lambda x: x['confidence'], reverse=True)
        
        return results

    def get_all_symptoms(self):
        """Return all available symptoms with descriptions"""
        return [{'id': k, 'description': v['description']} for k, v in self.symptoms.items()]

    def get_condition_info(self, condition_id):
        """Get detailed information about a specific condition"""
        return self.conditions.get(condition_id, {})