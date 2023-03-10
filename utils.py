import random, json, os


class Utils:
    def randomId(a: int = 2147483647, b: int = 4294967295) -> int:
        return random.randint(a, b)

    def writeJSON(*, data, path) -> dict:
        with open(path, "w", encoding="UTF-8", errors="ignore") as f:
            f.write(json.dumps(data, separators=(",", ":"), ensure_ascii=False))
            f.close()

    def importSettings() -> dict:
        return json.load(open("settings.json"))

    # Get normall file/dir name in directory
    def gnfnid(*, dir: str, searchStr: str) -> str:
        for n in os.listdir(dir):
            if n.lower() == searchStr.lower():
                return n

        return None

    # MotionPlatformSpecifics
    def getMPS(*, moveType) -> dict:
        if moveType == 0:
            return {
                "X360": {
                    "__class": "MotionPlatformSpecific",
                    "ScoreScale": 1,
                    "ScoreSmoothing": 0,
                    "LowThreshold": 0.2,
                    "HighThreshold": 1,
                },
                "ORBIS": {
                    "__class": "MotionPlatformSpecific",
                    "ScoreScale": 1,
                    "ScoreSmoothing": 0,
                    "LowThreshold": -0.2,
                    "HighThreshold": 0.6,
                },
                "DURANGO": {
                    "__class": "MotionPlatformSpecific",
                    "ScoreScale": 1,
                    "ScoreSmoothing": 0,
                    "LowThreshold": 0.2,
                    "HighThreshold": 1,
                },
            }
        elif moveType == 1:
            return {
                "X360": {
                    "__class": "MotionPlatformSpecific",
                    "ScoreScale": 1,
                    "ScoreSmoothing": 0,
                    "LowThreshold": 0.2,
                    "HighThreshold": 1,
                },
                "ORBIS": {
                    "__class": "MotionPlatformSpecific",
                    "ScoreScale": 3.5,
                    "ScoreSmoothing": 1,
                    "LowThreshold": -0.2,
                    "HighThreshold": 0.6,
                },
                "DURANGO": {
                    "__class": "MotionPlatformSpecific",
                    "ScoreScale": 3,
                    "ScoreSmoothing": 2,
                    "LowThreshold": 0.2,
                    "HighThreshold": 1,
                },
            }
        else:
            return {}

    def classifierPath(*, name: str, mapName: str):
        name = name.replace("\\", "/")
        name = name.split("/")[-1]
        try:
            name, ext = name.split(".")
            return f"world/maps/{mapName}/timeline/moves/{name}.{ext}".lower()
        except:
            return f"world/maps/{mapName}/timeline/moves/{name}.msm".lower()

    def createPhoneImages(*, coachCount: int, mapName: str):
        phoneImages = {
            "cover": f"world/maps/{mapName}/menuart/textures/{mapName}_cover_phone.jpg".lower()
        }

        for i in range(coachCount):
            phoneImages[
                f"coach{i+1}"
            ] = f"world/maps/{mapName}/menuart/textures/{mapName}_coach_{i+1}_phone.png".lower()

        return phoneImages
