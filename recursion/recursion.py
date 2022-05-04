def recursive_method(n):
    if n<1:
        print("n is less than 1")
    else:
        recursive_method(n-1)
        print(n)


def power_of_two_rec(n):
    if n == 0: return 1
    else:
        power = power_of_two_rec(n-1)
        return power * 2


def power_of_two_it(n):
    i = 0
    power = 1
    while i < n:
        power = power * 2
        i = i +1
    return power
