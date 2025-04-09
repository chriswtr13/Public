import csv
from datetime import datetime

class LogEvent:

    '''Represents a single event from the log file (e.g., a START or END entry)'''

    def __init__(self, timestamp, name, event, id):
        self.id = id
        self.name = name
        self.event = event.strip()
        self.time = datetime.strptime(timestamp, "%H:%M:%S").time() # parsed timestamp

class Job:

    '''Represents a job with name, start and end time (matched by PID)'''

    def __init__(self, id):
        self.id = id
        self.name = None
        self.start_time = None
        self.end_time = None

    def duration(self):

        '''Calculates job duration in seconds, if both times are available'''

        if self.start_time and self.end_time:
            start_time_seconds = self.start_time.hour * 3600 + self.start_time.minute * 60 + self.start_time.second
            end_time_seconds = self.end_time.hour * 3600 + self.end_time.minute * 60 + self.end_time.second
            return end_time_seconds - start_time_seconds
        return None # return None if job is incomplete


def parse_log(file_path):

    '''Parses the CSV log file into a list of LogEvent objects'''

    events = []
    with open(file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            events.append(LogEvent(*row))   # each row becomes a LogEvent
    return events

def track_jobs(events):

    '''Groups LogEvents by PID and builds Job objects with start/end times'''

    jobs = {}
    for event in events:
        if event.id not in jobs:
            jobs[event.id] = Job(event.id) # create new job if not seen before
        job = jobs[event.id]
        if not job.name:
            job.name = event.name
        if event.event == "START":
            job.start_time = event.time
        elif event.event == "END":
            job.end_time = event.time
    return jobs

def analyze_jobs(jobs):

    '''Analyzes job durations and assigns a status: OK, WARNING, ERROR, or RUNNING'''

    results = []
    for job in jobs.values():
        duration = job.duration()
        if duration is None:    # handle jobs that haven't finished
            results.append((job.id, None, "RUNNING"))
            continue
        if duration > 600:      # apply thresholds: 5 min = warning, 10 min = error
            results.append((job.id, duration, "ERROR"))
        elif duration > 300:
            results.append((job.id, duration, "WARNING"))
        else:
            results.append((job.id, duration, "OK"))
    return results

def print_report(results, output_file="report.log"):

    '''Outputs a report both to the console and to a file'''

    lines = []
    for pid, duration, status in results:       # format output depending on job status
        if status == "RUNNING":
            line = (f"PID: {pid} | Duration:         | INCOMPLETE (no END)")
        elif status == "OK":
            line = (f"PID: {pid} | Duration: {duration:.2f}s")
        else:
            line = (f"PID: {pid} | Duration: {duration:.2f}s | {status}")
        print(line)
        lines.append(line)

    with open(output_file, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    

def main():
    
    '''Orchestrates the flow: parse → track → analyze → report'''

    file_path = "logs.log"  
    events = parse_log(file_path)  # parse events
    jobs = track_jobs(events)      # build Job objects
    results = analyze_jobs(jobs)   # classify jobs by duration
    print_report(results)          # print and save report


if __name__ == "__main__":

    '''Ensures script only runs when executed directly'''

    main()