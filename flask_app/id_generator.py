import uuid

def generate_unique_user_id():
    """
    Generate a unique ID for a user.

    Returns:
        str: A unique user ID generated using UUID version 4.
    """
    return str(uuid.uuid4())

def generate_unique_therapist_id():
    """
    Generate a unique ID for a therapist.

    Returns:
        str: A unique therapist ID generated using UUID version 4.
    """
    return str(uuid.uuid4())
                
