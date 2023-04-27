import argparse
import sys
from bucket import Bucket


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse output from the mock data generator.")
    parser.add_argument("-f", "--file", type=str, required=False, help="File containing the input data. If not provided, reads from stdin.")
    parser.add_argument('-b', metavar='B', type=int, default=2,  help='Number of buckets')
    parser.add_argument('-d', metavar='D', type=int, default=15, help='Depth of each bucket')
    args = parser.parse_args()

    # We assume 30 machines, each one with one bucket
    if args.file:
        with open(args.file, "r") as f:
            data = f.readlines()
    else:
        data = sys.stdin.readlines()

    avg_response_time, stdev_response_time = map(float, data[0].strip().split(","))
    print(f"Average Response Time: {avg_response_time}")
    print(f"Standard Deviation of Response Time: {stdev_response_time}")

   
    # We assume 30 machines
    machine_buckets = [Bucket(avg_response_time,stdev_response_time,args.b,args.d,True,True) for x in list(range(0,30))] 

    for line in data[1:]:
        machine_id, response_time, timestamp = line.strip().split(",")
        try:

            machine_buckets[int(machine_id)].add_sample(int(response_time))
        except OverflowError:
            print(f"Machine id {machine_id} alert on {timestamp}")
