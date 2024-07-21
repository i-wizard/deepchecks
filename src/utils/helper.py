from typing import List
import statistics


def has_outlier(value: int, data: List[int]) -> bool:
    """
    Determine if a given value is an outlier in the provided data list.
    Args:
        value (int): The value to check for being an outlier.
        data (list): A list of numeric values to compute the mean and standard deviation.

    Returns:
        bool: True if the value is considered an outlier, False otherwise.
    """
    if len(data) == 0:
        return False
    # Copy the data to avoid modifying the original list
    data = data.copy()
    data.append(value)

    # Compute mean and standard deviation
    mean = statistics.mean(data)
    stdev = statistics.stdev(data) if len(data) > 1 else 0

    # Check if the value is an outlier
    return abs(value - mean) > 2 * stdev
