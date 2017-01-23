from functools import reduce

MOVES = ((1,0), (0,1), (-1,0), (0,-1))
ADD = lambda a, b: tuple(map(sum, zip(a,b)))

class Game:
    def __init__(self, dim, pairs):
        self.dim = dim
        self.pairs = pairs
        self.ends = tuple([pair[1] for pair in pairs])
        self.steps= [list(pair[:1]) for pair in pairs]

    def _isOver(self):
        return self._countEmpty() == 0

    def _getFilled(self):
        return tuple(reduce(lambda a, b: a+b, self.steps))

    def _countEmpty(self):
        return self.dim**2 - len(self._getFilled())

    def _isOnBoard(self, point):
        return 0 <= point[0] < self.dim and 0 <= point[1] < self.dim

    def _isMovable(self, point, n):
        occupied = self._getFilled() + self.ends[:n] + self.ends[n+1:]
        return self._isOnBoard(point) and point not in occupied

    def solve(self, n=0):
        if self._isOver():
            return True

        if not n < len(self.pairs):
            return False

        cur = self.steps[n][-1]
        if cur in self.ends: 
            return self.solve(n+1)

        for dir in MOVES:
            poi = ADD(cur, dir)
            if self._isMovable(poi, n):
                self.steps[n].append(poi)
                if self.solve(n):
                    return True
                self.steps[n].pop()
        return False

