import socket
import pdb


SERVER = "irc.twitch.tv"
PORT = 6667


'''
create a auth.txt file containing:

OWNER = |Your twitch account|
BOT = |Bot's name|
CHANNEL = |Channel Name (lower case)|
AUTH = |Twitch OAUTH Code| (get yours here https://twitchapps.com/tmi/)
'''

JOIN = {}
with open("auth.txt") as f:
    for line in f:
        (key, val) = line.split('=')
        JOIN[key] = val.rstrip('\n')

OWNER = JOIN["OWNER"]
BOT = JOIN["BOT"]
CHANNEL = JOIN["CHANNEL"]
AUTH = JOIN["AUTH"]

twitch = socket.socket()
twitch.connect((SERVER, PORT))
twitch.send(("PASS " + AUTH + "\n" + "NICK "+BOT + "\n" +
             "JOIN #" + CHANNEL + "\n").encode())

user = ""
message = ""


def getusr(line):
    fields = line.count(":")
    colons = line.split(":")
    user = colons[fields-1].split("!")[0]
    return user


def getmsg(line, user):
    message = line.split("PRIVMSG #" + user + ":")[1]
    return message


def sendmsg(twitch, msg):
    msginit = "PRIVMSG #" + CHANNEL + " :" + msg + "\n"
    twitch.send((msginit).encode())


def chatcontrol():
    global message
    global user

    while True:
        try:
            chatdata = twitch.recv(2048).decode()
        except:
            chatdata = ""
        for line in data.split("\r\n"):
            if line == "":
                continue
            if "PING :tmi.twitch.tv" in line:
                print(line)
                msg = "PONG :tmi.twitch.tx\r\n".encode()
                twitch.send(msg)
                print(msg)
                continue
            else:
            try:
                user = getusr(line)
                message = getmsg(line, user)
                print(user + ": " + message)
                # here you can add all the things you want,
                #  like sound request or alert sounds
                if "sound request custom reward id" in line:
                    sendmsg(twitch, "!sr " + message)
                elif "custom reward id" in line:
                    sendmsg(twitch, "!reward")

            except Exception:
                pass


def joinchat():
    loading = True
    while loading:
        data = twitch.recv(2048).decode()
        for line in data.split('\n'):
            print(line)
            if("End of /NAMES list" in line):
                print(BOT + " has joined " + CHANNEL + "'s chat")
                sendmsg(twitch, BOT + " has joined the chat")
                loading = False


joinchat()
chatcontrol()
