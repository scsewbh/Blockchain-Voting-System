# Blockchain-Voting-System
A voting system designed using the blockchain. Proof of Concept (PoC)
Blockchain ledgers would ensure that votes are secure and unable to be tampered with. In addition, they can easily be validated. 

# How does the application work?
The user can go to a specialized website (or in person if required by state) and fill out a digital form. (This site can be tailored to specific candidates) 

Once the user submits their vote, which includes the user’s name, age, email address and other information. We can distinguish between unique users via a social security number or in our test case, a Google ID. 

The submission is then sent to be validated by the miners. Upon submission, the user will be greeted with something which shows the blockchain in its entirety. This allows for transparency. After mining, the vote is verified and counted!

# Front End/Voting System
#### Framework
+ Web framework created with Flask on Python 
+ Front end design created with Bootstrap Studio
+ Jinja and POST requests to get data to and from website
+ Deployed front end framework on Google App Engine


#### Pages 
+ The login.html page allows users to sign in with their google account and then redirects them to the voting page.
+ The register.html page allows a signed in user to submit a vote to the mempool. The page has five fields, three of which are auto filled from your google account public information. The fields the user must complete are their age and vote as shown in Figure 1. After the vote is submitted, the user is redirected to the results page. 
+ The results.html page displays the currently verified standings of each candidate in a bar graph. Below the graph is a table illustrating the current state of the blockchain as shown in Figure 2. 

# Mining
#### How the miners work
+ The miner first connects to our server. Our server, hosted on Google Cloud, helps all the miners stay connected and updated fully with the mempool and the blockchain. 
+ The miner then waits for transactions to appear in the mempool. Once a transaction appears, it can claim the transaction and start trying to find a valid hash based on the number of leading zeroes. This number can be set by us on the server. For testing purposes, it has been set at 2 or 3. 
+ If a user has already voted, it will not allow them to vote again. The front end will not allow this either, as it keeps track of who has voted. Of course in a real situation, there would be many more checks and verifications to make sure a single person cannot vote more than once. We verify this by using a unique ID that is included in each block data. 
+ The consensus protocol is then used to confirm a block when it has at least 51% of the miners in agreement. Since we have a very small example, this usually happens very quickly within our code and on our server. 


#### Mempool
+ For the mempool, first the front end adds the transaction to the mempool. The mempool is then shared with all the nodes, and each can claim a transaction to work on. In our case, each transaction is a vote. 


# Application Images

![Register](https://github.com/scsewbh/Blockchain-Voting-System/blob/main/images/register.png)

![Results](https://github.com/scsewbh/Blockchain-Voting-System/blob/main/images/results.png)
