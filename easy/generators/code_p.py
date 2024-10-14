import random


def username_generator(n, first_names=None, last_names=None):
    """Generates random username"""
    # YOUR CODE
    user_dict = dict()
    if first_names is None:
        first_names = ['John', 'Jane', 'Alex', 'Emily', 'Chris', 'Taylor']
    if last_names is None:
        last_names = ['Smith', 'Doe', 'Brown', 'Wilson', 'Johnson', 'Davis']

    for i in range(1, n + 1):
        user_dict = {
            'id': i,
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names)
        }
        yield user_dict


def data_generator(n):
    """Generates random data"""
    # YOUR CODE
    for i in range(n):
        pairs = (i, random.randint(0,100))
        yield pairs

