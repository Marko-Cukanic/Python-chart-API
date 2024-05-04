import asyncio
import pandas as pd
from lightweight_charts import Chart

from ib_insync import *
import nest_asyncio
nest_asyncio.apply()

from streaming import demo, connect_to_stream  #


def get_data(symbol, timeframe):
    displayHeartbeat = True  # Set this to True to display heartbeats
    streaming_data = demo(displayHeartbeat)

    # Convert the streaming data to a pandas DataFrame
    df = pd.DataFrame(streaming_data)

    # Filter the DataFrame based on the symbol and timeframe
    df = df[df['instrument'] == symbol]
    # ... (add additional filtering based on timeframe if needed)

    return df

class API:
    def __init__(self):
        self.chart = None

    async def on_search(self, symbol):  # Called when the user searches.
        timeframe = self.chart.topbar['timeframe'].value
        data = get_data(symbol, timeframe)

        self.chart.set(data)  # sets data for the Chart or SubChart in question.
        self.chart.topbar['symbol'].set(symbol)

    async def on_timeframe(self):  # Called when the user changes the timeframe.
        timeframe = self.chart.topbar['timeframe'].value
        symbol = self.chart.topbar['symbol'].value
        data = get_data(symbol, timeframe)

        self.chart.set(data)

    
async def main():
    api = API()
    chart = Chart(api=api, topbar=True, searchbox=True)
    
    symbol = 'AAPL'
    timeframe = '15 mins'
    df = get_data(symbol, timeframe)

    chart.topbar.textbox('symbol', symbol)
    chart.topbar.switcher('timeframe', api.on_timeframe, '15 mins', '1 hour', '1 day', default='15 mins')
    
    chart.set(df)

    await chart.show_async(block=True)


if __name__ == '__main__':
    asyncio.run(main())