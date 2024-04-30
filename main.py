import itertools
import math


# Prints out the number of ballot words on the letters 1,...,k of each length 1\le n\le maxLength
def ballot(k, maxLength):

    # Count words of length n by counting SYT of size n, height at most k
    print("n | #")
    print("-----")
    for n in range(1, maxLength + 1):

        # Get a list of all valid tableau shapes
        tableaux = generateTableaux(maxParts=k, n=n)

        # Initiate the total
        total = 0

        # For each shape, count the number of SYT with the hook length formula
        for tableau in tableaux:
            total += hook(tableau)

        # Print the result
        print(f"{n} | {total}")


# Counts the number of SYT of a given shape using the hook length formula
def hook(tableau):

    # Number of parts of the tableau
    k = len(tableau)

    # Define the k+1'th part to be 0
    tableau.append(0)

    # The numerator of the expression is n!
    x = math.factorial(sum(tableau))

    # My implementation of the hook length formula. Hits the integer limit (at n=10) when k=162.
    for m in range(1, k+1):
        for j in range(1, m+1):
            x *= math.factorial(tableau[j - 1] - tableau[m - 1] + m - j)
            x /= math.factorial(tableau[j - 1] - tableau[m] + m - j)

    # (Debug)
    # print(tableau, round(x))

    # Return the total. The above formula always gives an integer, but we need to round because
    # there is division using floating point numbers, which are famously imprecise.
    return round(x)

# Generates a list of the partitions of "n" with at most "maxParts" parts that form valid Young tableau.
def generateTableaux(maxParts, n):
    # We need to reverse the lists given by generateHelper since these lists are increasing, not decreasing, by default
    return [list(reversed(tab)) for tab in generateHelper(maxParts, n, 0)]

# Iteratively generates the valid tableaux
def generateHelper(length, target_sum, start):
    if length == 0:
        return [[]] if target_sum == 0 else []

    validTableaux = []
    for i in range(start, target_sum + 1):
        if i > target_sum:
            break
        sub_tableaux = generateHelper(length - 1, target_sum - i, i)
        for tableau in sub_tableaux:
            validTableaux.append([i] + tableau)
    return validTableaux

# Generate a list of all tableaux of size "n". Not actually used in the final calculation.
def generateAllTableaux(n):
    return generateTableaux(n, n)

def run():

    k = int(input("Number of digits: "))
    maxLength = int(input("Max length to count: "))

    ballot(k, maxLength)

    # Some neat but unrelated examples follow. Checking these made use of the generateAllTableaux function.
    # Note, the sum of hook(T) for all tableaux T of size n is the coefficient of x^n/n! in e^(x+x^2/2),
    # and the sum of hook(T)^2 for all tableaux T of size n is n!


if __name__ == '__main__':
    run()

