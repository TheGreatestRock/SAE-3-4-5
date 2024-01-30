#take a String and every 2048 characters, write the 2048 last characters in a text file
def writeInFile(string):
    i = 0
    filenumber = 0
    while i < len(string):
        with open('C:/Users/thegr/Documents/cours_IUT_2022_2023/S2/SAE/SAE 3-4-5/SAE-3-4-5/aide/help'+str(filenumber)+'.txt', 'w') as myfile:
            myfile.write(string[i:i+2048])
        i += 2048
        filenumber += 1
        print(i)

writeInFile()