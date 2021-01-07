#Linear Algebra Project
#By Jamal Uddin Ahamed
#Code for Graphical User Interface based application, using Flask
import re
#from sys import exit
import webbrowser
from flask import Flask, send_from_directory, request, render_template
import numpy as np
from numpy import matrix
from numpy import linalg

global keyMatrix
global keyMatrix1
global inverseerror; inverseerror = 0

app = Flask(__name__, static_folder='views')

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
    getKeyMatrix(key) 
    for i in range(3): 
        messageVector[i][0] = ord(message[i])
    print("Message vector : ",messageVector)
    encrypt(messageVector) 
    CipherText = [] 
    for i in range(3):
        print(int(cipherMatrix[i][0]))
        char = chr(int(cipherMatrix[i][0]))
        print(char)
        if int(cipherMatrix[i][0]) <= 31:CipherText.append("//" + str(hex(ord(char))) + "//")
        else:CipherText.append(chr(int(cipherMatrix[i][0])))   
    print("Ciphertext: ", "".join(CipherText))
    return CipherText
    
def HilldeCipher(message, key):
    global keyMatrix
    getKeyMatrix(key)
    keyMatrix = modMatInv(keyMatrix,122)
    #print(keyMatrix)
    for key1 in keyMatrix:print(key1)
    for i in range(3): 
        messageVector[i][0] = ord(message[i])
    print("Deciphered Message Vector : ",messageVector)
    decrypt(messageVector)    
    CipherText = [] 
    for i in range(3): 
        CipherText.append(chr(int(cipherMatrix[i][0])))  
    print("Original Text: ", "".join(CipherText))
    return CipherText

def encrypt(messageVector): 
    for i in range(3): 
        for j in range(1): 
            cipherMatrix[i][j] = 0
            for x in range(3): 
                cipherMatrix[i][j] += (keyMatrix[i][x] * messageVector[x][j]) 
            cipherMatrix[i][j] = cipherMatrix[i][j] % 122
    print(cipherMatrix)

def decrypt(cipher_text):
    for i in range(3): 
        for j in range(1): 
            cipherMatrix[i][j] = 0
            for x in range(3): 
                cipherMatrix[i][j] += (keyMatrix[i][x] * messageVector[x][j]) 
            cipherMatrix[i][j] = cipherMatrix[i][j] % 122
    print("decipher decrypt : ",cipherMatrix)
    
   
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
  print(A)
  adj = np.zeros(shape=(n,n))
  for i in range(0,n):
      for j in range(0,n):
          adj[i][j]=((-1)**(i+j)*int(round(linalg.det(minor(A,j,i)))))%p
  try:
      print((modInv(int(round(linalg.det(A))),p)*adj)%p)
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
    if p==i:
      p=p+1
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
        try:
            val1 = str(match.group(1))
        except:pass
        message = message.replace("//0x"+val1+"//",str(chr(int(str("0x"+val1),16))), 1)
        #print(message) 
    return message    

def main():
    global keyMatrix
    global inverseerror
    message = input("\n\tEnter your message : ")
    #message = "hi how are you all hi tere"
    while True:
        #key = "SeheLOeee"
        key = input("\n\tEnter 9 letter Key : ")
        try:
            modMatInv(keyMatrix, 122)
            break
        except:
            if inverseerror == 1 or "1":pass
    ciphered = encrypter_main(message,key)
    deciphered = decrypter_main(ciphered,key)
    print("\n\tEncrypted Text is : ",ciphered)
    print("\n\tDecrypted Text is : \n\t",deciphered)

@app.route("/")
def index():return render_template('index.html')

@app.route("/main/encrypt", methods=["GET"], strict_slashes=False)
def encrypt_get_1():
  explanation = ""
  return render_template("encrypt_get.html",explanation = explanation,encrypt = "active")

@app.route("/main/encrypt", methods=["POST"], strict_slashes=False)
def encrypt_post_1():
  message = request.form.get("message")
  key_1 = request.form.get("key1")
  key = key_1
  if message and key:
    encrypted_message = encrypter_main(message, key)
    return render_template("encrypt_post.html",key = key,message = message,encrypted_message = encrypted_message,encrypt = "active")
  else:
    return render_template("error.html")

@app.route("/main/decrypt", methods=["GET"], strict_slashes=False)
def decrypt_get_1():
  explanation = ""
  return render_template("decrypt_get.html",explanation = explanation,decrypt = "active")  
  
@app.route("/main/decrypt", methods=["POST"], strict_slashes=False)
def decrypt_post_1():
  message = request.form.get("message")
  key_1 = request.form.get("key1")
  key = key_1
  if message and key:
    message = clean_string(message)
    decrypted_message = decrypter_main(message, key)
    return render_template("decrypt_post.html",key = key,message = message,decrypted_message = decrypted_message,decrypt = "active")
  else:
    return render_template("error.html")
 
@app.route("/main", strict_slashes=False)
def main_page():
  explanation = ""
  return render_template("main.html",explanation = explanation)

@app.route('/<path:path>', strict_slashes=False)
def send_static(path):
  return send_from_directory('public', path)

if __name__ == "__main__":
  webbrowser.open_new('http://localhost')
  app.run(host='0.0.0.0', port = 80)