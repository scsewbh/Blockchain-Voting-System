import hashlib
from Data import *


class Block:
    def __init__(self, id, fname, lname, age, email, vote, previous_hash):

        self.data = Data(id, fname, lname, age, email, vote)

        self.previous_hash = previous_hash
        h = str(self.data.id) + self.data.fname + self.data.lname + str(self.data.age) + self.data.email + self.data.vote + self.previous_hash

        self.hash = str(h.encode().hex())


