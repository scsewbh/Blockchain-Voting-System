from time import time


class Data:
    def __init__(self, id, fname, lname, age, email, vote):

        self.timestamp = time()

        self.id = id
        self.fname = fname
        self.lname = lname
        self.age = age
        self.email = email
        self.vote = vote
