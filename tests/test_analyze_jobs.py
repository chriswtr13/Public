import unittest
from datetime import time
from logger import Job, analyze_jobs

class TestAnalyzeJobs(unittest.TestCase):

    def test_error_status(self):    # job duration is over 10 min → ERROR
        job = Job("err1")
        job.start_time = time(10, 0, 0)
        job.end_time = time(10, 15, 0)
        results = analyze_jobs({"err1": job})
        self.assertEqual(results[0][2], "ERROR")

    def test_warning_status(self):  # job duration is over 5 min but under 10 → WARNING
        job = Job("warn1")
        job.start_time = time(10, 0, 0)
        job.end_time = time(10, 6, 0)
        results = analyze_jobs({"warn1": job})
        self.assertEqual(results[0][2], "WARNING")

    def test_ok_status(self):       # job duration under 5 min → OK
        job = Job("ok1")
        job.start_time = time(10, 0, 0)
        job.end_time = time(10, 4, 0)
        results = analyze_jobs({"ok1": job})
        self.assertEqual(results[0][2], "OK")

    def test_running_status(self):  # job has no END → should be marked as RUNNING
        job = Job("run1")
        job.start_time = time(10, 0, 0)
        # no end_time
        results = analyze_jobs({"run1": job})
        self.assertEqual(results[0][2], "RUNNING")

if __name__ == "__main__":
    unittest.main()
