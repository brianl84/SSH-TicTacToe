import asyncio
import asyncssh

class Server(asyncssh.SSHServer):
    def begin_auth(self, username):
        return False

players = {}

async def read_line(process):
    while True:
        try:
            return await process.stdin.readline()
        except asyncssh.TerminalSizeChanged:
            continue
        except Exception:
            return ""

async def handle(process):
    process.stdout.write("Your Name:")
    line = await read_line(process)
    name = "".join(c for c in line if c.isprintable() and c != ",").strip()[:12]
    if name == "" or name in players:
        process.stdout.write("Name empty or taken\r\n")
        process.exit(0)
        return
    players[name] = process
    process.stdout.write("Hi " + name + ", online: " + ", ".join(players) + "\r\n")
    while True:
        if await read_line(process) == "":
            break
    del players[name]
    process.exit(0)
    
async def main():
    await asyncssh.create_server(Server, "", 2222,
        server_host_keys=["host_key"], process_factory=handle)
    print("listening on 2222")
    await asyncio.Future()

asyncio.run(main())