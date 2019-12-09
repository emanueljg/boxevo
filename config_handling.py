from random import random

def formula(f, **kwargs) -> float:
    for k, v in kwargs.items():
        f = f.replace(str(k), str(v))
    return eval(f)


def deciprob(value) -> bool:
    return True if random() < value else False
