from random import randint

#---------------- Not my code ------------------

from os import system

system("")

COLOR = {
    "MAGENTA": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",
}

#----------------------------------------------

Tiles = {
    "Hidden": COLOR["BLUE"] + "H" + COLOR["ENDC"],
    "Flagged": COLOR["RED"] + "M" + COLOR["ENDC"]
}

map_size = [8, 8]

num_to_let = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
    4: "E",
    5: "F",
    6: "G",
    7: "H",
    8: "I",
    9: "J",
    10: "K",
    11: "L",
    12: "M",
    13: "N",
    14: "O",
    15: "P",
    16: "Q",
    17: "R",
    18: "S",
    19: "T",
    20: "U",
    21: "V",
    22: "W",
    23: "X",
    24: "Y",
    25: "Z",
}

let_to_num = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "I": 8,
    "J": 9,
    "K": 10,
    "L": 11,
    "M": 12,
    "N": 13,
    "O": 14,
    "P": 15,
    "Q": 16,
    "R": 17,
    "S": 18,
    "T": 19,
    "U": 20,
    "V": 21,
    "W": 22,
    "X": 23,
    "Y": 24,
    "Z": 25
}

map: list = []
rev_map: list = []

flagged: list = []
mines: list = []
num_of_mines: int

alive = True
won = False

first_tile_pressed = False


def update_cell(cell: list) -> None:
  global map
  if map[cell[1]][cell[0]] != "M":
    neighbours = get_neighbours(cell)
    mines_near = 0
    for neighbour in neighbours:
      if map[neighbour[1]][neighbour[0]] == "M":
        mines_near += 1
    map[cell[1]][cell[0]] = str(mines_near)


def get_neighbours(cell: list) -> list:
  neighbours = [
      [cell[0] - 1, cell[1] - 1],  #Top left
      [cell[0], cell[1] - 1],  # Top center
      [cell[0] + 1, cell[1] - 1],  # Top right
      [cell[0] - 1, cell[1]],  # Middle left
      [cell[0] + 1, cell[1]],  # Middle right
      [cell[0] - 1, cell[1] + 1],  #Bottom left
      [cell[0], cell[1] + 1],  # Bottom center
      [cell[0] + 1, cell[1] + 1]  # Bottom right
  ]

  if cell == [0, 0]:
    return [neighbours[4], neighbours[6], neighbours[7]]
  elif cell == [0, map_size[1] - 1]:
    return [neighbours[1], neighbours[2], neighbours[4]]
  elif cell == [map_size[0] - 1, 0]:
    return [neighbours[3], neighbours[5], neighbours[6]]
  elif cell == [map_size[0] - 1, map_size[1] - 1]:
    return [neighbours[0], neighbours[1], neighbours[3]]

  elif cell[0] == 0:
    neighbours.pop(0)
    neighbours.pop(2)
    neighbours.pop(3)
  elif cell[0] == map_size[0] - 1:
    neighbours.pop(2)
    neighbours.pop(3)
    neighbours.pop(5)
  elif cell[1] == 0:
    neighbours.pop(0)
    neighbours.pop(0)
    neighbours.pop(0)
  elif cell[1] == map_size[1] - 1:
    neighbours.pop(-1)
    neighbours.pop(-1)
    neighbours.pop(-1)

  return neighbours


def dig(x, y) -> None:
  global map, alive, rev_map, first_tile_pressed
  cell = [x, y]
  if cell in mines:
    if first_tile_pressed is False:

      new_mine = [randint(0, map_size[0] - 1), randint(0, map_size[1] - 1)]
      if len(mines) != map_size[0] * map_size[1]:
        while cell in mines:
          mines.pop(mines.index(cell))
          while new_mine in mines:
            new_mine = [
                randint(0, map_size[0] - 1),
                randint(0, map_size[1] - 1)
            ]
          mines.append(new_mine)
        map = []
        rev_map = []
        make_map()

      else:
        alive = False
        return
    else:
      alive = False
      return

  rev_map[y][x] = map[y][x]
  buffer = [cell]
  while buffer != []:
    cell = buffer[0]
    rev_map[cell[1]][cell[0]] = map[cell[1]][cell[0]]
    neighbours = get_neighbours(cell)
    for neighbour in neighbours:
      if rev_map[neighbour[1]][neighbour[0]] != Tiles["Hidden"]:
        continue
      if map[neighbour[1]][neighbour[0]] == "0":
        buffer.append(neighbour.copy())
      if map[neighbour[1]][neighbour[0]].isnumeric() is True and map[cell[1]][
          cell[0]] == "0":
        rev_map[neighbour[1]][neighbour[0]] = map[neighbour[1]][neighbour[0]]
    buffer.pop(0)


def flag(x, y):
  global rev_map
  if rev_map[y][x] in [Tiles["Hidden"], Tiles["Flagged"]]:
    if [x, y] in flagged:
      flagged.remove([x, y])
      rev_map[y][x] = Tiles["Hidden"]
  else:
    flagged.append([x, y])
    rev_map[y][x] = Tiles["Flagged"]


def update_game():
  inp = input("Make a move: ")
  grid_pos = inp.split()
  if len(grid_pos) < 2 or grid_pos[1].isnumeric is False or grid_pos[
      0].isalpha is False:
    return
  grid_pos[1] = int(grid_pos[1])
  grid_pos[0] = let_to_num[grid_pos[0].upper()]

  if len(grid_pos) == 3:
    if grid_pos[2].upper() == "F":
      flag(grid_pos[0], grid_pos[1])
  else:
    dig(grid_pos[0], grid_pos[1])


def make_map():
  global map, rev_map
  while len(mines) != num_of_mines:
    new_mine = [randint(0, map_size[0] - 1), randint(0, map_size[1] - 1)]
    if new_mine not in mines:
      mines.append(new_mine)

  for y in range(0, map_size[1]):
    buffer = []
    rev_buffer = []
    for x in range(0, map_size[0]):
      if [x, y] in mines:
        buffer.append("M")
      else:
        buffer.append("")
      rev_buffer.append(Tiles["Hidden"])
    rev_map.append(rev_buffer.copy())
    map.append(buffer.copy())

  for y in range(0, map_size[1]):
    for x in range(0, map_size[0]):
      update_cell([x, y])

def print_map(current_map):
  coords = "    "
  for x in range(0, map_size[0]):
    coords += COLOR["MAGENTA"] + num_to_let[x] + "" + COLOR["ENDC"]
  print(coords)
  for y in range(0, map_size[1]):
    line = ""
    if y < 10:
      line += " "
    line += COLOR["MAGENTA"] + str(y) + "| " + COLOR["ENDC"]
    for x in range(0, map_size[0]):
      line += current_map[y][x] + ""
    print(line)
  if won is False and alive is True:
    print("Mines left: " + str(num_of_mines - len(flagged)))


print(
    "Controls:\n- Enter x y to dig a cell (A 4)\n- x y f to flag it (B 5 F) \n- The spaces are needed\n"
)

map_size[0] = int(input("Enter map size x: "))
map_size[1] = int(input("Enter map size y: "))
num_of_mines = int(input("Enter number of mines: "))

make_map()

while alive is True and won is False:
  print_map(rev_map)
  update_game()
  first_tile_pressed = True

  cells_the_same = 0

  for y in range(0, map_size[1]):
    for x in range(0, map_size[0]):
      if rev_map[y][x] == map[y][x]:
        cells_the_same += 1

  if cells_the_same == (map_size[0] * map_size[1]) - num_of_mines:
    won = True

print_map(map)

if won is True and alive is True:
  print("You won")
else:
  print("You stepped on a mine")
