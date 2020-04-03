import random

def get_random_number(length=6):
    """Generate a random string of fixed length """
    numbers = "1234567890"

    return ''.join(random.choice(numbers) for i in range(length))
