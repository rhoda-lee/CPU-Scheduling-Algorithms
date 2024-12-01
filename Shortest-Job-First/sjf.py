import heapq
from task import Tasks

class ShortestJob:
    def __init__(self, tasks):
        self.tasks = sorted(tasks, key=lambda p: p.arrival_time)
        self.time = 0
        self.gantt_chart = []
        self.ready_queue = []
        self.max_starvation_time = 0

    def simulate(self):
        i = 0
        while i < len(self.tasks) or self.ready_queue:
            while i < len(self.tasks) and self.tasks[i].arrival_time <= self.time:
                task = self.tasks[i]
                heapq.heappush(self.ready_queue, (task.burst_time, task.priority, task))
                i += 1

            if self.ready_queue:
                _, _, current_process = heapq.heappop(self.ready_queue)
                self.gantt_chart.append((self.time, self.time + current_process.burst_time, current_process.task_id))
                self.time += current_process.burst_time
                current_process.turnaround_time = self.time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                self.max_starvation_time = max(self.max_starvation_time, current_process.waiting_time)

                self.update_priorities()
            else:
                self.time += 1

        avg_waiting_time = sum(p.waiting_time for p in self.tasks) / len(self.tasks)
        avg_turnaround_time = sum(p.turnaround_time for p in self.tasks) / len(self.tasks)

        return self.gantt_chart, avg_waiting_time, avg_turnaround_time, self.max_starvation_time

    def update_priorities(self):
        for idx, (_, priority, task) in enumerate(self.ready_queue):
            waiting_time = self.time - task.arrival_time - task.burst_time
            task.priority += waiting_time // 10
            self.ready_queue[idx] = (task.burst_time, task.priority, task)
        heapq.heapify(self.ready_queue)

# Usage
tasks = [
    Tasks("P1", 0, 10, 1),
    Tasks("P2", 2, 5, 2),
    Tasks("P3", 4, 7, 3)
]
scheduler = ShortestJob(tasks)
result = scheduler.simulate()
print("Gantt Chart:", result[0])
print("Average Waiting Time:", result[1])
print("Average Turnaround Time:", result[2])
print("Maximum Starvation Time:", result[3])
