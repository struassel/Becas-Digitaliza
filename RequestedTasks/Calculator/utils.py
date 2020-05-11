#!/usr/bin/env python3
import math


def add():
    try:
        x = float(input("Enter first number: "))
        y = float(input("Enter second number: "))
        z = x + y
        print("Result: ", x, " + ", y, " = ", z, sep="")
    except ValueError:
        print("Please, insert a number")


def subtract():
    try:
        x = float(input("Enter first number: "))
        y = float(input("Enter second number: "))
        z = x - y
        print("Result: ", x, " - ", y, " = ", z, sep="")
    except ValueError:
        print("Please, insert a number")


def multiply():
    try:
        x = float(input("Enter first number: "))
        y = float(input("Enter second number: "))
        z = x * y
        print("Result: ", x, " * ", y, " = ", z, sep="")
    except ValueError:
        print("Please, insert a number")


def divide():
    try:
        x = float(input("Enter dividend number: "))
        y = float(input("Enter divisor number: "))
        z = x / y
        print("Result: ", x, " / ", y, " = ", z, sep="")
    except ValueError:
        print("Please, insert a number")
    except ZeroDivisionError:
        print("A number cannot be divided by 0")


def __power(x, y):
    return x ** y  # Manually done as it is one of the features requested by the teacher
    # return math.pow(x,y)


def power():
    try:
        x = float(input("Enter number: "))
        y = float(input("Enter the power: "))
        z = __power(x, y)
        print("Result: ", x, " power ", y, " = ", z, sep="")
    except ValueError:
        print("Please, insert a number")
    except OverflowError:
        print("Result is too big to be printed")


def sqrt():
    try:
        x = float(input("Enter number: "))
        z = __power(x, 0.5)
        print("Result: Square root of ", x, " = ", z, sep="")
    except ValueError:
        print("Please, insert a number")


def __factorial(x):
    if x == 1:
        return 1
    else:
        return x * __factorial(x - 1)


def factorial():
    try:
        x = float(input("Enter number: "))
        z = __factorial(x)
        print("Result: Factorial of ", x, " = ", z, sep="")
    except ValueError:
        print("Please, insert a number")
    except (RecursionError, OverflowError):
        print("Result is too big to be printed")


def log():
    try:
        x = float(input("Enter number: "))
        try:
            z = math.log(x)
        except ValueError as e:
            print("Only positive numbers are allowed")
            return
        print("Result: Exponential logarithm of ", x, " = ", z, sep="")
    except ValueError:
        print("Please, insert a number")
    except OverflowError:
        print("Result is too big to be printed")


def cos():
    try:
        x = float(input("Enter angle in radians: "))
        z = math.cos(x)
        print("Result: Cosine of ", x, " rad = ", z, sep="")
    except ValueError:
        print("Please, insert a valid angle")
    except (RecursionError, OverflowError):
        print("Result is too big to be printed")


def sin():
    try:
        x = float(input("Enter angle in radians: "))
        z = math.sin(x)
        print("Result: Sine of ", x, " rad = ", z, sep="")
    except ValueError:
        print("Please, insert a valid angle")
    except (RecursionError, OverflowError):
        print("Result is too big to be printed")


def tan():
    try:
        x = float(input("Enter angle in radians: "))
        z = math.tan(x)
        print("Result: Tangent of ", x, " rad = ", z, sep="")
    except ValueError:
        print("Please, insert a valid angle")
    except (RecursionError, OverflowError):
        print("Result is too big to be printed")
