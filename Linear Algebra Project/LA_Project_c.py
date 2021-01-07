#Linear Algebra Project
#By Jamal Uddin Ahamed
#Code for Command Line Interface based application, using Flask
import numpy as np
from sys import exit
from numpy import matrix
from numpy import linalg
import re
import time

global keyMatrix
global keyMatrix1
global inverseerror; inverseerror = 0

keyMatrix = [[0] * 3 for i in range(3)]
messageVector = [[0] for i in range(3)]
cipherMatrix = [[0] for i in range(3)] 

def getKeyMatrix(key): 
    k = 0
    for i in range(3): 
        for j in range(3):
            keyMatrix[i][j] = ord(key[k])
            k += 1
            
def encrypter_main(message, key):
    global keyMatrix
    global inverseerror        
    message1 = get_codon_list(message)
    print("\n\tThree letter word is : ",message)
    print("\n\tNine letter Key is : ",key)
    print("\n\tEncryption Block called")
    print("Key matrix generated is: ")
    print(keyMatrix)
    ciphered1 = []; ciphered2 = ""
    for message in message1:
        cipher = HillCipher(message, key)
        ciphered2 = ""
        ciphered2.join(cipher)
        new = "" 
        for x in cipher: 
            new += x   
        ciphered1.append(new)
        print()
    new = "" 
    for x in ciphered1: 
        new += x
    return new

def decrypter_main(message, key):
    global keyMatrix
    global inverseerror        
    message1 = get_codon_list(message)
    print("\n\tGiven input is : ",message)
    print("\n\tNine letter Key is : ",key)
    print("\n\tDecryption Block called")
    print("Key matrix generated is: ")
    print(keyMatrix)
    ciphered1 = []; ciphered2 = ""
    for message in message1:
        cipher = HilldeCipher(message, key)
        ciphered2 = ""
        ciphered2.join(cipher)
        new = "" 
        for x in cipher: 
            new += x   
        ciphered1.append(new)
        print()
    new = "" 
    for x in ciphered1: 
        new += x
    return new
            
def HillCipher(message, key):
    t0= time.clock()
    getKeyMatrix(key) 
    for i in range(3): 
        messageVector[i][0] = ord(message[i])
    print("Message vector : \n",messageVector)
    encrypt(messageVector) 
    CipherText = []
    print("Key Matrix : \n",keyMatrix)
    for i in range(3):
        ##print(int(cipherMatrix[i][0]))
        char = chr(int(cipherMatrix[i][0]))
        print(char)
        if int(cipherMatrix[i][0]) <= 31:CipherText.append("//" + str(hex(ord(char))) + "//")
        else:CipherText.append(chr(int(cipherMatrix[i][0])))   
        t1 = time.clock() - t0
        print("Time elapsed: ", t1) # CPU seconds elapsed (floating point)
    return CipherText
    
def HilldeCipher(message, key):
    global keyMatrix
    getKeyMatrix(key)
    keyMatrix = modMatInv(keyMatrix,122)
    for key1 in keyMatrix:print(key1)
    for i in range(3): 
        messageVector[i][0] = ord(message[i])
    #print("Deciphered Message Vector : ",messageVector)
    decrypt(messageVector)    
    CipherText = [] 
    for i in range(3):
        #print(int(cipherMatrix[i][0]))
        CipherText.append(chr(int(cipherMatrix[i][0])))  
    #print("Original Text: ", "".join(CipherText))
    return CipherText

def encrypt(messageVector): 
    for i in range(3): 
        for j in range(1): 
            cipherMatrix[i][j] = 0
            for x in range(3): 
                cipherMatrix[i][j] += (keyMatrix[i][x] * messageVector[x][j]) 
            cipherMatrix[i][j] = cipherMatrix[i][j] % 122
    #print(cipherMatrix)

def decrypt(cipher_text):
    for i in range(3): 
        for j in range(1): 
            cipherMatrix[i][j] = 0
            for x in range(3): 
                cipherMatrix[i][j] += (keyMatrix[i][x] * messageVector[x][j]) 
            cipherMatrix[i][j] = cipherMatrix[i][j] % 122
    #print("Deciphered : ",cipherMatrix)
    
   
