import asyncio
import aiohttp

url = 'https://js-30-ular-default-rtdb.europe-west1.firebasedatabase.app/'

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:

            print("Status:", response.status)

            data = await response.json()
            return data



async def main():

    products = ['meals', 'product']
    task_list = []
    for p in products:
        task = asyncio.create_task(fetch_data(f'{url}{p}.json'))
        task_list.append(task)

    result = await asyncio.gather(*task_list)
    print(result)

asyncio.run(main())