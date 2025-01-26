def sliding_window(arr: list[float], window_size: int, start: int=0):
    """
    Iterate all winows of a given size for the array.

    Args:
        arr: The data array to iterate through
        windows_size: The static size of the window to use.
        start: Optional parameter to start the window other than at the
            beginning of the array.
    """
    for idx in range(len(arr) - window_size + 1):
        yield arr[idx: idx + window_size]


def is_cycle(arr: list[float]) -> bool:
    """
    Detect a cycle of alternating data points.

    Args:
        arr: The data array to analyze

    Returns:
        Whether or not the dataset follows a cycle pattern.
    """
    # Assuming a minimum of four points are needed to establish a cyclic pattern
    if len(arr) < 4:
        return False, []

    is_increasing = False if arr[1] - arr[0] < 0 else True

    for idx in range(1, len(arr) - 1):
        next_step = False if arr[idx+1] - arr[idx] < 0 else True

        if is_increasing == next_step:
            return False

        is_increasing = next_step

    return True
