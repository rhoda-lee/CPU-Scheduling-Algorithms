from collections import defaultdict
from memory import MemoryManager
from io_management import IORequest, Device

def unified_simulation(io_requests, reference_sequence, frames):
    # Initialize subsystems
    devices = defaultdict(Device)
    memory_manager = MemoryManager(frames)
    
    for request in io_requests:
        if request.device_type not in devices:
            devices[request.device_type] = Device(request.device_type)
        devices[request.device_type].add_request(request)
    
    total_requests = len(io_requests)  # Track total number of requests
    time = 0  # Track overall system time
    
    # Process requests for each device
    for device in devices.values():
        device.process_next_request()
        for request_id, start_time, end_time in device.timeline:
            # Simulate memory accesses during I/O processing
            memory_page = int(request_id[1:])  # Example: Derive page from Request ID
            memory_manager.access_page(memory_page)
    
    # Calculate overall metrics
    total_throughput = sum(len(device.timeline) for device in devices.values())
    avg_response_time = sum((end - start for device in devices.values() for _, start, end in device.timeline)) / total_requests
    total_busy_time = sum(device.total_busy_time for device in devices.values())
    total_time = max((end for device in devices.values() for _, _, end in device.timeline), default=0)
    overall_utilization = (total_busy_time / total_time) * 100 if total_time > 0 else 0
    
    memory_metrics = memory_manager.calculate_metrics()
    
    # Output performance metrics
    print("\nUnified Subsystem Metrics:")
    print(f"Total Throughput: {total_throughput} requests")
    print(f"Average Response Time: {avg_response_time:.2f} ms")
    print(f"Overall Resource Utilization: {overall_utilization:.2f}%")
    print(f"Memory Metrics:")
    print(f"  Total Page Faults: {memory_metrics['Page Faults']}")
    print(f"  Hit Ratio: {memory_metrics['Hit Ratio']:.2f}")
    print(f"  Average Memory Access Time: {memory_metrics['Average Memory Access Time']:.2f} ms")

    # Print memory replacement timeline for visualization
    print("\nMemory Replacement Timeline:")
    for step, state in enumerate(memory_manager.timeline):
        print(f"Step {step + 1}: {state}")

# Example Usage
unified_requests = [
    IORequest("R1", "Disk", 0, 20),
    IORequest("R2", "Printer", 10, 25),
    IORequest("R3", "Printer", 5, 15)
]
unified_reference_sequence = [2, 3, 1, 5, 2, 4, 1, 3, 5, 2]
unified_simulation(unified_requests, unified_reference_sequence, 3)
