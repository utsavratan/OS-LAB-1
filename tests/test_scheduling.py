import unittest

from oslab.scheduling import (
    DEMO_PROCESSES,
    Process,
    averages,
    fcfs,
    round_robin,
    simulate,
)


class SchedulingTests(unittest.TestCase):
    def test_fcfs_completion_and_waiting(self):
        ps = [Process("P1", 0, 5), Process("P2", 1, 3)]
        results, segments = fcfs(ps)
        by_name = {r.name: r for r in results}
        self.assertEqual(by_name["P1"].completion, 5)
        self.assertEqual(by_name["P2"].completion, 8)
        self.assertEqual(by_name["P2"].waiting, 4)
        self.assertEqual(segments[-1].end, 8)

    def test_round_robin_completes_every_process(self):
        results, _ = round_robin(DEMO_PROCESSES, 2)
        self.assertEqual(len(results), len(DEMO_PROCESSES))
        self.assertTrue(all(r.completion > 0 for r in results))

    def test_metrics_are_non_negative(self):
        results, _ = simulate("srtf", DEMO_PROCESSES)
        avg = averages(results)
        self.assertGreaterEqual(avg["waiting"], 0)
        self.assertGreaterEqual(avg["turnaround"], 0)
        self.assertGreaterEqual(avg["response"], 0)

    def test_invalid_quantum(self):
        with self.assertRaises(ValueError):
            round_robin(DEMO_PROCESSES, 0)

    def test_duplicate_names(self):
        with self.assertRaises(ValueError):
            fcfs([Process("P1", 0, 2), Process("P1", 1, 3)])


if __name__ == "__main__":
    unittest.main()
