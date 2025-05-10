import asyncio

from zoey import Core
        
async def main():
    # How to use
    core = Core()
    print(await core.generate_response(prompt="Kamu cantik banget :)"))
    await core.close_session()

if __name__ == "__main__":
    asyncio.run(main())