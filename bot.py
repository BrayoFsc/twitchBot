import socket


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
