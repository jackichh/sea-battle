import time
from tkinter import *
from tkinter import messagebox
from ships import Ships
from ship import Ship
from board import Board
import random


class App:
    GAME_IS_RUNNING = False
    PLAYERS_TURN = True
    CANVAS_WIDTH = CANVAS_HEIGHT = L = 500
    SIZE = 10
    STEP = CANVAS_WIDTH // SIZE
    NUMBER_OF_SHIPS = 10

    NUMBER_OF_CELLS_FOR_SHIPS = 20

    def __init__(self, window):
        self.__in_attack = False
        self.__window = window
        self.__create_screen()
        self.__draw_widgets()
        self.__computer_ships = Ships()
        self.__player_ships = None
        self.__game_has_started = False
        self.__start_placing()
        self.__computer_fleet_is_shown = False
        self.__there_was_a_hit = (False, [], Ship())
        self.__cells_around_hit_cell = set()
        self.__first_hit = ()
        self.__front_or_back = set()

    def __create_screen(self):
        self.__window.title('Sea Battle')
        self.__window.geometry(f'{1200}x{720}')
        self.__window.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.__window.resizable(False, False)

    def __on_closing(self):
        if messagebox.askokcancel("Quit?", "Your progress won't be saved!"):
            self.__window.destroy()

    def __draw_widgets(self):
        label_upper = Label(text='Start placing your ships')
        label_upper.place(x=50, y=15)

        self.__ready_btn = Button(height=2, width=7, text='Ready', command=self.__ready_button)
        self.__ready_btn.place(x=50, y=50)

        self.__random_btn = Button(height=2, width=15, command=self.__random_button, text='Generate fleet')
        self.__random_btn.place(x=125, y=50)

        self.__entry = Entry(self.__window, font=['calibre', 8, 'normal'])
        self.__entry.place(x=250, y=45)

        self.__cheat_btn = Button(height=1, width=8, text='show', command=self.__check_entry)
        self.__cheat_btn.place(x=250, y=70)

        self.__hide_btn = Button(height=1, width=8, text='hide', command=self.__hide_computer_fleet)
        self.__hide_btn.place(x=325, y=70)

        label_lower_player = Label(text="Player's board", font=("Arial", 16, "bold"))
        label_lower_player.place(x=225, y=650)

        label_lower_computer = Label(text="Computer's board", font=("Arial", 16, "bold"))
        label_lower_computer.place(x=810, y=650)

    def __check_entry(self):
        if self.__entry.get() == 'password':
            # App.__draw_random_fleet(self.__computer_board, self.__computer_ships, 'green')
            self.__computer_fleet_is_shown = True
        else:
            pass

    def __hide_computer_fleet(self):
        pass

    def __start_placing(self):
        self.__player_board = Board(root=self.__window,
                                    bg='lightblue',
                                    side_length=App.L,
                                    side_pos=LEFT,
                                    number_of_ships=App.NUMBER_OF_SHIPS,
                                    size_of_board=App.SIZE)
        self.__computer_board = Board(self.__window, 'lightblue', App.L, RIGHT, App.NUMBER_OF_SHIPS, App.SIZE)
        print("Computer's fleet: \n" + str(self.__computer_ships) + '\n')
        print("Player's fleet: \n" + str(self.__player_ships))
        self.__random_button()
        self.__computer_board.bind('<Button-1>', App.__while_placing_ships)

    @staticmethod
    def __while_placing_ships(event):
        messagebox.showinfo(title='Info', message="Press 'ready' button, if you are ready")

    def __start_game(self):
        App.GAME_IS_RUNNING = True
        self.__computer_board.bind('<ButtonPress-1>', self.__when_pressed)
        self.__computer_board.bind('<ButtonRelease-1>', self.__when_released)

    def __when_pressed(self, event):
        if self.PLAYERS_TURN:
            if self.__computer_ships.there_are_alive_ships():
                x, y = (event.x // 50, event.y // 50)
                if (x, y) in self.__computer_ships.get_all_possible_cells():
                    if (x, y) in self.__computer_ships.get_cells_all_ships_occupy_set():
                        self.__computer_board.create_rectangle((x * 50, y * 50), ((x + 1) * 50, (y + 1) * 50), 'gray')
                        self.__computer_board.create_cross((x, y))
                        ship = self.__computer_ships.detect_ship_by_cell((x, y))
                        print(ship)
                        ship.been_shot((x, y))
                        if ship.is_dead():
                            print(ship, 'is dead')
                            App.__draw_and_remove_dead_ship_area(self.__computer_ships, ship, self.__computer_board)
                            self.__computer_ships.delete_ship_from_ship_list(ship)
                            print(len(self.__computer_ships))
                            if len(self.__computer_ships) == 0:
                                messagebox.showinfo(title='Game over', message='You have won!!!')
                                self.__window.destroy()
                        else:
                            self.__computer_ships.remove_cell_from_possible_cells((x, y))
                    else:
                        self.__computer_board.create_dot((x, y))
                        self.__computer_ships.remove_cell_from_possible_cells((x, y))
                        self.PLAYERS_TURN = False

                    print(x, y)
                    print('player shoots\n')
                else:
                    messagebox.showinfo(title='Notice', message="You cannot shoot at this cell!")
            else:
                print('computer has no ships')
        else:
            pass

    def __start_new_game(self):
        self.__init__(self.__window)

    # def __get_random_cell_from_cells_around_hit(self, cell, valid_cells):
    #     hit_x, hit_y = cell
    #     x, y = random.choice([(hit_x + 1, hit_y), (hit_x, hit_y + 1), (hit_x - 1, hit_y), (hit_x, hit_y - 1)])
    #     if (x, y) in valid_cells:
    #         return x, y
    #     else:
    #         return self.__get_cells_around_hit(cell, valid_cells.difference((x, y)))

    # def __get_cells_around_hit(self, cell):
    #     x, y = cell
    #     return {(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)}

    def __when_released(self, event):

        if not self.PLAYERS_TURN:
            time.sleep(0.5)
            if self.__player_ships.there_are_alive_ships():
                # if self.__in_attack:
                #     if self.__there_was_a_hit[0]:
                #         hit = self.__there_was_a_hit[1]
                #         hit_ship = self.__there_was_a_hit[2]
                #         ship_hp = hit_ship.get_health_points()
                #         ship_len = hit_ship.get_length()
                #         if ship_len - ship_hp == 1:
                #             self.__cells_around_hit_cell = self.__get_cells_around_hit(hit)
                #             x, y = random.choice(tuple(self.__get_cells_around_hit(cell=hit)))
                #             self.__cells_around_hit_cell.discard((x,y))
                #         else:
                #             if ship_len - ship_hp == 2:
                #                 first = self.__first_hit
                #                 fx, fy = first[0], first[1]
                #                 lx, ly = self.__there_was_a_hit[1]
                #                 if fx == fy:
                #                     self.__front_or_back.add({(fx, max(fy, ly)+1), (fx, min(fy, ly)-1)})
                #                 else:
                #                     self.__front_or_back.add({(fy, max(fx, lx) + 1), (fy, min(fx, lx) - 1)})
                #                 x, y = random.choice(tuple(self.__front_or_back))
                #                 self.__second_cell = True
                #
                #     else:
                #         if not self.__second_cell:
                #             x, y = random.choice(tuple(self.__cells_around_hit_cell))
                #             self.__cells_around_hit_cell.discard((x, y))
                #         else:
                #             x, y = random.choice(tuple(self.__front_or_back))
                #
                # else:
                #     x, y = random.choice(tuple(self.__player_ships.get_all_possible_cells()))

                #     hit = self.__there_was_a_hit[1]
                #     check_ship = self.__player_ships.detect_ship_by_cell(hit)
                #     try:
                #         if check_ship.is_dead():
                #             x, y = random.choice(tuple(self.__player_ships.get_all_possible_cells()))
                #         else:
                #             x, y = self.__get_cells_around_hit(hit, self.__player_ships.get_all_possible_cells())
                #     except:
                #
                # else:
                x, y = random.choice(tuple(self.__player_ships.get_all_possible_cells()))
                if (x, y) in self.__player_ships.get_all_possible_cells():
                    if (x, y) in self.__player_ships.get_cells_all_ships_occupy_set():
                        self.__in_attack = True
                        self.__player_board.create_rectangle((x * 50, y * 50), ((x + 1) * 50, (y + 1) * 50), 'gray')
                        self.__player_board.create_cross((x, y))

                        ship = self.__player_ships.detect_ship_by_cell((x, y))
                        print(ship)
                        ship.been_shot((x, y))
                        self.__there_was_a_hit = True, (x, y), ship
                        if self.__first_hit != ():
                            self.__first_hit = (x, y)
                        else:
                            pass
                        if ship.is_dead():
                            self.__in_attack = False
                            self.__first_hit = ()
                            print(ship, 'is dead')
                            App.__draw_and_remove_dead_ship_area(self.__player_ships, ship, self.__player_board)
                            self.__player_ships.delete_ship_from_ship_list(ship)
                            print(len(self.__player_ships))
                            if len(self.__player_ships) == 0:
                                messagebox.showinfo(title='Game over', message='You have lost(((')
                                self.__window.destroy()
                        else:
                            self.__player_ships.remove_cell_from_possible_cells((x, y))
                        self.__when_released(event)
                    else:
                        self.PLAYERS_TURN = True
                        if not self.__in_attack:
                            self.__there_was_a_hit = False, (x, y), Ship()
                        self.__player_board.create_dot((x, y))
                        self.__player_ships.remove_cell_from_possible_cells((x, y))

                    print(x, y)

                    print('computer shoots\n')
                else:
                    pass
            else:
                print('player has no ships')
        else:
            pass

    def __random_button(self):
        self.__player_ships = Ships()
        App.__draw_random_fleet(self.__player_board, self.__player_ships, 'gray25')

    def __ready_button(self):
        self.__random_btn['state'] = 'disabled'
        self.__ready_btn['state'] = 'disabled'
        messagebox.showinfo(title='Start', message="Game has started\nPlayer's turn")
        print(self.__player_ships)
        self.__start_game()

    @staticmethod
    def __draw_random_fleet(canvas, ships, color):
        canvas.clear_board()
        for ship in ships:
            for cell in ship:
                canvas.create_rectangle((cell[0] * 50, cell[1] * 50), ((cell[0] + 1) * 50,
                                                                       (cell[1] + 1) * 50), color)

    @staticmethod
    def __draw_and_remove_dead_ship_area(ships, ship, board):
        for cell in ship:
            ships.remove_cell_from_possible_cells((cell[0], cell[1]))
            for k in range(-1, 2):
                for m in range(-1, 2):
                    if 0 <= (cell[0] + k) <= 9 and 0 <= (cell[1] + m) <= 9 and (cell[0] + k, cell[1] + m) != (
                            cell[0], cell[1]):
                        board.create_rectangle(((cell[0] + k) * 50, (cell[1] + m) * 50),
                                               ((cell[0] + k + 1) * 50,
                                                (cell[1] + m + 1) * 50),
                                               'gray')
                        ships.remove_cell_from_possible_cells((cell[0] + k, cell[1] + m))
        for cell in ship:
            board.create_cross(cell)
        start_pos = sorted(ship)[0]
        end_pos = sorted(ship)[-1]
        board.create_rectangle(((start_pos[0]) * 50, (start_pos[1]) * 50),
                               ((end_pos[0] + 1) * 50,
                                (end_pos[1] + 1) * 50), width=5)

#
# def __get_cells_around_hit(self, cell):
#     """Returns the four adjacent cells (up, down, left, right) around a hit cell."""
#     x, y = cell
#     return {(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)}
#
#
# def __filter_valid_cells(self, cells):
#     """Filters a set of cells to only include valid cells that haven't been shot at yet."""
#     valid_cells = set()
#     for cell in cells:
#         x, y = cell
#         if (0 <= x <= 9 and 0 <= y <= 9 and
#                 cell in self.__player_ships.get_all_possible_cells()):
#             valid_cells.add(cell)
#     return valid_cells
#
#
# def __when_released(self, event):
#     if not self.PLAYERS_TURN:
#         time.sleep(0.5)
#         if self.__player_ships.there_are_alive_ships():
#             # Choose target cell based on AI strategy
#             if self.__in_attack:
#                 # We're in "hunt" mode - we've hit a ship and are trying to sink it
#                 if self.__first_hit == ():
#                     # This is our first hit on this ship
#                     self.__first_hit = self.__there_was_a_hit[1]
#
#                 # Get all cells adjacent to our last hit
#                 hit_cell = self.__there_was_a_hit[1]
#                 cells_around_hit = self.__get_cells_around_hit(hit_cell)
#                 valid_targets = self.__filter_valid_cells(cells_around_hit)
#
#                 if valid_targets:
#                     # If we have multiple hits in a row, prioritize cells in that direction
#                     if self.__there_was_a_hit[2].get_length() - self.__there_was_a_hit[2].get_health_points() >= 2:
#                         # We have at least 2 hits on the same ship, so we know its orientation
#                         first_hit = self.__first_hit
#                         last_hit = self.__there_was_a_hit[1]
#
#                         # Determine if ship is horizontal or vertical
#                         if first_hit[0] == last_hit[0]:  # Horizontal
#                             # Try to extend in the same direction
#                             min_y = min(first_hit[1], last_hit[1])
#                             max_y = max(first_hit[1], last_hit[1])
#                             potential_targets = {(first_hit[0], min_y - 1), (first_hit[0], max_y + 1)}
#                             aligned_targets = self.__filter_valid_cells(potential_targets)
#                             if aligned_targets:
#                                 valid_targets = aligned_targets
#                         else:  # Vertical
#                             # Try to extend in the same direction
#                             min_x = min(first_hit[0], last_hit[0])
#                             max_x = max(first_hit[0], last_hit[0])
#                             potential_targets = {(min_x - 1, first_hit[1]), (max_x + 1, first_hit[1])}
#                             aligned_targets = self.__filter_valid_cells(potential_targets)
#                             if aligned_targets:
#                                 valid_targets = aligned_targets
#
#                     # Choose a random cell from our valid targets
#                     x, y = random.choice(tuple(valid_targets))
#                 else:
#                     # No valid adjacent cells, revert to random targeting
#                     x, y = random.choice(tuple(self.__player_ships.get_all_possible_cells()))
#             else:
#                 # We're in "seek" mode - randomly searching for ships
#                 x, y = random.choice(tuple(self.__player_ships.get_all_possible_cells()))
#
#             # Process the shot
#             if (x, y) in self.__player_ships.get_all_possible_cells():
#                 if (x, y) in self.__player_ships.get_cells_all_ships_occupy_set():
#                     # Hit
#                     self.__in_attack = True
#                     self.__player_board.create_rectangle((x * 50, y * 50), ((x + 1) * 50, (y + 1) * 50), 'gray')
#                     self.__player_board.create_cross((x, y))
#
#                     ship = self.__player_ships.detect_ship_by_cell((x, y))
#                     print(ship)
#                     ship.been_shot((x, y))
#                     self.__there_was_a_hit = True, (x, y), ship
#
#                     if ship.is_dead():
#                         # Ship is sunk, reset targeting variables
#                         self.__in_attack = False
#                         self.__first_hit = ()
#                         print(ship, 'is dead')
#                         App.__draw_and_remove_dead_ship_area(self.__player_ships, ship, self.__player_board)
#                         self.__player_ships.delete_ship_from_ship_list(ship)
#                         print(len(self.__player_ships))
#                         if len(self.__player_ships) == 0:
#                             messagebox.showinfo(title='Game over', message='You have lost(((')
#                             self.__window.destroy()
#                     else:
#                         self.__player_ships.remove_cell_from_possible_cells((x, y))
#
#                     # Computer gets another turn after a hit
#                     self.__when_released(event)
#                 else:
#                     # Miss
#                     self.PLAYERS_TURN = True
#                     if not self.__in_attack:
#                         self.__there_was_a_hit = False, (x, y), Ship()
#                     self.__player_board.create_dot((x, y))
#                     self.__player_ships.remove_cell_from_possible_cells((x, y))
#
#                 print(x, y)
#                 print('computer shoots\n')
#             else:
#                 pass
#         else:
#             print('player has no ships')
#     else:
#         pass