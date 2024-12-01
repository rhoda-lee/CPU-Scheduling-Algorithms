'''Model of tasks class'''

class Tasks:
    def __init__(self, task_id, arrival_time, burst_time, priority):
        self.task_id = task_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.waiting_time = 0
        self.turnaround_time = 0


