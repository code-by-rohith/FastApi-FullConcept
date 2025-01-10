import time
import asyncio

# An asynchronous function simulating a task with a delay
async def main(i):
    print("task 1")
    await asyncio.sleep(5)  # Simulate delay (I/O operation or computation)
    print("task 2")

# Another async function that calls 'main'
async def main_2():
    print("starting process")
    await main(5)  # Wait for 'main' to complete
    print("end process")

# A simple async function that prints a message
async def data():
    await asyncio.sleep(2)
    print("hi")

async def mai():
    print("no returns")
# Use 'asyncio.run()' to run the asynchronous tasks concurrently
async def run():
    await asyncio.gather(main_2(), data(),mai())  # Running both tasks concurrently

# This line runs the event loop and executes the 'run' function
asyncio.run(run())
