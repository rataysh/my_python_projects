import websockets, asyncio, json, datetime


async def main():
    url = 'wss://stream.binance.com:9443/stream?streams=btcusdt@miniTicker'
    async with websockets.connect(url) as client:
        while True:
            data = json.loads(await client.recv())['data']
            now_time = datetime.datetime.fromtimestamp(int(data['E'])//1000) # # Тоже самое (просто запомнить на будующее).strftime('%Y-%m-%d %H:%M:%S')
            now_price = data['c']
            print(f'{now_time} --> {now_price}')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
