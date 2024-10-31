class Ship:
    def __init__(self, length=None, coordinates=None):
        self.__len = length
        self.__coordinates = coordinates
        self.__health_points = length
        self.__is_alive = True

    def get_length(self):
        return self.__len

    def get_coordinates_of_ship(self):
        return self.__coordinates

    def get_health_points(self):
        return self.__health_points

    def is_dead(self):
        if not self.__is_alive:
            return True
        return False

    def been_shot(self, cell):
        print('hit')
        if self.__health_points - 1 == 0:
            self.__is_alive = False
        if self.__health_points:
            self.__health_points -= 1

    def __iter__(self):
        self.__i = 0
        return self

    def __next__(self):
        if self.__i < self.__len:
            coordinate = self.__coordinates[self.__i]
            self.__i += 1
            return coordinate
        else:
            raise StopIteration

    def __str__(self):
        return f"Ship of length {self.__len} with coordinates {self.__coordinates}"
