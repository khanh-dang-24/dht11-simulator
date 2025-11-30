import random
import math
import time

class DHT11Sim:
    def __init__(self, base_temp=26.0, base_hum=60.0, fail_rate=0.03, drift_std=0.02):
        self.base_temp = float(base_temp)
        self.base_hum = float(base_hum)
        self.fail_rate = float(fail_rate)
        self.drift_std = float(drift_std)
        self._t = self.base_temp
        self._h = self.base_hum
        self._last_update = time.time()

    def _step_drift(self):
        now = time.time()
        dt = max(0.0001, now - self._last_update)
        self._last_update = now
        self._t += random.gauss(0.0, self.drift_std) * math.sqrt(dt)
        self._h += random.gauss(0.0, self.drift_std) * math.sqrt(dt)
        self._t = min(max(self._t, -10.0), 60.0)
        self._h = min(max(self._h, 0.0), 100.0)

    def readTemperature(self):
        if random.random() < self.fail_rate:
            return None
        self._step_drift()
        noise = random.gauss(0.0, 0.25)
        return round(self._t + noise, 1)

    def readHumidity(self):
        if random.random() < self.fail_rate:
            return None
        self._step_drift()
        noise = random.gauss(0.0, 0.8)
        return round(self._h + noise, 1)
