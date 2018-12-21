from math import gcd
from mytest import mytest


def brut():
    C = int(input())

    for _ in range(C):
        input()
        number_of_floors = int(input())
        rooms = [int(x) for x in input().split()]
        X, Y = [int(x) for x in input().split()]

        result = 0
        for floor in range(1, number_of_floors+1):
            l = 100*floor
            r = 100*floor + rooms[floor-1]

            for room in range(l+1, r+1):
                if not room % X or not room % Y:
                    result += 1

        print(result)


def lcm(k, l):
    return k*l/gcd(k, l)


@mytest.neko_tester(0, path='10')
def main():
    C = int(input())

    for _ in range(C):
        input()
        number_of_floors = int(input())
        rooms = [int(x) for x in input().split()]
        X, Y = [int(x) for x in input().split()]
        result = 0
        for floor in range(1, number_of_floors+1):
            r = 100*floor + rooms[floor-1]
            l = 100*floor
            result += r // X + r // Y - r // lcm(X, Y) - (l // X + l // Y - l // lcm(X, Y))
        print(int(result))


if __name__ == "__main__":
    main()
