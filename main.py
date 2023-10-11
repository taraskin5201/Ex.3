import threading
import queue

# Глобальний лок для доступу до черги та результатів
queue_lock = threading.Lock()
result_queue = queue.Queue()

def collatz_steps(n):
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

def calculate_steps(start, end):
    local_steps = 0
    for num in range(start, end + 1):
        steps = collatz_steps(num)
        local_steps += steps
    with queue_lock:
        result_queue.put(local_steps)

def worker():
    while True:
        start_end = task_queue.get()
        if start_end is None:
            break
        calculate_steps(*start_end)
        task_queue.task_done()

if __name__ == "__main__":
    N = 1000
    num_threads = 4

    # Створення черги завдань
    task_queue = queue.Queue()

    # Розподіл завдань між потоками
    step = N // num_threads
    for i in range(num_threads):
        start = i * step + 1
        end = (i + 1) * step if i != num_threads - 1 else N
        task_queue.put((start, end))

    # Створення та запуск потоків
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    # Чекаємо завершення потоків
    task_queue.join()

    # Завершення роботи потоків
    for _ in range(num_threads):
        task_queue.put(None)

    for thread in threads:
        thread.join()

    # Збираємо результати з черги та розраховуємо середню кількість кроків
    total_steps = 0
    while not result_queue.empty():
        total_steps += result_queue.get()

    average_steps = total_steps / N
    print(f"Середня кількість кроків для чисел від 1 до {N}: {average_steps}")
