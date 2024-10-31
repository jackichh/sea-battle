import random
from ship import Ship


class Ships:
    def __init__(self):
        self.__available_cells = set((x, y) for x in range(0, 10) for y in range(0, 10))
        self.__cells_all_ships_occupy_set = set()
        self.__ships = self.locate_ships()
        self.__all_possible_cells = set((x, y) for x in range(0, 10) for y in range(0, 10))

    def __len__(self):
        return len(self.__ships)

    def get_all_possible_cells(self):
        return self.__all_possible_cells

    def remove_cell_from_possible_cells(self, cell):
        self.__all_possible_cells.discard(cell)

    def delete_ship_from_ship_list(self, ship):
        self.__ships.remove(ship)
        self.__cells_all_ships_occupy_set.difference(ship.get_coordinates_of_ship())

    def there_are_alive_ships(self):
        for ship in self.get_ships():
            if not ship.is_dead():
                return True
        return False

    def get_ships(self):
        return self.__ships

    def get_available_cells(self):
        return self.__available_cells

    def get_cells_all_ships_occupy_set(self):
        return self.__cells_all_ships_occupy_set

    def detect_ship_by_cell(self, cell):
        for ship in self.get_ships():
            for ship_cell in ship.get_coordinates_of_ship():
                if ship_cell == cell:
                    return ship

    @staticmethod
    def generate_randomly_start_cell(available_cells):
        orientation = random.choice(['h', 'v'])
        direction = random.choice((-1, 1))
        x, y = random.choice(tuple(available_cells))
        return (x, y), orientation, direction

    @staticmethod
    def append_cell_to_ship(coordinate, direction, orientation, ship_coordinates):
        if orientation == 'h':
            x_or_y = 0
        else:
            x_or_y = 1

        if (coordinate <= 0 and direction == -1) or (coordinate >= 9 and direction == 1):
            direction *= -1
            return direction, ship_coordinates[0][x_or_y] + direction
        else:
            return direction, ship_coordinates[-1][x_or_y] + direction

    def create_ship(self, length_of_ship, available_cells):
        ship_coordinates = []
        t, orientation, direction = Ships.generate_randomly_start_cell(available_cells)
        x, y = t
        for _ in range(length_of_ship):
            ship_coordinates.append((x, y))
            if orientation == 'h':
                direction, x = Ships.append_cell_to_ship(
                    x, direction, orientation, ship_coordinates)
            else:
                direction, y = Ships.append_cell_to_ship(
                    y, direction, orientation, ship_coordinates)
        if self.is_ship_valid(ship_coordinates):
            return Ship(length_of_ship, ship_coordinates)
        return self.create_ship(length_of_ship, available_cells)

    def is_ship_valid(self, new_ship):
        ship = set(new_ship)
        return ship.issubset(self.__available_cells)

    def add_new_ship_to_set(self, ship):
        for cell in ship:
            self.__cells_all_ships_occupy_set.add(cell)

    def remove_cells_that_ship_occupies_from_available(self, ship):
        for elem in ship:
            for k in range(-1, 2):
                for m in range(-1, 2):
                    if 0 <= (elem[0] + k) <= 9 and 0 <= (elem[1] + m) <= 9:
                        self.__available_cells.discard((elem[0] + k, elem[1] + m))

    def locate_ships(self):
        ships = []
        for length in range(4, 0, -1):
            for _ in range(5 - length):
                new_ship = self.create_ship(length, self.__available_cells)
                ships.append(new_ship)
                self.add_new_ship_to_set(new_ship)
                self.remove_cells_that_ship_occupies_from_available(new_ship.get_coordinates_of_ship())
        return ships

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index < len(self.__ships):
            ship = self.__ships[self.__index]
            self.__index += 1
            return ship
        else:
            raise StopIteration

    def __str__(self):
        str_ships = ''
        for ship in self.__ships:
            str_ships += str(ship) + '\n'
        return str_ships
