import heapq

# Initialize and function to add element and remove elements in queue
class PriorityQueue:
def __init__(self, capacity):
    self.capacity = capacity
    self.queue = []
    self.counter = 0

# Maintain only the #of elements in queue as per capacity and remove the low priority item in queue when high priority comes
def enqueue(self, value, priority):
if len(self.queue) < self.capacity:
    heapq.heappush(self.queue, (priority, self.counter, value))
    self.counter += 1
else:
    min_priority, _, _ = self.queue[0]

if priority > min_priority:
heapq.heappop(self.queue)
heapq.heappush(self.queue, (priority, self.counter, value))
self.counter += 1

# Remove the high priority element in queue
def dequeue(self):
sorted_queue = sorted(self.queue, key=lambda x: x[0], reverse=True)
self.queue = sorted_queue
if self.queue:
_, _, value = heapq.heappop(self.queue)
return value
else:
return None
def print_queue(self):
final_sort = sorted(self.queue, key=lambda x: x[0], reverse=True)
for k in final_sort:
print(f"{k[2]} {k[0]}")
print('')

# Read the capacity of the queue
capacity = int(input())
priority_queue = PriorityQueue(capacity)

# Call enqueue / dequeue to add/remove elements in queue
while True:
try:
operation = input().split()
if operation[0] == "enqueue":
value, priority = int(operation[1]), int(operation[2])
priority_queue.enqueue(value, priority)
elif operation[0] == "dequeue":
priority_queue.dequeue()
except EOFError:
break

priority_queue.print_queue()