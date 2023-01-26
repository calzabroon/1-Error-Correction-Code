import math
import random


file = open("text.txt", "r")
file_encoder = open("encoded.txt", "a")

file_encoder.truncate(0)

asciiDict = {i: chr(i) for i in range(128)}
codeWordDict = []


x = 'a'
file.seek(0)


distance = 0

error_rate = .0001


i = 0
z = 0
f = 0
i2 = 0

#this part here is not neccessary but i over complicated the encoding
#instead of having the binary value 0 and making it 000 for all 8 bits of the Ascii code
# i did this
# afterwards all code words are 3 bits apart but only require 12 bits becasue their order is different
for i in range(len(asciiDict)):
#for i in range(1):
  f = 0
  while (f < len(codeWordDict)):
    new_codeword = bin(round(z))[2:].zfill(12)
    #print(new_codeword)

    #to calculate the distance between new word and all words
    for i2 in range(12):
      #compare each bit 
      if ((int((codeWordDict[f])[i2]) != int(new_codeword[i2]))):
        distance += 1
    
    #if distance is valid then compare with next codeword
    if (distance >= 3):
      f = f + 1
    #if its not increment the new_codeword and start again
    else:
      f = 0
      z = z + 1
    distance = 0
  #adds new codeword to dictionary
  codeWordDict.append(bin(round(z))[2:].zfill(12))
  
print('the codeword dictionary: ', codeWordDict)


i = 0


while(1):
  
  character = file.read(1) #reads the next character
  
  if character != "": #continues if we are not at the end of the txt file
    
    #converts character to Ascii index
    Ascii_index = ord(character)
    if (Ascii_index <= 128):
      
      AsciiCodeWord = codeWordDict[Ascii_index]
      
      for i in range(12):
        #introduce random noise for 
        #can add noise for every bit in word
        if(random.randint(1,(1/error_rate)) == (1/error_rate)):
          if(AsciiCodeWord[i] == "1"):
            AsciiCodeWord_list = list(AsciiCodeWord)
            AsciiCodeWord_list[i] = "0"

            AsciiCodeWord = "".join(AsciiCodeWord_list)

          else:
            AsciiCodeWord_list = list(AsciiCodeWord)
            AsciiCodeWord_list[i] = "1"

            AsciiCodeWord = "".join(AsciiCodeWord_list)

      #prints encoded bit to encoded.txt
      #then sends word with new noise or no noise
      file_encoder.write(AsciiCodeWord)
    else:
      #for words that are not in ascii we send this which represets ctrl-@
      #this is so when we calcualate the error rate at tehn end the files are of the same size, so we have to send something
      file_encoder.write("000000000000")

  else:
    #here we are at the end of the file and therefore need to exit the loop which reads it
    break

file.close()


file_encoder.close()
file_encoder = open("encoded.txt", "r")

file_decoded = open("decoded.txt", "a")
file_decoded.truncate(0)

x = 'a'
file_encoder.seek(0)



checker = True
x = ""
i2 = 0
while(checker):
  #reads next codeword which we know is 12 bits
  for i in range(12):
    x = x + file_encoder.read(1)

  if (x in codeWordDict):

    file_decoded.write(asciiDict[codeWordDict.index(x)])
    x = ""
  else:
    if (x == ""):
      break
    min_distance = 12
    f = 0
    #print(x)
    closestWord = ""

    while (f < len(codeWordDict)):

    #to calculate the distance between new word and all words
      for i2 in range(12):
      #compare each bit 
        if (int((codeWordDict[f])[i2]) != int(x[i2])):
          distance += 1
    
    #if distance is valid then compare with next codeword
      if (distance < min_distance):
        closestWord = codeWordDict[f]
        min_distance = distance
      
      f += 1
      distance = 0

    #if it now any valid codeword, post the responding codeword
    if (closestWord in codeWordDict):
      file_decoded.write(asciiDict[codeWordDict.index(closestWord)])
    else:
      #to show there was an error
      file_decoded.write(asciiDict[0])
    

    if(x == ""):
      checker = False
    x = ""


file_decoded.close()

#to read the file and not fix any errors to calulate how noisy it really was

file_undecoded = open("undecoded.txt", "a")
file_undecoded.truncate(0)

x = 'a'
file_encoder.seek(0)

checker = True
x = ""
i2 = 0
while(checker):
  #reads next codeword which we know is 12 bits
  for i in range(12):
    x = x + file_encoder.read(1)

  if (x in codeWordDict):

    file_undecoded.write(asciiDict[codeWordDict.index(x)])
    x = ""
  else:
    #since read codeword is not in our dictionary print ctrl-@, so when we compare with text.txt it can detect the wrong character has been printed
    file_undecoded.write(asciiDict[0])
    
    if(x == ""):
      checker = False
    x = ""
  

file_undecoded.close()

file_encoder.close()


file = open("text.txt", "r")
file_decoded = open("decoded.txt", "r")
totalCorrectChar = 0
totalChar = 0

#this section calculates the accuracy of our error correction
while(1):
  
  character = file.read(1) #reads the next character
  character_decoded = file_decoded.read(1)
  
  if ((character != "") or (character_decoded != "")): #continues if we are not at the end of the txt file
    
    totalChar += 1
    #converts character to Ascii index
    if (character == character_decoded):
      totalCorrectChar += 1
      

  else:
    #here we are at the end of the file and therefore need to exit the loop which reads it
    break

print('With error correction')
print('correct: ', totalCorrectChar)
print('total: ', totalChar)
print('percentage: ', (float(totalCorrectChar))/(float(totalChar))*100, '%')


file.seek(0)
file_undecoded = open("undecoded.txt", "r")
totalCorrectChar = 0
totalChar = 0

#this section calulcates the text if there was no error correction
while(1):
  
  character = file.read(1) #reads the next character
  character_decoded = file_undecoded.read(1)
  
  if ((character != "") or (character_decoded != "")): #continues if we are not at the end of the txt file
    
    totalChar += 1
    #converts character to Ascii index
    if (character == character_decoded):
      totalCorrectChar += 1
      

  else:
    #here we are at the end of the file and therefore need to exit the loop which reads it
    break

print('\nWith no error correction')
print('correct: ', totalCorrectChar)
print('total: ', totalChar)
print('percentage: ', (float(totalCorrectChar))/(float(totalChar))*100, '%')

file.close()
file_decoded.close()
file_undecoded.close()



