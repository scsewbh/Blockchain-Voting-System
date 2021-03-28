from time import time
import hashlib


class Block():

    def __init__(self, data, previous_hash):
        self.timestamp = time(),
        self.data = data
        self.previous_hash = previous_hash
        self.hash = hashlib.sha256(previous_hash.encode()).hexdigest()


str1 = "abcde"

str2 = "Hi my name is Eric"

str3 = "wjfkbwiucbiwucbiwcbiuwbiuwhiwuehwiuehiwundiuwnbdiuwhdiuwhe"

str4 = "990304"
result1 = hashlib.sha256(str1.encode())
result2 = hashlib.sha256(str2.encode())
result3 = hashlib.sha256(str3.encode())
result4 = hashlib.sha256(str4.encode())


print(result1.hexdigest())
print(result2.hexdigest())
print(result3.hexdigest())
print(result4.hexdigest())

for i in range(0, 1000000):
    testString = str(i)
    r = hashlib.sha256(testString.encode())
    r = r.hexdigest()
    if r[0] == "0" and r[1] == "0" and r[2] == "0":
        nonce = i
        break

print("Found an input of " + str(nonce))
