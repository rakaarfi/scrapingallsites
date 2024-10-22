import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup as bs

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

async def get_requests(url, session:aiohttp.ClientSession):
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                response_text = response.text()
                return await response_text
            else:
                print(f"Failed to get response from {url}, status code: {response.status}")
                return None
    except aiohttp.ClientError as e:
        print(f"An error occured: {e}")
        return None

# async def main():
#     url = 'https://news.detik.com/indeks/'

#     async with aiohttp.ClientSession() as session:
#         response_text = await get_requests(url, session)
#         print(response_text)

# if __name__ == "__main__":
#     asyncio.run(main())