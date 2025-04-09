import csv
from datetime import datetime


class LogEvent:

    def __init__(self, timestamp, name, event, id):
        self.id = id
        self.name = name
        self.event = event.strip()
        self.time = datetime.strptime(timestamp, "%H:%M:%S").time() # parsed timestamp

def parse_log(file_path):

    events = []
    with open(file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            events.append(LogEvent(*row))   # each row becomes a LogEvent
    return events

def main():

    file_path = "logs.log"  
    events = parse_log(file_path)  # parse events
    jobs = track_jobs(events)      # build Job objects
    results = analyze_jobs(jobs)   # classify jobs by duration
    print_report(results)          # print and save report


if __name__ == "__main__":

    main()