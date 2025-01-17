from queue import LifoQueue

stack = LifoQueue(maxsize=3)

stack.put(1)
stack.put(2)
stack.put(3)

print(stack.queue)
print(stack.full())

print(stack.get(2))

print(stack.empty())