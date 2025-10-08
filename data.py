import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy

# ======================================================
# 🔢 1. RASTGELE VERİ OLUŞTURMA
# ======================================================
data = list(range(1, 100))
random.shuffle(data)

# ======================================================
# ⚙️ 2. SIRALAMA ALGORİTMALARI (GENERATOR OLARAK)
# ======================================================
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            yield arr
        arr[j + 1] = key
        yield arr

def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr

def merge_sort(arr, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    if left >= right:
        return
    mid = (left + right) // 2
    yield from merge_sort(arr, left, mid)
    yield from merge_sort(arr, mid + 1, right)
    yield from merge(arr, left, mid, right)
    yield arr

def merge(arr, left, mid, right):
    left_copy = arr[left:mid + 1]
    right_copy = arr[mid + 1:right + 1]
    i = j = 0
    for k in range(left, right + 1):
        if j >= len(right_copy) or (i < len(left_copy) and left_copy[i] <= right_copy[j]):
            arr[k] = left_copy[i]
            i += 1
        else:
            arr[k] = right_copy[j]
            j += 1
        yield arr

# ======================================================
# 🧩 3. ANİMASYON FONKSİYONU
# ======================================================
def visualize_sort(sort_name, sort_generator):
    fig, ax = plt.subplots()
    ax.set_title(f"{sort_name} Visualization", fontsize=14, color="lime")
    bar_rects = ax.bar(range(len(data)), data, align="edge", color="limegreen")
    ax.set_xlim(0, len(data))
    ax.set_ylim(0, int(max(data) * 1.1))
    text = ax.text(0.02, 0.95, "", transform=ax.transAxes, color="white", fontsize=12)

    iteration = [0]

    def update_fig(arr, rects, iteration):
        for rect, val in zip(rects, arr):
            rect.set_height(val)
        iteration[0] += 1
        text.set_text(f"Iterations: {iteration[0]}")
        return rects

    anim = animation.FuncAnimation(
        fig,
        func=update_fig,
        fargs=(bar_rects, iteration),
        frames=sort_generator,
        interval=10,
        repeat=False,
        blit=False
    )

    plt.style.use('dark_background')
    plt.show()

# ======================================================
# 🚀 4. ÇALIŞTIRMA MENÜSÜ
# ======================================================
algorithms = {
    "1": ("Bubble Sort", bubble_sort),
    "2": ("Insertion Sort", insertion_sort),
    "3": ("Selection Sort", selection_sort),
    "4": ("Merge Sort", merge_sort)
}

print("Sıralama Görselleştirici (by Mahmut Sibal)")
print("------------------------------------------")
for key, (name, _) in algorithms.items():
    print(f"{key}. {name}")

choice = input("Bir algoritma seç (1-4): ")

if choice in algorithms:
    name, func = algorithms[choice]
    arr_copy = copy.copy(data)
    generator = func(arr_copy)
    visualize_sort(name, generator)
else:
    print("Geçersiz seçim!")
