from random import random

def random_pin() -> str:
    '''
    Utility metoda, ktera umi generovat nahodny 5 mistny PIN.
    '''
    return str(int(random() * 10000 + 10000))
