
class Bucket:

    def __init__(self, b_avg, b_std, D=30, B=1, abort=False, reset=False, inverse=False):
        """

        :param b_avg: baseline average
        :param b_std: baseline standard deviation
        :param D: depth of each bucket (Default 30)
        :param B: Number of buckets    (Default 1)
        :param abort: if True will raise Overflow exception when all buckets are full
        :param reset: if True will reset counter after filling all buckets (empty all buckets)
        :param inverse: if True will invert the logic which interpret 
        the metric (the lower the better).  
            E.g. Usefull for Throughput, instead of Response Time.
        """
        self.inverse = inverse
        self.B = B
        self.D = D

        self.avg = b_avg
        self.std = b_std

        self._threshold = B * D

        self.abort = abort
        self.reset = reset

        # Bucktes will be an represented by arithmetic operations
        self.counter = 0

        self.p = 0
        self.d = 0

    def update_baselines(self, b_avg, b_std):
        self.avg = b_avg
        self.std = b_std

    def add_sample(self, rt):
        """
        :param rt: return time to analyse
        :return:
                  0 == Not n degraded state
                > 0 == Degraded scale
                > B * D == System in alert (will follow the
                       accumulation of the degraded scale but in negative value)

        """

        # using the function to add support for different metrics
        if self.compare(rt):
            self.counter += 1
        else:
            self.counter -= 1

            if self.counter < 0:
                # Again, we do not stop iterating, so, fix the negative values
                # Also, negative values help us keep track
                self.counter = 0
                self.d = 0
                return 0

        return_counter = self.counter
        # we should update the pointers again
        self.update_bucket_pointer()
        self.d = self.counter % self.D

        if return_counter >= self._threshold:
            if self.reset:
                self.counter = 0
            if self.abort:
                raise OverflowError()

        return return_counter

    def update_bucket_pointer(self):
        # Is we are not resetting the counter we can have and unlimited increase on the
        # stdev window (which depends on p) so we need to update the pointer
        if self.counter >= self._threshold:
            # We count from zero, so:  B-1
            self.p = self.B - 1
        else:
            self.p = self.counter / self.D

    def compare(self, rt):
        # We need to update the pointer before the  comparison
        self.update_bucket_pointer()
        if self.inverse:
            return rt < self.avg - (self.p * self.std)
        else:
            return rt > self.avg + (self.p * self.std)
        pass





