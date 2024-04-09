import unittest
from flask_app.analysis import get_custom_response

class TestAnalysis(unittest.TestCase):
    def test_get_custom_response(self):
        # Test for high personality level, anxiety level, and depression level
        personality_level = 2.0
        anxiety_level = 2.0
        depression_level = 2.0
        response = get_custom_response(personality_level, anxiety_level, depression_level)
        self.assertIsNotNone(response)

        personality_level = 1.0
        anxiety_level = 1.0
        depression_level = 1.0
        response = get_custom_response(personality_level, anxiety_level, depression_level)
        self.assertIsNotNone(response)

        personality_level = 0.0
        anxiety_level = 0.0
        depression_level = 0.0
        response = get_custom_response(personality_level, anxiety_level, depression_level)
        self.assertIsNotNone(response)
