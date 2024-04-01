def get_custom_response(personality_level, anxiety_level, depression_level):
    # Define thresholds for personality levels
    if personality_level >= 1.5:
        personality_response = "You have a strong and outgoing personality."
    elif personality_level >= 0.5:
        personality_response = "You have a moderately outgoing personality."
    else:
        personality_response = "You have a reserved personality."

    # Define thresholds for anxiety levels
    if anxiety_level >= 1.5:
        anxiety_response = "You seem to experience high levels of anxiety. It's important to practice relaxation techniques and seek support if needed."
    elif anxiety_level >= 0.5:
        anxiety_response = "You experience some anxiety, but it's manageable with coping strategies."
    else:
        anxiety_response = "You seem to have low levels of anxiety."

    # Define thresholds for depression levels
    if depression_level >= 1.5:
        depression_response = "Your responses suggest you may be experiencing symptoms of depression. It's important to reach out to a mental health professional for support."
    elif depression_level >= 0.5:
        depression_response = "You're experiencing some symptoms of depression. Taking care of your mental health is important, consider talking to someone about how you're feeling."
    else:
        depression_response = "Your responses indicate low levels of depression."

    # Combine the responses
    custom_response = f"{personality_response} {anxiety_response} {depression_response}"
    return custom_response