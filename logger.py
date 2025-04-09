def main():

    file_path = "logs.log"  
    events = parse_log(file_path)  # parse events
    jobs = track_jobs(events)      # build Job objects
    results = analyze_jobs(jobs)   # classify jobs by duration
    print_report(results)          # print and save report


if __name__ == "__main__":

    main()