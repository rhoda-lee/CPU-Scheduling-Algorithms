import heapq
from collections import defaultdict


class IORequest:
    def __init__(self, request_id, device_type, arrival_time, duration):
        self.request_id = request_id
        self.device_type = device_type
        self.arrival_time = arrival_time
        self.duration = duration

    def __lt__(self, other):
        return (self.arrival_time, self.duration) < (other.arrival_time, other.duration)


class Device:
    def __init__(self, device_type):
        self.device_type = device_type
        self.queue = []
        self.timeline = []
        self.current_time = 0
        self.total_busy_time = 0
        self.idle_time = 0  # New attribute to track idle time

    def add_request(self, io_request):
        heapq.heappush(self.queue, io_request)

    def process_next_request(self):
        if not self.queue:
            return None  # Device is idle
        
        current_request = heapq.heappop(self.queue)
        start_time = max(self.current_time, current_request.arrival_time)
        finish_time = start_time + current_request.duration
        self.timeline.append((current_request.request_id, start_time, finish_time))
        self.total_busy_time += current_request.duration
        self.current_time = finish_time
        self.idle_time = 0  # Reset idle time after processing
        return finish_time

    def increment_idle_time(self, increment):
        self.idle_time += increment


def simulate_io_management(io_requests):
    # Create device queues
    devices = defaultdict(Device)
    for request in io_requests:
        if request.device_type not in devices:
            devices[request.device_type] = Device(request.device_type)
        devices[request.device_type].add_request(request)

    time = 0
    while any(device.queue or device.idle_time < 10 for device in devices.values()):
        for device in devices.values():
            if device.queue:
                finish_time = device.process_next_request()
                if finish_time:
                    time = max(time, finish_time)
            else:
                device.increment_idle_time(1)

        # Dynamic queue management
        for device in devices.values():
            if device.idle_time > 10:  # Device is idle for more than 10ms
                # Find a request to steal from other devices
                longest_waiting_request = None
                donor_device = None
                for other_device in devices.values():
                    if other_device is not device and other_device.queue:
                        # Find the request with the longest wait time
                        waiting_request = other_device.queue[0]
                        if not longest_waiting_request or waiting_request.arrival_time < longest_waiting_request.arrival_time:
                            longest_waiting_request = waiting_request
                            donor_device = other_device
                
                if longest_waiting_request:
                    # Steal the request
                    donor_device.queue.remove(longest_waiting_request)
                    heapq.heapify(donor_device.queue)  # Re-heapify the donor device queue
                    device.add_request(longest_waiting_request)
                    device.idle_time = 0  # Reset idle time after stealing

    # Output metrics
    for device_type, device in devices.items():
        print(f"\nDevice: {device_type}")
        print("Timeline:", device.timeline)
        total_time = max((end for _, _, end in device.timeline), default=0)
        avg_waiting_time = sum(
            start - next(req.arrival_time for req in io_requests if req.request_id == request_id)
            for request_id, start, _ in device.timeline
        ) / len(device.timeline)
        avg_turnaround_time = sum(
            end - next(req.arrival_time for req in io_requests if req.request_id == request_id)
            for request_id, _, end in device.timeline
        ) / len(device.timeline)
        utilization = (device.total_busy_time / total_time) * 100 if total_time > 0 else 0
        print(f"Average Waiting Time: {avg_waiting_time:.2f}")
        print(f"Average Turnaround Time: {avg_turnaround_time:.2f}")
        print(f"Device Utilization: {utilization:.2f}%")


# Example Usage
requests = [
    IORequest("R1", "Disk", 0, 20),
    IORequest("R2", "Printer", 10, 25),
    IORequest("R3", "Printer", 5, 15),
    IORequest("R4", "Disk", 30, 10)
]
simulate_io_management(requests)
