def partition(arr, low, high):
    """Lomuto partition: uses arr[high] as the pivot and returns its final index."""
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quicksort(arr, low=0, high=None):
    """Sorts arr in place in ascending order.

    Average time O(n log n), worst case O(n^2), extra space O(log n) on average.
    """
    if high is None:
        high = len(arr) - 1
    if low < high:
        p = partition(arr, low, high)
        quicksort(arr, low, p - 1)
        quicksort(arr, p + 1, high)
    return arr


if __name__ == "__main__":
    data = [38, 27, 43, 3, 9, 82, 10, 3, -5, 0]
    print(quicksort(data))
