from random import randint


class Cell:
    def __init__(self, coordinates, color=None):
        self.__x = coordinates[0]
        self.__y = coordinates[1]
        self.__color = color

    @staticmethod
    def random_cell(size):
        return Cell((randint(0, size - 1), randint(0, size - 1)))
