import csv
from datetime import datetime


class LogEvent:

    def __init__(self, timestamp, name, event, id):
        self.id = id
        self.name = name
        self.event = event.strip()
        self.time = datetime.strptime(timestamp, "%H:%M:%S").time() # parsed timestamp


class Job:

    def __init__(self, id):
        self.id = id
        self.name = None
        self.start_time = None
        self.end_time = None

    def duration(self):

        if self.start_time and self.end_time:
            start_time_seconds = self.start_time.hour * 3600 + self.start_time.minute * 60 + self.start_time.second
            end_time_seconds = self.end_time.hour * 3600 + self.end_time.minute * 60 + self.end_time.second
            return end_time_seconds - start_time_seconds
        return None # return None if job is incomplete

def parse_log(file_path):

    events = []
    with open(file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            events.append(LogEvent(*row))   # each row becomes a LogEvent
    return events

def track_jobs(events):

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

def main():

    file_path = "logs.log"  
    events = parse_log(file_path)  # parse events
    jobs = track_jobs(events)      # build Job objects
    results = analyze_jobs(jobs)   # classify jobs by duration
    print_report(results)          # print and save report


if __name__ == "__main__":

    main()