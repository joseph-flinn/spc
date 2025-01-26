def sliding_window(arr, window_size, start=0):
    for idx in range(len(arr) - window_size + 1):
        yield arr[idx: idx + window_size]


def is_cycle(arr):
    # A minimum of four points are needed to establish a cyclic pattern
    if len(arr) < 4:
        return False, []

    is_increasing = False if arr[1] - arr[0] < 0 else True
    
    for idx in range(1, len(arr) - 1):
        next_step = False if arr[idx+1] - arr[idx] < 0 else True
        
        if is_increasing == next_step:
            return False

        is_increasing = next_step
        
    return True