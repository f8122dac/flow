import time
from solver import Game

def test(dim, pairs):
    print("dimension:", dim)
    print("length:", len(pairs))
    print("pairs:")
    for pair in pairs:
        print("\t{} -> {}".format(pair[0], pair[1]))
    print("\nsolving ...")
    game = Game(dim, pairs)
    start = time.time()
    if game.solve():
        duration = time.time() - start
        print("DONE")
        print("time elapsed: {:d} mins  {:7.4f} secs".format(int(duration)//60, duration%60))
        print("\nsolution steps:")
        for index, steplist in enumerate(game.steps):
            print("\t[{}] -> {}".format(index, steplist))
        print("="*50 + "\n")
    else:
        print("unsolvable")
    return game


def test1():
    dim = 4
    pairs = (
        ((0, 3), (2, 2)),
        ((0, 0), (1, 0)),
        ((1, 3), (3, 2)),
        ((3, 1), (3, 0)),
        )
    print("Starting test1(easy)")
    return test(dim, pairs)

def test2():
    dim = 6
    pairs = (
            ((0, 5), (2, 4)),
            ((0, 2), (0, 4)),
            ((0, 1), (2, 5)),
            ((0, 0), (4, 0)),
            ((5, 0), (5, 4)),
            )
    print("Starting test2(easy)")
    return test(dim, pairs)

def test3():
    dim = 5
    pairs = (
            ((0, 0), (3, 2)),
            ((0, 4), (1, 2)),
            ((0, 3), (2, 1)),
            ((2, 2), (4, 4)),
            ((3, 3), (4, 0)),
            )
    print("Starting test3(easy)")
    return test(dim, pairs)

def test4():
    dim = 6
    pairs = (
            (( 5, 5), ( 4, 0)),
            (( 0, 1), ( 4, 5)),
            (( 1, 1), ( 4, 2)),
            (( 2, 1), ( 3, 2)),
            (( 0, 0), ( 4, 1)),
            )
    print("Starting test4(easy)")
    return test(dim, pairs)

def test5():
    dim = 7
    pairs = (
            (( 0, 6), ( 3, 0)),
            (( 4, 2), ( 3, 5)),
            (( 2, 1), ( 5, 6)),
            (( 6, 2), ( 3, 4)),
            (( 6, 0), ( 3, 1)),
            (( 6, 1), ( 3, 3)),
            (( 6, 6), ( 4, 5)),
            )
    print("Starting test5(medium)")
    return test(dim, pairs)

def test6():
    dim = 8
    pairs = (
            (( 7, 0), ( 1, 3)),
            (( 4, 3), ( 4, 5)),
            (( 5, 1), ( 1, 5)),
            (( 1, 2), ( 4, 1)),
            (( 5, 3), ( 5, 5)),
            (( 6, 1), ( 2, 6)),
            (( 0, 7), ( 7, 1)),
            (( 2, 2), ( 1, 6)),
            )
    print("Starting test6(medium)")
    return test(dim, pairs)

def test7():
    dim = 11
    pairs = (
            ((10, 2), ( 6, 5)),
            ((10,10), ( 8, 2)),
            (( 0, 2), ( 3, 7)),
            (( 0, 0), ( 7, 6)),
            (( 0, 1), ( 8, 3)),
            (( 0, 3), ( 9, 9)),
            (( 2, 3), ( 7, 8)),
            (( 1, 3), ( 9, 4)),
            (( 9, 1), ( 7, 5)),
            )
    print("Starting test7(expert)")
    return test(dim, pairs)
 
if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    #test7()
