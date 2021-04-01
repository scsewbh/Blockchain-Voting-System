from Block import *


blockZero = "zeroHash"
voter = Block(1, "mike", "smith", 23, "voter@gmail.com", "Poggers", blockZero) #block for voter created


#mining software:
for i in range(0, 1000000):
    testString = str(i)
    r = hashlib.sha256(testString.encode())
    r = r.hexdigest()

    if r[0] == "0" and r[1] == "0" and r[2] == "0":
        nonce = i
        break

print("Found an input of " + str(nonce)) #this is the first found nonce value for the block