def get_codon_list(codon_string):
    codon_length = 3
    codon_list = []
    for codon_start in range(0, len(codon_string), codon_length):
        codon_end = codon_start + codon_length
        codon_list.append(f"{codon_string[codon_start:codon_end]:<3}")
    return codon_list

def modMatInv(A,p):
    n = len(A)
    A = matrix(A)
    #print(A)
    adj = np.zeros(shape=(n,n))
    for i in range(0,n):
        for j in range(0,n):
            adj[i][j]=((-1)**(i+j)*int(round(linalg.det(minor(A,j,i)))))%p
    try:
        #print((modInv(int(round(linalg.det(A))),p)*adj)%p)
        return (modInv(int(round(linalg.det(A))),p)*adj)%p
    except:global inverseerror; inverseerror = 1

def modInv(a,p):
    for i in range(1,p):
        if (i*a)%p==1:return i
    global inverseerror; inverseerror = 1
    raise ValueError(str(a)+" has no inverse mod "+str(p))

def minor(A,i,j):
    A=np.array(A)
    minor=np.zeros(shape=(len(A)-1,len(A)-1))
    p=0
    for s in range(0,len(minor)):
          if p==i:p=p+1
          q=0
          for t in range(0,len(minor)):
                if q==j:
                    q=q+1
                minor[s][t]=A[p][q]
                q=q+1
          p=p+1
    return minor

def clean_string(message):
    for i in range(0, int((len(message)/2))):
        match = re.search(r'//0x?([^//>]+)', message)
        try:val1 = str(match.group(1))
        except:pass
        message = message.replace("//0x"+val1+"//",str(chr(int(str("0x"+val1),16))), 1) 
    return message
def first_intro():
    print("\n\n\t\t\tHello User")
    
def main_menu():
    print("\t1.Encrypt Direct Input")
    print("\t2.Decrypt Direct Input")   
    print("\t3.Encrypt Input from file")
    print("\t4.Decrypt Input from file")
    print("\t5.Exit")    

def input_key():
    while True:
        key = input("\n\tEnter 9 letter Key : ")
        try:
            modMatInv(keyMatrix, 122)
            return key
        except:
            if inverseerror == 1 or "1":return key
            
def main():
    global keyMatrix
    global inverseerror
    first_intro()
    ch=""
    while True:
        main_menu()
        ch = input("\n\tSelect Your Option ELse press any key to exit : ")
        if ch == '1':
            message = input("\n\tEnter your message : ")
            key = input_key()
            ciphered = encrypter_main(message,key)
            print("Obtained Cipher : ",ciphered)
            break
        
        elif ch == '2':
            ciphered = input("\n\tEnter your Encrypted message : ")
            key = input_key()
            ciphered = clean_string(ciphered)
            deciphered = decrypter_main(ciphered,key)
            print("Decipher message : ",deciphered)
            break
        
        elif ch == '3':
            file_name = input("\n\tEnter Input file name : ")
            file_name_e = input("\n\tEnter Enc output file name : ")
            key = input_key()
            fhand = open(file_name,"r")
            message = fhand.read()
            fhand.close()
            ciphered = encrypter_main(message,key)
            fhand = open(file_name_e,"w")
            fhand.write(ciphered)
            fhand.close()
            
        elif ch == '4':
            file_name = input("\n\tEnter Input enc file name : ")
            file_name_d = input("\n\tEnter Dec output file name : ")
            key = input_key()
            fhand = open(file_name,"r")
            ciphered = fhand.read()
            ciphered = clean_string(ciphered)
            fhand.close()
            deciphered = decrypter_main(ciphered,key)
            fhand = open(file_name_d,"w")
            fhand.write(deciphered)
            fhand.close()
            
        elif ch == '5':exit()
        else:exit()
      
if __name__ == "__main__": 
    main() 