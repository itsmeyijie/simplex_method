import numpy as np


class LinearModel:

    def __init__(self, A=np.empty([0, 0]), b=np.empty([0, 0]), c=np.empty([0, 0]), minmax="MAX"):
        self.A = A
        self.b = b
        self.c = c
        self.x = [float(0)] * len(c)
        self.minmax = minmax
        self.printIter = True
        self.optimalValue = None
        self.transform = False

    def addA(self, A):
        self.A = A

    def addB(self, b):
        self.b = b

    def addC(self, c):
        self.c = c
        self.transform = False

    def setObj(self, minmax):
        if (minmax == "MIN" or minmax == "MAX"):
            self.minmax = minmax
        else:
            print("Invalid objective.")
        self.transform = False

    def setPrintIter(self, printIter):
        self.printIter = printIter

    def printSoln(self):
        print("Coefficients: ")
        print(self.x)
        print("Optimal value: ")
        print(self.optimalValue)

    def printTableau(self, tableau):

        print("ind \t\t", end="")
        for j in range(0, len(c)):
            print("x_" + str(j), end="\t")
        for j in range(0, (len(tableau[0]) - len(c) - 2)):
            print("s_" + str(j), end="\t")

        print()
        for j in range(0, len(tableau)):
            for i in range(0, len(tableau[0])):
                if (not np.isnan(tableau[j, i])):
                    if (i == 0):
                        print(int(tableau[j, i]), end="\t")
                    else:
                        print(round(tableau[j, i], 2), end="\t")
                else:
                    print(end="\t")
            print()

    def getTableau(self):
        # construct starting tableau

        if (self.minmax == "MIN" and self.transform == False):
            self.c[0:len(c)] = -1 * self.c[0:len(c)]
            self.transform = True

        t1 = np.array([None, 0])
        numVar = len(self.c)
        numSlack = len(self.A)

        t1 = np.hstack(([None], [0], self.c, [0] * numSlack))

        basis = np.array([0] * numSlack)

        for i in range(0, len(basis)):
            basis[i] = numVar + i

        A = self.A

        if (not ((numSlack + numVar) == len(self.A[0]))):
            B = np.identity(numSlack)
            A = np.hstack((self.A, B))

        t2 = np.hstack((np.transpose([basis]), np.transpose([self.b]), A))

        tableau = np.vstack((t1, t2))

        tableau = np.array(tableau, dtype='float')

        return tableau

    def optimize(self):

        if (self.minmax == "MIN" and self.transform == False):
            for i in range(len(self.c)):
                self.c[i] = -1 * self.c[i]
                transform = True

        tableau = self.getTableau()
        # assume initial basis is not optimal
        optimal = False
        # keep track of iterations for display
        iter = 1

        while (True):



            if (self.minmax == "MAX"):
                for profit in tableau[0, 2:]:
                    if profit > 0:
                        optimal = False
                        break
                    optimal = True
            else:
                for cost in tableau[0, 2:]:
                    if cost < 0:
                        optimal = False
                        break
                    optimal = True

            # if all directions result in decreased profit or increased cost
            if optimal == True:
                break

            # nth variable enters basis, account for tableau indexing
            if (self.minmax == "MAX"):
                n = tableau[0, 2:].tolist().index(np.amax(tableau[0, 2:])) + 2
            else:
                n = tableau[0, 2:].tolist().index(np.amin(tableau[0, 2:])) + 2

            # minimum ratio test, rth variable leaves basis
            minimum = 99999
            r = -1
            for i in range(1, len(tableau)):
                if (tableau[i, n] > 0):
                    val = tableau[i, 1] / tableau[i, n]
                    if val < minimum:
                        minimum = val
                        r = i

            pivot = tableau[r, n]
            # perform row operations
            # divide the pivot row with the pivot element
            tableau[r, 1:] = tableau[r, 1:] / pivot

            # pivot other rows
            for i in range(0, len(tableau)):
                if i != r:
                    mult = tableau[i, n] / tableau[r, n]
                    tableau[i, 1:] = tableau[i, 1:] - mult * tableau[r, 1:]
                    # new basic variable
            tableau[r, 0] = n - 2
            iter += 1
        self.x = np.array([0] * len(c), dtype=float)
        # save coefficients
        for key in range(1, (len(tableau))):
            if (tableau[key, 0] < len(c)):
                self.x[int(tableau[key, 0])] = tableau[key, 1]

        self.optimalValue = -1 * tableau[0, 1]

model1 = LinearModel()

A = np.array([[2, -1, 3],
              [1, 2, 4]])
b = np.array([30, 40])
c = np.array([4, 2,8])

model1.addA(A)
model1.addB(b)
model1.addC(c)

print("A =\n", A, "\n")
print("b =\n", b, "\n")
print("c =\n", c, "\n")
model1.optimize()
print("\n")
model1.printSoln()