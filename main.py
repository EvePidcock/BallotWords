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

    # My implementation of the hook length formula. This is a slightly simplified version with only one
    # factorial per m value (k total) instead of the original with two factorials for every j value (k^2-k total).
    # In theory, if the multiplications get too big before the division step brings it back down, there may be an
    # issue if the integer limit is hit. I can't remember how Python deals with that, though. Further, that is
    # almost certainly not going to happen, since this program struggles with even slightly large values of k and n.
    for m in range(1, k+1):
        for j in range(2, m+1):
            x *= (tableau[j - 2] - tableau[m - 1] + m - j + 1)
        x /= math.factorial(tableau[m - 1] + k - m)

    # (Debug)
    # print(tableau, round(x))

    # Return the total. The above formula always gives an integer, but we need to round because
    # there is division using floating point numbers, which are famously imprecise.
    return round(x)

# Generates a list of the partitions of "n" with at most "maxParts" parts that form valid Young tableau.
def generateTableaux(maxParts, n):

    # Get a list of the numbers between 0 and n (there is probably a faster way to do this)
    rowValues = []
    for i in range(n + 1):
        rowValues.append(i)

    # Initiate the list of valid tableaux shapes
    validTableaux = []

    # A tableau of size n can not have more than n parts. This makes the loop a bit smaller
    if maxParts > n:
        maxParts = n

    # Iterate over all tuples in the set {0,...,n}^(maxParts)
    for potentialTableauxTuple in itertools.product(rowValues, repeat=maxParts):

        # Turn the tuple into a list so that it is easier to work with
        potentialTableauxList = list(potentialTableauxTuple)

        # If the numbers chosen for the parts do not add up to n, disregard the tuple.
        # Since we throw out so many of the tuples we iterate over, this for loop is highly inefficient;
        # however, I am not sure how to avoid doing this. At least, not in a way that isn't absurd.
        if sum(potentialTableauxList) != n:
            continue

        valid = True
        # At each row, make sure it is not smaller than the row above it. If it is, set valid=False to
        # indicate that this is not a valid shape for a tableau.
        for i in range(maxParts - 1):
            if potentialTableauxList[i] < potentialTableauxList[i+1]:
                valid = False
                break

        # If the shape is valid for a tableau, add it to the list
        if valid:
            validTableaux.append(potentialTableauxList)

    # Return the list of valid tableau shapes.
    return validTableaux

# Generate a list of all tableaux of size "n"
def generateAllTableaux(n):
    return generateTableaux(n, n)

def run():

    k = int(input("Number of digits: "))
    maxLength = int(input("Max length to count: "))

    ballot(k, maxLength)

    # Note, the sum of hook(T) for all tableaux T of size n is the coefficient of x^n/n! in e^(x+x^2/2),
    # and the sum of hook(T)^2 for all tableaux T of size n is n!


if __name__ == '__main__':
    run()

