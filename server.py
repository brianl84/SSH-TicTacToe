import asyncio
import asyncssh

class Server(asyncssh.SSHServer):
    def begin_auth(self, username):
        return False

players = {}
waiting = None

async def read_line(process):
    while True:
        try:
            return await process.stdin.readline()
        except asyncssh.TerminalSizeChanged:
            continue
        except Exception:
            return ""

class Player:
    def __init__(self, name, proc):
        self.name = name
        self.proc = proc
        self.game = None
        self.mark = ""
class Game:
    def __init__(self, px, po):
        self.px = px
        self.po = po
        self.board = [""] * 9
        self.turn = "X"

def send(p, text):
    try:
        p.proc.stdout.write(text)
    except Exception:
        pass

def matchmake(p):
    global waiting
    if waiting is None or waiting is p:
        waiting = p
        send(p, "Waiting for another player...\r\n")
        return
    other = waiting
    waiting = None
    g = Game(other, p)
    other.game = g
    other.mark = "X"
    p.game = g
    p.mark = "O"
    send(other, "You are matched with " + p.name + ", you are X\r\n")
    send(p, "You are matched with " + other.name + ", you are O\r\n")

def leave(p):
    global waiting
    if waiting is p:
        waiting = None
    players.pop(p.name, None)

def on_line(p, line):
    send(p, "You said " + line + "\r\n")

async def handle(process):
    process.stdout.write("Your Name:")
    line = await read_line(process)
    name = "".join(c for c in line if c.isprintable() and c != ",").strip()[:12]
    if name == "" or name in players:
        process.stdout.write("Name empty or taken\r\n")
        process.exit(0)
        return
    p = Player(name, process)
    players[name] = p
    matchmake(p)
    try:
        while True:
            raw = await read_line (process)
            if raw == "":
                break
            if on_line(p, raw_strip()) is False:
                break
    finally:
        leave(p)
    process.exit(0)
    
async def main():
    await asyncssh.create_server(Server, "", 2222,
        server_host_keys=["host_key"], process_factory=handle)
    print("listening on 2222")
    await asyncio.Future()

asyncio.run(main())