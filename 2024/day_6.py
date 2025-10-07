from typing import Literal

type Sparse = list[list[int]]
type Position = tuple[int, int]


class Grid:
    def __init__(self, size: tuple[int, int]):
        self.size = size
        self.majors = ([[] for _ in range(size[0])], [[] for _ in range(size[1])])

    @property
    def row_major(self):
        return self.majors[0]

    @property
    def col_major(self):
        return self.majors[1]

    def add_obstacles(self, row: int, obstacles: list[int]):
        self.row_major[row] = obstacles
        for col in obstacles:
            self.col_major[col].append(row)

    def add_obstacle(self, pos: Position):
        self.row_major[pos[0]].insert(_search(self.row_major[pos[0]], pos[1]), pos[1])
        self.col_major[pos[1]].insert(_search(self.col_major[pos[1]], pos[0]), pos[0])

    def remove_obstacle(self, pos: Position):
        del self.row_major[pos[0]][_search(self.row_major[pos[0]], pos[1])]
        del self.col_major[pos[1]][_search(self.col_major[pos[1]], pos[0])]

    def walk(self, start: Position, facing: int) -> tuple[Position, bool]:
        # left: 0, up: 1, right: 2, down: 3
        obstacles = self.majors[facing % 2][start[facing % 2]]
        positive_direction = facing // 2  # is 1 if right or down, 0 otherwise
        obstacle_idx = _search(obstacles, start[(facing + 1) % 2]) + (
            positive_direction - 1
        )  # idx of next obstacle
        nxt = list(start)
        if 0 <= obstacle_idx < len(obstacles):
            # obstacle in the way
            obstacle = True
            nxt[(facing + 1) % 2] = obstacles[obstacle_idx] + (
                1 - 2 * positive_direction
            )
        else:
            # walk off the grid
            obstacle = False
            nxt[(facing + 1) % 2] = positive_direction * (
                self.size[(facing + 1) % 2] - 1
            )
        return ((nxt[0], nxt[1]), obstacle)

    def draw(self, visited: set[Position]):
        for x in range(self.size[0]):
            print(
                "".join(
                    [
                        (
                            "#"
                            if y in self.row_major[x]
                            else "X" if (x, y) in visited else "."
                        )
                        for y in range(self.size[1])
                    ]
                )
            )


def solve(part: Literal["a", "b"], input: str) -> int:
    lines = input.splitlines()
    grid = Grid((len(lines), len(lines[0])))
    pos = None
    for row, line in enumerate(lines):
        obstacles = [col for col, c in enumerate(line) if c == "#"]
        grid.add_obstacles(row, obstacles)
        if (col := line.find("^")) != -1:
            pos = (row, col)

    if pos is None:
        return 0

    if part == "a":
        visited = patrol(grid, pos, 1)
        return len(visited)
    else:
        return solve_b(grid, pos)

def patrol(grid: Grid, pos: Position, facing: int) -> set[Position]:
    """returns visited positions"""
    on_grid = True
    visited = set()
    while on_grid:
        nxt, on_grid = grid.walk(pos, facing)
        visited |= {
            (x, y)
            for x in range(min(pos[0], nxt[0]), max(pos[0], nxt[0]) + 1)
            for y in range(min(pos[1], nxt[1]), max(pos[1], nxt[1]) + 1)
        }

        # turn by 90 degrees clock-wise
        facing = (facing + 1) % 4

        pos = nxt
    return visited

def patrol_loops(grid: Grid, pos: Position, facing: int) -> bool:
    """returns whether patrol is looping"""
    on_grid = True
    visited = { (pos, facing) }
    while on_grid:
        pos, on_grid = grid.walk(pos, facing)
        visited.add((pos, facing))

        facing = (facing + 1) % 4

        if (pos, facing) in visited:
            return True

        visited.add((pos, facing))
    return False


def solve_b(grid: Grid, start: Position) -> int:
    visited = patrol(grid, start, 1)
    total = 0
    for pos in visited:
        if pos != start:
            grid.add_obstacle(pos)
            if patrol_loops(grid, start, 1):
                total += 1
            grid.remove_obstacle(pos)

    return total


def _search(lst: list[int], val: int) -> int:
    """returns insertion index for val in non-empty list"""
    l = 0
    r = len(lst)
    while l < r:
        m = l + (r - l) // 2
        if lst[m] < val:
            l = m + 1
        elif lst[m] > val:
            r = m
        else:
            return m
    assert l <= r
    return l
