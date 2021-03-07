#Strassens Encryption
#Andi Brandsness, Finn McClone, James Holtz


import secrets #This is a more secure way to generate random numbers
# Updated 12/13 with a bunch of functions

# Tells strassen how to add two matrices A and B
def AddMatrices(A, B):
    n = len(A) # dimension of A and B
    C = [[0. for i in range(n)] for j in range(n)] #Make an empty matrix the same size
    for i in range(n):
        for j in range(n):
            #add each number of A to the corresponding number in B, 
            # place it in the corresponding spot in C
            C[i][j] = A[i][j] + B[i][j] 

    return C

# Matrix multiplication algorithm. 
# Input: 2 matrices, A and B, both square and of dimension nxn where n is a power of 2
# Output: C, an nxn matrix where C = A*B
def Strassen(A, B):
    n = len(A) # dimension of current matrices
    if n == 2: #if 2x2 go straight to strassens
        C = [[0. for i in range(n)] for j in range(n)] #make a 2x2 of zeros
        # Strassens's 7 multiplications
        m1 = (A[0][0] + A[1][1]) * (B[0][0] + B[1][1])
        m2 = (A[1][0] + A[1][1]) * B[0][0]
        m3 = A[0][0] * (B[0][1] - B[1][1])
        m4 = A[1][1] * (B[1][0] - B[0][0])
        m5 = (A[0][0] + A[0][1]) * B[1][1]
        m6 = (A[1][0] - A[0][0]) * (B[0][0] + B[0][1])
        m7 = (A[0][1] - A[1][1]) * (B[1][0] + B[1][1])
        # fill C with its 4 values
        C[0][0] = round(m1 + m4 - m5 + m7)
        C[0][1] = round(m3 + m5)
        C[1][0] = round(m2 + m4)
        C[1][1] = round(m1 + m3 - m2 + m6)
        #done! 2x2 * 2x2 is caluculated
        return C
    
    elif n > 2: # 4, 8, 16, 32, ...
        #make A and B into four new sub matrices each, where the submatrices are (n/2)x(n/2)
        
        new_n = int(n/2) #new matrices will be half the dimension of the originals
        #make 8 matrices of zeros, that will be the 4 corners of the two matrices we're splitting up
        a1 = [[0. for i in range(new_n)] for j in range(new_n)]
        a2 = [[0. for i in range(new_n)] for j in range(new_n)]
        a3 = [[0. for i in range(new_n)] for j in range(new_n)]
        a4 = [[0. for i in range(new_n)] for j in range(new_n)]
        b1 = [[0. for i in range(new_n)] for j in range(new_n)]
        b2 = [[0. for i in range(new_n)] for j in range(new_n)]
        b3 = [[0. for i in range(new_n)] for j in range(new_n)]
        b4 = [[0. for i in range(new_n)] for j in range(new_n)]
        #fill in the matrices from A and B respectively
        for i in range(0, new_n):
            for j in range(0, new_n):
                a1[i][j] = A[i][j]
                a2[i][j] = A[i][j+new_n]
                a3[i][j] = A[i+new_n][j]
                a4[i][j] = A[i+new_n][j+new_n]
                b1[i][j] = B[i][j]
                b2[i][j] = B[i][j+new_n]
                b3[i][j] = B[i+new_n][j]
                b4[i][j] = B[i+new_n][j+new_n]


        #parts of matrix C = A*B
        #this is matrix multiplication of smaller matrices. 
        # e.g. the top left quadrant of C, c1, is the product of the top row of A, a1 and a2, and the left column of B, b1 and b3
        c1 = AddMatrices( Strassen(a1, b1), Strassen(a2, b3) ) 
        c2 = AddMatrices( Strassen(a1, b2), Strassen(a2, b4) )
        c3 = AddMatrices( Strassen(a3, b1), Strassen(a4, b3) )
        c4 = AddMatrices( Strassen(a3, b2), Strassen(a4, b4) )

        C = [[0. for i in range(n)] for j in range(n)] #original size, not halfed. 
        #put the pieces of C back together
        for i in range(0, n):
            for j in range(0, n):
                if i < new_n and j < new_n:
                    C[i][j] = c1[i][j]
                elif i < new_n and j >= new_n:
                    C[i][j] = c2[i][j-new_n]
                elif i >= new_n and j < new_n:
                    C[i][j] = c3[i-new_n][j]
                else:
                    C[i][j] = c4[i-new_n][j-new_n]
        
        return C 


# Randomly generates a nxn invertible matrix in LU form
#  Input: n = Dimension of square matrix, m = max random value
# Output: Random nxn matrix with values between 0 and m
#         key_file that holds LU, with spaces after each entry and \n after each row 
#         Matrix in LU form, meaning
#         U = entries on and above the diagonal, with 0s below the diagonal
#         L = entries below the diagonal, with 1s on the diagonal, and 0s above the diagonal
def generateLU(n, m):
    print("What would you like to name the key?")
    file_name = input()
    if '.txt' not in file_name: #make sure it has .txt extension
        file_name += '.txt'
    key_file = open(file_name,'w')
    LU = [[0. for i in range(n)] for j in range(n)] # make matrix of size n
    for i in range(n):
        for j in range(n):
            x = secrets.randbelow(m) #choose a random number
            LU[i][j] = x #put the random number into the matrix
            key_file.write(str(x) + ' ') #write it to file with a space following
        key_file.write('\n') #newline after each row ends

    key_file.close()
    return LU

