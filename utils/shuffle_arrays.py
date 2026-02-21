import random


def shuffleArray(obj_list: list):
    new_obj_list = obj_list[:]
    random.shuffle(new_obj_list)
    return new_obj_list
