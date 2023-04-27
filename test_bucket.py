from unittest import TestCase

from bucket import Bucket


class TestBucket(TestCase):

    def setUp(self):
        self.b = Bucket(0.5, 0.2, 2, 3)
        """
        p -> plateau
        0  > 0.5
        1  > 0.7
        2  > 0.9 
        """

    def test_update_baselines(self):
        self.assertEqual(self.b.avg, 0.5)
        self.assertEqual(self.b.std, 0.2)
        self.b.update_baselines(0.1, 0.3)
        self.assertEqual(self.b.avg, 0.1)
        self.assertEqual(self.b.std, 0.3)

    def test_increasing_sample(self):
        v = [ x + 0.5 for x in [x/10.0 for x in range(20)]]
        r = [0, 1, 2, 3, 4, 5, 6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19]
        res = []
        for i in range(len(v)):
            res.append(self.b.add_sample(v[i]))
        self.assertListEqual(r, res)

    def test_alert_restoration(self):
        v = [1] * 7 + [0.5] * 7 + [1] * 8
        r = [1, 2, 3, 4, 5, 6, -7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 6, -7, -8]
        res = []
        for i in range(len(v)):
            res.append(self.b.add_sample(v[i]))
        self.assertListEqual(r, res)


