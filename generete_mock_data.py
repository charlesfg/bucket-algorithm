import argparse
import random
import datetime
import statistics

def generate_data(num_entries, entries_to_print, malicious_machine_id):
    machines = list(range(0, 30))
    response_times = [random.randint(10, 5000) for _ in range(num_entries)]
    avg_response_time = statistics.mean(response_times)
    stdev_response_time = statistics.stdev(response_times)
    print(f"{avg_response_time},{stdev_response_time}")

    timestamps = [
        (datetime.datetime.now() - datetime.timedelta(minutes=random.randint(1, 60*24))).isoformat()
        for _ in range(num_entries)
    ]

    for i in range(entries_to_print):
        machine_id = random.choice(machines)
        response_time = random.choice(response_times)
        timestamp = timestamps[i % len(timestamps)]

        if machine_id == malicious_machine_id:
            degradation_factor = random.uniform(2.05, 5.25)
            response_time *= degradation_factor

        print(f"{machine_id},{int(response_time)},{timestamp}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate mock data for a hypothetical web services cluster.")
    parser.add_argument("num_entries", type=int, help="Number of entries to generate.")
    parser.add_argument("entries_to_print", type=int, help="Number of entries to print.")
    parser.add_argument("malicious_machine_id", type=int, help="Machine ID with malicious behavior.")
    args = parser.parse_args()

    generate_data(args.num_entries, args.entries_to_print, args.malicious_machine_id)
