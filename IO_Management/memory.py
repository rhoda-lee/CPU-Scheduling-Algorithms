from collections import defaultdict

class MemoryManager:
    def __init__(self, frames):
        self.frames = frames
        self.memory = []
        self.page_faults = 0
        self.hit_count = 0
        self.access_history = []
        self.frequency = defaultdict(int)
        self.timeline = []  # To track memory state at each step
        self.total_access_time = 0  # To calculate average memory access time

    def access_page(self, page):
        self.total_access_time += 1  # Increment access time for each request
        if page in self.memory:
            self.hit_count += 1
        else:
            self.page_faults += 1
            if len(self.memory) < self.frames:
                self.memory.append(page)
            else:
                # Use LRU or MFU depending on workload
                if len(self.access_history) < 2 or self.access_history[-1] != self.access_history[-2]:
                    # LRU
                    lru_page = min(self.memory, key=lambda p: self.access_history[::-1].index(p))
                    self.memory.remove(lru_page)
                else:
                    # MFU
                    mfu_page = max(self.memory, key=lambda p: self.frequency[p])
                    self.memory.remove(mfu_page)
                self.memory.append(page)

        # Update access history and frequency
        self.access_history.append(page)
        self.frequency[page] += 1

        # Prefetching: Improved logic
        if len(self.access_history) > 1:
            most_frequent_page = max(self.frequency, key=self.frequency.get)
            if most_frequent_page not in self.memory and len(self.memory) < self.frames:
                self.memory.append(most_frequent_page)

        # Record memory state at this step
        self.timeline.append(list(self.memory))

    def calculate_metrics(self):
        hit_ratio = self.hit_count / (self.hit_count + self.page_faults)
        avg_access_time = self.total_access_time / (self.hit_count + self.page_faults)
        return {
            "Page Faults": self.page_faults,
            "Hit Ratio": hit_ratio,
            "Average Memory Access Time": avg_access_time
        }


def simulate_memory_management(reference_sequence, frames):
    manager = MemoryManager(frames)
    for page in reference_sequence:
        manager.access_page(page)

    # Display metrics
    metrics = manager.calculate_metrics()
    print(f"Total Page Faults: {metrics['Page Faults']}")
    print(f"Hit Ratio: {metrics['Hit Ratio']:.2f}")
    print(f"Average Memory Access Time: {metrics['Average Memory Access Time']:.2f} ms")

    # Display timeline
    print("\nPage Replacement Timeline:")
    for i, state in enumerate(manager.timeline):
        print(f"Step {i + 1}: {state}")


# Example Usage
reference_sequence = [2, 3, 1, 5, 2, 4, 1, 3, 5, 2]
frames = 3
simulate_memory_management(reference_sequence, frames)
