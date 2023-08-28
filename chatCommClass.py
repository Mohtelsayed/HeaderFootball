##THIS CODE COMES FROM MY HW7 IT IS SLIGHTLY TWEAKED BUT 95% IS COPIED

import socket as s

########## FILL IN THE FUNCTIONS TO IMPLEMENT THE CHATCOMM CLASS ##########
class chatComm:
    def __init__(self,ipaddress,portnum):
        self.ipAddress = ipaddress
        self.port = portnum 
        
    def startConnection(self):
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.socket.connect((self.ipAddress,self.port))

    #Helper for the login function that generates the block
    # and corresponding ASCII caculations
    def helperBlockASCIIGenerate(self,password,challenge):
        passSize = len(password)
        chalSize = len(challenge)
        message = password+challenge
        block = message + "1"
        while len(block) + len(message) + 3 <= 512:
            block += message
        block += ("0"* (509-len(block))) + (
            "0" * (3-len(str(passSize + chalSize))))+ str(passSize + chalSize)
        M = []
        for i in range(16):
            sumASCII = 0
            for j in range(32):
                sumASCII += ord(block[(32*i)+j])
            M += [sumASCII]
        return block, M

    #Helper login function that Initialises the variables that will be used in
    # the MD5 Algorithm
    def helperInitialiseVars(self):
        s = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 5, 9,
             14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,4, 11, 16, 23,
             4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,6, 10, 15, 21, 6, 10,
             15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
        K = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf,
             0x4787c62a, 0xa8304613, 0xfd469501, 0x698098d8, 0x8b44f7af,
             0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e,
             0x49b40821, 0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
             0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8, 0x21e1cde6,
             0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8,
             0x676f02d9, 0x8d2a4c8a, 0xfffa3942, 0x8771f681, 0x6d9d6122,
             0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
             0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039,
             0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, 0xf4292244, 0x432aff97,
             0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d,
             0x85845dd1, 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
             0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391]
        a0, A, b0, B, c0, C, d0, D = (0x67452301, 0x67452301, 0xefcdab89,
        0xefcdab89, 0x98badcfe, 0x98badcfe, 0x10325476, 0x10325476)
        return s, K, a0, A, b0, B, c0, C, d0, D

    #Help for the MDF Algorithm that Left rotates as described in HW
    def helperLeftRotate (self, x, c):
        return (x << c)&0xFFFFFFFF | (x >> (32-c)&0x7FFFFFFF >>(32-c))

    #Implementation of the given algorithm in the HW
    def helperMD5Alg(self, s, K, A, B, C, D, M):
        for i in range(64):
            if i <= 15:
                F = (B & C)|((~B) & D)
                F &= 0xFFFFFFFF
                g = i
            elif i <= 31:
                F = (D & B)|((~D) & C)
                F &= 0xFFFFFFFF
                g = (5*i + 1) % 16
            elif i <= 47:
                F = B ^ C ^ D
                F &= 0xFFFFFFFF
                g = (3*i + 5) % 16
            else:
                F = C ^ (B | ~D)
                F &= 0xFFFFFFFF
                g = (7*i) % 16
            dTemp = D
            D = C
            C = B
            B += self.helperLeftRotate((A + F + K[i] + M[g]),s[i])
            B &= 0xFFFFFFFF
            A = dTemp
        return A, B, C, D

    #Task 1
    def login(self,username, password):
        if username == "" or password == "":
            return False
        self.socket.send(b"LOGIN "+username.encode()+b"\n")
        response = self.socket.recv(1000)
        
        #checks if username is does not exist will return False
        if response == b'USER NOT FOUND\n':
            return False
        #extracting the challenge from the server response
        challenge = response.decode().split()[2]

        #generating the block and the Array of corresponding Values
        #using the helperBlockASCIIGenerate function
        block, M = self.helperBlockASCIIGenerate(password,challenge)
        
        #Initialises all the variables that will be used in the MD5
        #by using the helperInitialiseVars function
        s, K, a0, A, b0, B, c0, C, d0, D = self.helperInitialiseVars()

        #Performs the MD5 Algorithm as described in HW
        A, B, C, D = self.helperMD5Alg(s, K, A, B, C, D, M)
        a0 = (a0 + A) & 0xFFFFFFFF
        b0 = (b0 + B) & 0xFFFFFFFF
        c0 = (c0 + C) & 0xFFFFFFFF
        d0 = (d0 + D) & 0xFFFFFFFF
        
        #concatenates the values to get the messagedigest
        result = str(a0)+ str(b0) + str(c0) + str(d0)

        #Sends the message digest along with the username to be checked
        self.socket.send(b"LOGIN "+username.encode()+
                         " ".encode()+result.encode()+b"\n")
        
        #returns True if password is correct and False otherwise
        response = self.socket.recv(2000)
        return response[:len(b'WRONG PASSWORD!')] != b'WRONG PASSWORD!'

    #returns an array of all the users avilable by sending @users to server
    def getUsers(self):
        self.socket.send(b'@users')
        size = int(self.socket.recv(6).decode()[1:])
        response = ""
        counter = 0
        while size != len(response)+6:
            counter += 1
            response += self.socket.recv(size-6).decode()
        response = response.split("@")
        users = sorted(response[3:])
        return users

    #returns an array of all current friends
    def getFriends(self):
        self.socket.send(b'@friends')
        size = int(self.socket.recv(6).decode()[1:])
        response = self.socket.recv(size-6).decode().split("@")
        users = sorted(response[3:])
        return users

    #sends the server the command for friend request while also computing
    #the size of the command in bytes and concatenating to the start of the
    #the command
    def sendFriendRequest(self, friend):
        clientMessage = f'@request@friend@{friend}'
        clientMessage = ("@"+"0" * (5-(len(str(len(clientMessage)+6)))) +
                         str(len(clientMessage)+6)+clientMessage)
        self.socket.send(clientMessage.encode())
        size = int(self.socket.recv(6).decode()[1:])
        response = self.socket.recv(size-6).decode()
        return "ok" in response

    #sends the server the command for accepting a request while also computing
    #the size of the command in bytes and concatenating to the start of the
    #the command
    def acceptFriendRequest(self,friend):
        clientMessage = f'@accept@friend@{friend}'
        clientMessage = ("@"+"0" * (5-(len(str(len(clientMessage)+6)))) +
                         str(len(clientMessage)+6)+clientMessage)
        self.socket.send(clientMessage.encode())
        size = int(self.socket.recv(6).decode()[1:])
        response = self.socket.recv(size-6).decode() 
        return "ok" in response

    #sends the server the command for sending a message while also computing
    #the size of the command + message in bytes and concatenating to the start
    #of the command
    def sendMessage(self,friend, message):
        clientMessage = f'@sendmsg@{friend}@{message.replace("@","")}'
        clientMessage = ("@"+"0" * (5-(len(str(len(clientMessage)+6)))) +
                         str(len(clientMessage)+6)+clientMessage)
        self.socket.send(clientMessage.encode())
        size = int(self.socket.recv(6).decode()[1:])
        response = self.socket.recv(size-6).decode()
        return "ok" in response

    #sends the server the command for sending a file while also computing
    #the size of the command + file in bytes and concatenating to the start
    #of the command
    def sendFile(self,friend, filename):
        try:
            file = open(filename,"r")
        except:
            return False
        filecontent = file.read().replace("@","")
        file.close()
        clientMessage = f'@sendfile@{friend}@{filename}@{filecontent}'
        clientMessage = ("@"+"0" * (5-(len(str(len(clientMessage)+6)))) +
                         str(len(clientMessage)+6)+clientMessage)
        self.socket.send(clientMessage.encode())
        size = int(self.socket.recv(6).decode()[1:])
        response = self.socket.recv(size-6).decode() 
        return "ok" in response

    #returns array of pending requests by sending comman @users to server
    def getRequests(self):
        self.socket.send(b'@rxrqst')
        size = int(self.socket.recv(6).decode()[1:])
        response = self.socket.recv(size-6).decode().split("@")
        users = sorted(response[2:])
        return users

    #returns a tuple of arrays of messages and files by sending command
    #@rxmsg to the server
    def getMail(self):
        self.socket.send(b'@rxmsg')
        size = int(self.socket.recv(6).decode()[1:])
        response = self.socket.recv(size-6).decode().split("@")
        messages = []
        files = []
        counter = 2
        while counter < len(response) and response[counter] == "msg":
            messages.append((response[counter+1],response[counter+2]))
            counter += 3
        while counter < len(response) and response[counter] == "file":
            files.append((response[counter+1],response[counter+2]))
            try:
                file = open(response[counter+2],"r")
                file.close()
            except:
                file = open(response[counter+2],"w")
                file.write(response[counter+3])
                file.close()
            counter += 4
        return (messages, files)
