import time
from cereal.messaging import SubMaster

class World:
    has_started = False
    start_time = 0

    sm = None
    data = {}
    header = {}

    @staticmethod
    def start():
        World.sm = SubMaster(["sensorEvents"])
        World.has_started = World.sm is not None
        World.data = []
        World.rows = [
                {"key": "sensorEvents/gyroUncalibrated/v"},
                {"key": "put_any_string_also_can_but_this_is_v1"},
                ]
        World.start_time = time.time()

    @staticmethod
    def stop():
        World.sm = None
        World.has_started = False

def tick():
    if not World.has_started:
        return

    t = time.time()
    World.sm.update()
    for ev in World.sm["sensorEvents"]:
        if ev.sensor == 5:
            World.data.append({
                "time": t - World.start_time,
                World.rows[0]["key"]: ev.gyroUncalibrated.v[0],
                World.rows[1]["key"]: ev.gyroUncalibrated.v[1],
            })

