import threading

# Глобальний лок для доступу до середнього значення кроків
average_steps_lock = threading.Lock()

# Глобальна змінна для зберігання загальної кількості кроків
total_steps = 0

def collatz_steps(n):
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

def calculate_average_steps(start, end):
    global total_steps
    for num in range(start, end + 1):
        steps = collatz_steps(num)
        with average_steps_lock:
            total_steps += steps

if __name__ == "__main__":
    N = 1000  # Замініть це значення на бажану кількість чисел від 1 до N
    num_threads = 4  # Замініть це значення на бажану кількість потоків

    # Розподіл роботи між потоками
    thread_list = []
    step = N // num_threads
    for i in range(num_threads):
        start = i * step + 1
        end = (i + 1) * step if i != num_threads - 1 else N
        thread = threading.Thread(target=calculate_average_steps, args=(start, end))
        thread_list.append(thread)
        thread.start()

    # Очікування завершення всіх потоків
    for thread in thread_list:
        thread.join()

    # Розрахунок середньої кількості кроків
    average_steps = total_steps / N
    print(f"Середня кількість кроків для чисел від 1 до {N}: {average_steps}")