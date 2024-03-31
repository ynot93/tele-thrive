class HealthAnalysis:
    total_scores = []
    
    def __init__(self, personality_type, anxiety_levels, depression_likelihood):
        self.personality_type = personality_type
        self.anxiety_levels = anxiety_levels
        self.depression_likelihood = depression_likelihood
        
    def categorize_personality_type(responses):
        # Calculate scores for personality traits
        extroversion_score = sum(responses[0:2])
        openness_score = sum(responses[3:5])
        neuroticism_score = sum(responses[6:8])
    
        # Determine personality type based on scores
        personality_type = {
            'extroverted': 'introverted' if extroversion_score < 4 else 'extroverted',
            'open': 'conscientious' if openness_score < 4 else 'open',
            'emotionally_stable': 'neurotic' if neuroticism_score < 4 else 'emotionally stable'
        }
        
        return personality_type
    
    def categorize_anxiety_levels(responses):
        # Calculate total anxiety score
        anxiety_score = sum(responses[9:12])  # Sum of responses to questions 9, 10, and 11
    
        # Determine anxiety level based on score
        if anxiety_score < 6:
            return 'low'
        elif anxiety_score < 9:
            return 'moderate'
        else:
            return 'high'

    def categorize_depression_likelihood(responses):
        # Calculate total depression score
        depression_score = sum(responses[9:12])  # Sum of responses to questions 9, 10, and 11
        
        # Determine depression likelihood based on score
        if depression_score < 3:
            return 'minimal'
        elif depression_score < 6:
            return 'mild'
        elif depression_score < 9:
            return 'moderate'
        else:
            return 'severe'