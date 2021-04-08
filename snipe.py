from datetime import datetime
import aiohttp
import asyncio


CHALLENGES_API = "https://api.mojang.com/user/security/challenges"
NAME_CHANGE_API = "https://api.minecraftservices.com/minecraft/profile/name/"


async def main():
    token = input("Token of account to snipe on: ")
    name = input("Name to snipe: ")
    print("It may be a good idea to subtract 1 from the seconds value of the availability time to account for the "
          "time for the authorization request, and because the script auto-retries if it fails")
    print("Format: 24-hour time hh:mm:ss taken directly from NameMC.")
    print("NOTE: DO NOT ZERO PAD. 00 SHOULD BECOME 0. 09 SHOULD BECOME 9")
    time = input("Time: ")
    print(f"[INFO] Waiting for IGN to become available at {time}")
    while True:
        now = datetime.now()
        if f"{now.hour}:{now.minute}:{now.second}" != time:
            continue
        else: break
    async for attempt in change_name(token, name):
        print(attempt)


async def change_name(token, name):
    header = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    print("[INFO] Requesting for security challenges to trust IP..")
    async with aiohttp.request("GET", CHALLENGES_API, headers=header) as _:
        pass  # nothing needs to be done with this data
    print("[INFO] Sent request for security challenges, IP should be trusted now")
    tries = 0
    while True:
        if tries >= 50: return
        tries += 1
        async with aiohttp.request("PUT", f"{NAME_CHANGE_API}{name}", headers=header) as response:
            if response.status == 200:
                print(f"[STATUS] Successfully changed name to {name}")
                return
            elif response.status == 400:
                print("[ERROR] Invalid name given, over 16 characters or contains non-ASCII characters")
            elif response.status == 403:
                print("[ERROR] Name given was unavailable")
            elif response.status == 401:
                print("[ERROR] Token given was invalid")
            elif response.status == 500:
                print("[ERROR] Mojang API timed out")
            yield await response.json()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
