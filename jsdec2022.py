from collections import deque
from enum import Enum
import copy
import time


class Position:
    def __init__(self, r:int, c:int, s:int, remaining_sum:int=9767, visited=[(5,0)]):
        self.row = r
        self.col = c
        self.score = s
        self.remaining_sum = remaining_sum # sum of the board
        self.visited = visited
    
    def toStr(self) -> None:
        print(f'Row: {self.row} | Col: {self.col} | Score: {self.score} | Remaining_sum: {self.remaining_sum}')

class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

class Dice:
    def __init__(self, top:float=None, bot:float=None, left:float=None, right:float=None, front:float=None, back:float=None):
        self.top:float = top
        self.bot:float = bot
        self.left:float = left
        self.right:float = right
        self.front:float = front
        self.back:float = back


    def roll(self, dir:str):
        match dir:
            case 'LEFT':
                return Dice(top=self.right, bot=self.left, left=self.top, front=self.front, right=self.bot, back=self.back)
            case 'UP':
                return Dice(left=self.left, right=self.right, front=self.top, top=self.back, back=self.bot, bot=self.front)
            case 'RIGHT':
                return Dice(top=self.left, bot=self.right, left=self.bot, front=self.front, right=self.top, back=self.back)
            case 'DOWN':
                return Dice(left=self.left, right=self.right, front=self.bot, top=self.front, back=self.top, bot=self.back)


    def toStr(self) -> None:
        print(f'Top: {self.top} | Bot: {self.bot} | Left: {self.left} | Right: {self.right} | Front: {self.front} | Back: {self.back}')


def solve():
    board = [[57, 33, 132, 268, 492, 732],
            [81, 123, 240, 443, 353, 508],
            [186, 42, 195, 704, 452, 228],
            [-7, 2, 357, 452, 317, 395],
            [5, 23, -4, 592, 445, 620],
            [0, 77, 32, 403, 337, 452]]

    move = 1
    queue = deque()
    directions = (Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT)

    queue.append((Position(r=5, c=0, s=0), Dice()))

    while queue:
        print('Move:', move)
        temp_q = copy.deepcopy(queue)
        while temp_q:
            pos, dice = queue.popleft()
            pos.toStr()
            dice.toStr()
            print()
            temp_q.popleft()
            for dir in directions:
                dr, dc = dir.value
                new_row, new_col = pos.row + dr, pos.col + dc
                if new_row < 0 or new_row > 5 or new_col < 0 or new_col > 5:
                    continue
                new_dice = dice.roll(dir.name)
                if not new_dice.top:
                    print('New number added to dice')
                    new_dice.top = (board[new_row][new_col] - pos.score) / move
                new_score = pos.score + move * new_dice.top
                if board[new_row][new_col] == new_score:
                    print('Direction of next roll:', dir.name)
                    if new_row == 0 and new_col == 5:
                        print('End found. Remaining sum:', pos.remaining_sum - board[new_row][new_col])  # return remaining_sum - the value of the final square
                        return
                    new_rem_sum = pos.remaining_sum - board[new_row][new_col] if (new_row, new_col) not in pos.visited else pos.remaining_sum
                    new_vis = pos.visited + [(new_row, new_col)]
                    new_pos = Position(r=new_row, c=new_col, s=new_score, remaining_sum=new_rem_sum, visited=new_vis)
                    queue.append((new_pos, new_dice))
        move += 1
            
    print('No dice found')


if __name__ == '__main__':
    solve()
    