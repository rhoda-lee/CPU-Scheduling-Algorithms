from task import Tasks
from collections import deque
import heapq

'''Modeling the round Robin algorithm'''

class RoundRobin:
    def __init__(self, tasks):
        self.tasks = sorted(tasks, key = lambda p: p.arrival_time)
        self.time = 0
        self.time_quantum = 5
        self.gantt_chart = []
        self.ready_queue = deque()
        self.priority_queue = []
        self.busy_time = 0
        self.idle_time = 0


    # Method to add all tasks to the priority queue by arrival time
    def simulation(self):
        for task in self.tasks:
            heapq.heappush(self.priority_queue, (task.arrival_time, task))

        # Main loop of the simulation
        while self.priority_queue or self.ready_queue:
            while self.priority_queue and self.priority_queue[0][0] <= self.time:
                _, task = heapq.heappop(self.priority_queue)
                self.ready_queue.append(task)


            if self.ready_queue:
                current_task = self.ready_queue.popleft()
                execution_time = min(current_task.remaining_time, self.time_quantum)
                self.gantt_chart.append((self.time, self.time + execution_time, current_task.task_id))
                self.time += execution_time
                current_task.remaining_time -= execution_time
                self.busy_time += execution_time

                for task in self.ready_queue:
                    task.waiting_time += execution_time

                if current_task.remaining_time > 0:
                    self.ready_queue.append(current_task)
                else:
                    current_task.turnaround_time = self.time - current_task.arrival_time

                self.adjust_quantum()
            else:
                self.idle_time += 1
                self.time += 1

        total_waiting_time = sum(p.waiting_time for p in self.tasks)
        total_turnaround_time = sum(p.turnaround_time for p in self.tasks)
        cpu_utilization = (self.busy_time / (self.busy_time + self.idle_time)) * 100

        return self.gantt_chart, total_waiting_time, total_turnaround_time, cpu_utilization

    def adjust_quantum(self):
        remaining_burst_times = [p.remaining_time for p in self.ready_queue]
        if remaining_burst_times:
            self.time_quantum = max(1, sum(remaining_burst_times) // len(remaining_burst_times))


'''Usage'''
tasks = [
    Tasks("P1", 0, 10, 1),
    Tasks("P2", 2, 5, 2),
    Tasks("P3", 4, 7, 3)
]
scheduler = RoundRobin(tasks)
result = scheduler.simulation()
print("Gantt Chart:", result[0])
print("Total Waiting Time:", result[1])
print("Total Turnaround Time:", result[2])
print("CPU Utilization:", result[3], "%")