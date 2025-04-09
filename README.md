
#  Log Monitoring Application

This project is a solution to a coding challenge focused on parsing and monitoring a job log file. It identifies job durations and classifies them based on defined thresholds, generating both a terminal report and a saved log file.

---

##  Features

- Parse a CSV-based log file with job entries
- Match `START` and `END` events by job ID
- Calculate job durations in seconds
- Classify jobs:
  - `OK`: ≤ 5 minutes
  - `WARNING`: > 5 minutes
  - `ERROR`: > 10 minutes
  - `RUNNING`: missing END
- Output a clean report to console and file

---

##  Log Format

Each line of the log file must follow this structure:

```
HH:MM:SS,<job name>,<START|END>,<job PID>
```

### Example:
```
11:35:23,scheduled task 032, START,37980
11:35:56,scheduled task 032, END,37980
```

---

##  How It Works

1. **Parse** each row of the log file into a `LogEvent` object
2. **Track** events and assemble jobs using `track_jobs()`
3. **Analyze** jobs with `analyze_jobs()` to assign a status
4. **Report** results to both terminal and `report.log` file

---

##  Testing

Unit tests are available and cover:
- Job duration calculation
- Job classification logic
- Job tracking from events

Run tests with:

```bash
python -m unittest discover tests/
```

---

##  Project Structure

```
main_script.py       # Main logic and CLI entry
logs.log             # Input log file
report.log           # Output report file
tests/               # Unit tests
```

---

##  How to Run

1. Add your log entries to `logs.log`
2. Run the script:

```bash
python logger.py
```

3. Check:
   - Console output
   - Generated file: `report.log`

---

##  What Could Be Improved (If More Time)

- Convert to modular package layout (`utils/`, etc.)
- Improve error handling for malformed rows

---

##  Author

Cristian Marcu  
April 2025

---