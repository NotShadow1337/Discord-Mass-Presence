import random, json, time, sys, threading, websocket

def presence(token, game, type, status):


    ws = websocket.WebSocket()
    ws.connect('wss://gateway.discord.gg/?v=6&encoding=json')

    hello = json.loads(ws.recv())

    heartbeat_interval = hello['d']['heartbeat_interval']

    if type == "Playing":
        gamejson = {
            "name": game,
            "type": 0
        }

    elif type == 'Streaming':
        gamejson = {
            "name": game,
            "type": 1,
            "url": "https://www.twitch.tv/ishowspeed" #change this
        }

    elif type == "Listening to":
        gamejson = {
            "name": game,
            "type": 2
        }

    elif type == "Watching":
        gamejson = {
            "name": game,
            "type": 3
        }

    auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": sys.platform,
                "$browser": "RTB",
                "$device": f"{sys.platform} Device"
            },
            "presence": {
                "game": gamejson,
                "status": status,
                "since": 0,
                "afk": False
            }
        },
        "s": None,
        "t": None
    }

    ws.send(json.dumps(auth))

    ack = {
        "op": 1,
        "d": None
    }

    print(f"Token: {token:<20} | Status: {status} | Type: {type}")

    while True:
        time.sleep(heartbeat_interval / 1000)
        try:
            ws.send(json.dumps(ack))
        except:
            break


def main():
    activity_type = ['Playing', 'Streaming', 'Watching', 'Listening to']
    games = ['Valorant', 'Minecraft', 'Roblox']
    status = ['online', 'dnd', 'idle', 'dnd', 'idle']
    for token in open("tokens.txt","r").readlines():
        threading.Thread(target=lambda : presence(token.strip(), random.choice(games), random.choice(activity_type), random.choice(status))).start()

main()