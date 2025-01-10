import time
import asyncio

# A simulated task (e.g., network request, file I/O)
def sync_task(task_id):
    print(f"Sync Task {task_id} started...")
    time.sleep(2)  # Simulates a blocking operation
    print(f"Sync Task {task_id} completed.")

async def async_task(task_id):
    print(f"Async Task {task_id} started...")
    await asyncio.sleep(2)  # Simulates a non-blocking operation
    print(f"Async Task {task_id} completed.")

# Synchronous version
def sync_example():
    start_time = time.time()
    for i in range(5):  # Simulate 5 tasks
        sync_task(i)
    end_time = time.time()
    print(f"Synchronous execution time: {end_time - start_time:.2f} seconds\n")

# Asynchronous version
async def async_example():
    start_time = time.time()
    tasks = [async_task(i) for i in range(50)]  # Simulate 5 tasks
    await asyncio.gather(*tasks)
    end_time = time.time()
    print(f"Asynchronous execution time: {end_time - start_time:.2f} seconds\n")

# Run the comparison
# print("Running Sync Example...")
# sync_example()

print("Running Async Example...")
asyncio.run(async_example())
