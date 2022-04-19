from cereal.messaging import SubMaster

class World:
    has_started = False

    sm = None
    data = {}

    @staticmethod
    def start():
        World.sm = SubMaster(["sensorEvents"])
        World.has_started = World.sm is not None
        World.data = {"data":[]}

    @staticmethod
    def stop():
        World.sm = None
        World.has_started = False

def tick():
    print("has_started", World.has_started)
    if not World.has_started:
        return

    World.sm.update()
    for ev in World.sm["sensorEvents"]:
        if ev.sensor == 5:
            World.data["data"].append(list(ev.gyroUncalibrated.v))
