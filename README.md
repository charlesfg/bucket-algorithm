# Bucket Algorithm

This repository provides a Python implementation of the bucket algorithm for performance degradation detection, as described in the work of Avritzer et al.

## Introduction

The bucket algorithm is a lightweight and efficient method for detecting performance degradation in software systems. It works by comparing incoming performance metrics (e.g., response time, throughput) against a baseline and using a series of "buckets" to classify the system's state.

The main idea is to have a series of buckets, each with a certain depth. When a new metric arrives, it's compared to the baseline. If the metric is worse than the baseline plus a certain threshold (which increases with the number of filled buckets), a counter is incremented. If the metric is better, the counter is decremented. The number of filled buckets is determined by the value of the counter.

This allows the algorithm to be sensitive to small, continuous degradations, while being robust to occasional spikes.

## How it Works

The core of the algorithm is the `Bucket` class. Here's a breakdown of the key concepts:

*   **Baselines (`b_avg`, `b_std`):** The algorithm needs a baseline average and standard deviation of the performance metric in a healthy state.
*   **Buckets (`B`, `D`):** The algorithm uses `B` buckets, each with a depth of `D`.
*   **Counter:** The `counter` is incremented when a sample is "bad" and decremented when it's "good". A sample is considered "bad" if it's greater than `b_avg + p * b_std`, where `p` is the number of full buckets.
*   **Degradation Scale:** The `add_sample` method returns the current value of the `counter`, which represents the degradation scale. A value of 0 means the system is not in a degraded state. A value greater than 0 indicates the scale of the degradation.
*   **Inverse Logic:** The `inverse` parameter allows you to use the algorithm for metrics where a lower value is better (e.g., throughput).

## Usage

Here's a simple example of how to use the `Bucket` class:

```python
from bucket import Bucket

# Baseline average and standard deviation
b_avg = 100
b_std = 10

# Create a Bucket instance
bucket = Bucket(b_avg, b_std)

# Add some samples
samples = [105, 110, 115, 120, 125, 130, 100, 90]

for s in samples:
    degradation_scale = bucket.add_sample(s)
    print(f"Sample: {s}, Degradation Scale: {degradation_scale}")
```

## Parameters

The `Bucket` class constructor takes the following parameters:

*   `b_avg`: Baseline average.
*   `b_std`: Baseline standard deviation.
*   `D`: Depth of each bucket (Default: 30).
*   `B`: Number of buckets (Default: 1).
*   `abort`: If `True`, will raise an `OverflowError` exception when all buckets are full (Default: `False`).
*   `reset`: If `True`, will reset the counter after filling all buckets (empty all buckets) (Default: `False`).
*   `inverse`: If `True`, will invert the logic to interpret the metric (the lower the better). Useful for metrics like throughput (Default: `False`).

## Methods

### `add_sample(rt)`

Adds a new sample to the bucket.

*   **Parameter:** `rt` - The sample to be analyzed.
*   **Returns:** The degradation scale. 
    *   `0`: Not in a degraded state.
    *   `> 0`: Degraded scale.
    *   `> B * D`: System in alert.

### `update_baselines(b_avg, b_std)`

Updates the baseline average and standard deviation.

*   **Parameters:**
    *   `b_avg`: New baseline average.
    *   `b_std`: New baseline standard deviation.

## Example

The `generete_mock_data.py` script can be used to create a file with mock data for testing purposes. The `timing.py` script provides an example of how to use the `Bucket` class with a larger dataset.

To run the example:

1.  Generate mock data:
    ```bash
    python generete_mock_data.py > input_data.dat
    ```
2.  Run the timing script:
    ```bash
    python timing.py input_data.dat
    ```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
