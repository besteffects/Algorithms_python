# Fibonacci is a sequence of nmbers in which each number is the sum of the two preceding ones and the sequence starts from 0 and 1
# 0,1,1,2,3,5,,8,13,21,34,55,89
# Step 1
# 5 = 3+2  f(n) = f(n-1)  + f(n-2)
# Step 2
# The stopping criterion 0 and 1

def fibonacci(n):
    if n in [0,1]:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


print(fibonacci(5))
