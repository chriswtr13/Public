import unittest
from datetime import time
from logger import Job

class TestJob(unittest.TestCase):

    def test_duration_normal_case(self):    # test a complete job duration of exactly 10 minutes
        job = Job(id="001")
        job.start_time = time(10, 0, 0)
        job.end_time = time(10, 10, 0)
        self.assertEqual(job.duration(), 600)

    def test_duration_incomplete(self):     # test case where the job is incomplete (no end_time)
        job = Job(id="002")
        job.start_time = time(10, 0, 0)
        # No end_time
        self.assertIsNone(job.duration())

if __name__ == "__main__":
    unittest.main()