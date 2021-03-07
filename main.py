#Strassens Encryption
#Andi Brandsness, Finn McClone, James Holtz

import strassens
import sys

#############################
# global variables

# generate our matricies
mLength = 16
key = []
keyL = []
keyU = []
keyLi = []
keyUi = []
keyLoaded = False
for i in range(mLength):
    key.append([])
    for j in range(mLength):
        key[i].append(0)
exitCode = False
textMatrix = []
test = []
code = []

###############################
# Functions

def promptUser():
    print()
    print("Would you like to:")
    print("1) Load passkey")
    print("2) Generate a passkey")
    print("3) Code a message")
    print("4) Decode a message")
    print("5) Ask for help")
    print("6) Exit program")
    print("Enter the number for desired action")
    userChoice = int(input())
    print()
    return userChoice

#############################
# main
print()
print("Welcome to Super-Duper Secure Messaging System")  

while exitCode == False:
    action = promptUser()

    # load a premade key
    if action == 1:
        # prompt user for file name
        print("Enter key's file name")
        file_name = input()
        if '.txt' not in file_name: #make sure it has .txt extension
            file_name += '.txt'
        f = open(file_name, "r")
        inputData = f.read()
        f.close()

        # take data and store into key
        keyDataStr = inputData.strip().split()
        for i in range(mLength):
            for j in range(mLength):
                key[i][j] = int(keyDataStr[i * mLength + j])

        # set the L, U and inverses
        keyL = strassens.GetL(key, mLength)
        keyU = strassens.GetU(key, mLength)
        keyLi = strassens.getInverseL(keyL, mLength)
        keyUi = strassens.getInverseU(keyU, mLength)
        keyLoaded = True

    # generate a new key
    elif action == 2:
        key = strassens.generateLU(mLength, 41)

        # set the L, U and inverses
        keyL = strassens.GetL(key, mLength)
        keyU = strassens.GetU(key, mLength)
        keyLi = strassens.getInverseL(keyL, mLength)
        keyUi = strassens.getInverseU(keyU, mLength)
        checkL = strassens.Strassen(keyL, keyLi)
        checkU = strassens.Strassen(keyU, keyUi)
        keyLoaded = True

    # encrypt a message
    elif action == 3:
        if not keyLoaded:
            print("No key has been loaded")
        else:
            # get text to encode
            confirm = 2
            while confirm != 1:
                print("Please enter your message bellow.")
                print("Please keep your text under 256 characters.")
                print("Everything after that will be deleted.")
                text = input()
                textMatrix = strassens.TextToMatrix(text, mLength)
                print("This is your message")
                print(strassens.MatrixToText(textMatrix))
                print("Enter 1 to confirm this as your message")
                print("Enter 2 to change message")
                confirm = int(input())
            # code the message
            tempMatrix = strassens.Strassen(keyL, textMatrix)
            encryptedMatrix = strassens.Strassen(keyU, tempMatrix)
            print("Your text has been encrypted. What name would you like the file to have?")
            file_name = input()
            strassens.MatrixToFile(encryptedMatrix, file_name)
            print("Your file has been saved")

    # decrpyt a message
    elif action == 4:
        if not keyLoaded:
            print("No key has been loaded")
        else:
            print("Enter the file name to decrpyt")
            file_name = input()
            if '.txt' not in file_name: #make sure it has .txt extension
                file_name += '.txt'
            encrpytedMatrix = strassens.FileToMatrix(file_name, mLength)
            tempMatrix = strassens.Strassen(keyUi, encrpytedMatrix)
            textMatrix = strassens.Strassen(keyLi, tempMatrix)
            print("The message is:")
            print(strassens.MatrixToText(textMatrix))


    # ask for help
    elif action == 5:
        print("This is a program to encrypt and decrypt messages.")
        print("The first step is to load a key.")
        print("If you already have a key, you will input the name of the file.")
        print("If you do not have a key, you can generate one.")
        print("Once you have loaded a key, you can encrypt or decrypt messages.")
        print("If you need to load a new key, you can do so.")


    # Exit the program
    elif action == 6:
        exitCode = True