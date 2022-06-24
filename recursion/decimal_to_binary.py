def decimal_to_binary(n):
    assert int(n) == n, "The parameter must be an integer only!"
    if n == 0:
        return 0
    else:
        return n % 2 + 10 * decimal_to_binary(int(n/2))