# Separates U so it can be used individually
# Input: LU Matrix, dimension n of LU
def GetU(LU, n):
    U = [[0. for i in range(n)] for j in range(n)] #make empty nxn matrix
    for i in range(n):
        for j in range(n):
            if j > i: # U is the upper right triangle of LU 
                U[i][j] = LU[i][j]
            elif j == i: # make diagonal all 1s
                U[i][j] = 1
    return U

# Separates L so it can be used individually
# Input: LU Matrix, dimension n of LU
def GetL(LU, n): 
    L = [[0. for i in range(n)] for j in range(n)] # make empty nxn matrix
    for i in range(n):
        for j in range(n):
            if j < i: # L is the bottom left triangle of LU
                L[i][j] = LU[i][j]
            elif j == i: # set diagonal to 1s
                L[i][j] = 1
    return L


#  Input: text 256 chars or less
# Output: 16x16 Matrix A with each letter of the text (no symbols or spaces) 
#         converted to numbers (A = 1, B = 2, ... , Z = 26) 
#         message_file that holds A, with spaces after each entry and \n after each row 
def TextToMatrix(text, n):
    #message_file = open('message_file.txt','w')
    clean_text = []
    for a in text:
        #remove symbols and spaces, and make uppercase
        if a.isalnum():
            a = a.upper()
            clean_text.append(a)

    letterKey = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9, 'J':10, 'K':11, 'L':12, 'M':13, 'N':14, 
                'O':15, 'P':16, 'Q':17, 'R':18, 'S':19, 'T':20, 'U':21, 'V':22, 'W':23, 'X':24, 'Y':25, 'Z':26}
    A = [[0. for i in range(n)] for j in range(n)] # Set A to all zeros

    for i in range(n):
        for j in range(n):
            if len(clean_text) > 0:
                x = letterKey[clean_text.pop(0)] # put the first letter in the martix in number form
                A[i][j] = x
    #            message_file.write(str(x) + ' ')
    #        else:
    #            message_file.write(str(0) + ' ')
    #    message_file.write('\n')
    
    #message_file.close()
    return A

# Could call this function in GenerateLU and TextToMatrix instead of doing it manually
# Takes a matrix M and writes it to a file
def MatrixToFile(M, file_name):
    if '.txt' not in file_name: #make sure it has .txt extension
        file_name += '.txt'
    f = open(file_name, 'w') #open file to write
    n = len(M)
    for i in range(n):
        for j in range(n):
            f.write(str(M[i][j]) + ' ') #space after each column
        f.write('\n') # newline after each row
    f.close()

# Input: matrix M that is decoded but still in number form
# Output: returns the text contained in the matrix and writes it to 'decoded_text.txt'
def MatrixToText(M):
    n = len(M)
    text = ''
    letterKey = {0:' ', 1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F', 7:'G', 8:'H', 9:'I', 10:'J', 11:'K', 12:'L', 13:'M', 14:'N', 
                15:'O', 16:'P', 17:'Q', 18:'R', 19:'S', 20:'T', 21:'U', 22:'V', 23:'W', 24:'X', 25:'Y', 26:'Z'}
    for i in range(n):
        for j in range(n):
            text += letterKey[ M[i][j] ]
    #f = open('decoded_text.txt', 'w')
    #f.write(text)
    return text

def FileToMatrix(file_name, n):
    A = [[0. for i in range(n)] for j in range(n)] # Set A to all zeros
    f = open(file_name, "r")
    inputString = f.read()
    f.close()
    inputList = inputString.strip().split()
    for i in range(n):
        for j in range(n):
            A[i][j] = float(inputList[i * n + j])
    return A


# input:    U: the U matrix
#           n: the size of the U matrix
# output:   Ui: the inverse of U
def getInverseU(U, n):
    # start by generating Ui as the identity matrix
    Ui = [[0. for i in range(n)] for j in range(n)]
    for i in range(n):
        Ui[i][i] = 1

    # start at the bottom of U
    for i in range(n - 1, -1, -1):
        # start by making all the values after i = 0
        for j in range(i + 1, n):
            # add the row j * -j to the row i
            scale = U[i][j]
            for k in range(n):
                Ui[i][k] = Ui[i][k] - scale * Ui[j][k]

    return Ui

# input:    L: a lower triangle matrix
#           n: the size of the matrix L
# output:   Li: inverse of matrix L
def getInverseL(L, n):
    # generate Li
    Li = [[0. for i in range(n)] for j in range(n)]
    for i in range(n):
        Li[i][i] = 1

    # work from the top down
    for i in range(n):
        # work from left to right to make the values 0
        for j in range(0,i):
            scale = L[i][j]
            # go through row and change values
            for k in range(0, n):
                Li[i][k] = Li[i][k] - scale * Li[j][k]
    return Li
