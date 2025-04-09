import unittest
from logger import LogEvent, track_jobs

class TestTrackJobs(unittest.TestCase):

    def test_track_start_and_end(self):     # verify that a job is correctly created and times assigned
        events = [
            LogEvent("10:00:00", "Task A", "START", "100"),
            LogEvent("10:05:00", "Task A", "END", "100")
        ]
        jobs = track_jobs(events)
        job = jobs["100"]
        self.assertEqual(job.start_time.hour, 10)
        self.assertEqual(job.end_time.minute, 5)

    def test_multiple_jobs(self):           # ensure multiple jobs are handled independently
        events = [
            LogEvent("09:00:00", "Task X", "START", "111"),
            LogEvent("09:02:00", "Task X", "END", "111"),
            LogEvent("10:00:00", "Task Y", "START", "222")
        ]
        jobs = track_jobs(events)
        self.assertEqual(len(jobs), 2)
        self.assertIsNotNone(jobs["111"].end_time)
        self.assertIsNone(jobs["222"].end_time)

if __name__ == "__main__":
    unittest.main()