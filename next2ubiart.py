import os, UnityPy
from utils import Utils
from PIL import Image

settings = Utils.importSettings()

songCoachCount: int = 1


def convertMapMB(
    *,
    tree: dict = {},
    outputDir: str,
    ktapeName: str,
    dtapeName: str,
    mainSequenceName: str,
):
    MapName = tree["MapName"]

    if "KaraokeData" in tree:
        print("Converting KaraokeData")

        Tape = {
            "__class": "Tape",
            "Clips": [],
            "TapeClock": 0,
            "TapeBarCount": 1,
            "FreeResourcesAfterPlay": 0,
            "MapName": MapName,
            "SoundwichEvent": "",
        }

        for ClipTree in tree["KaraokeData"]["Clips"]:
            KaraokeClipTree = ClipTree.get("KaraokeClip", None)

            if KaraokeClipTree:
                Clip = {
                    "__class": "KaraokeClip",
                    "Id": Utils.randomId(),
                    "TrackId": Utils.randomId(),
                    "IsActive": KaraokeClipTree["IsActive"],
                    "StartTime": KaraokeClipTree["StartTime"],
                    "Duration": KaraokeClipTree["Duration"],
                    "Pitch": KaraokeClipTree["Pitch"],
                    "Lyrics": KaraokeClipTree["Lyrics"],
                    "IsEndOfLine": KaraokeClipTree["IsEndOfLine"],
                    "ContentType": KaraokeClipTree["ContentType"],
                    "StartTimeTolerance": KaraokeClipTree["StartTimeTolerance"],
                    "EndTimeTolerance": KaraokeClipTree["EndTimeTolerance"],
                    "SemitoneTolerance": KaraokeClipTree["SemitoneTolerance"],
                }

                Tape["Clips"].append(Clip)

        Tape["Clips"].sort(
            key=lambda x: x["Id"] - x["TrackId"] + (x["StartTime"] * 10000)
        )

        Utils.writeJSON(data=Tape, path=f"{outputDir}/{ktapeName}")

    if "DanceData" in tree:
        print("Converting DanceData")

        Tape = {
            "__class": "Tape",
            "Clips": [],
            "TapeClock": 0,
            "TapeBarCount": 1,
            "FreeResourcesAfterPlay": 0,
            "MapName": MapName,
            "SoundwichEvent": "",
        }

        MotionClips = tree["DanceData"].get("MotionClips", [])
        PictoClips = tree["DanceData"].get("PictoClips", [])
        GoldEffectClips = tree["DanceData"].get("GoldEffectClips", [])
        HideHudClips = tree["DanceData"].get("HideHudClips", [])

        for ClipTree in MotionClips:

            Clip = {
                "__class": "MotionClip",
                "Id": Utils.randomId(),
                "TrackId": Utils.randomId(),
                "IsActive": ClipTree["IsActive"],
                "StartTime": ClipTree["StartTime"],
                "Duration": ClipTree["Duration"],
                "ClassifierPath": Utils.classifierPath(
                    name=ClipTree["MoveName"], mapName=MapName
                ),
                "GoldMove": ClipTree["GoldMove"],
                "CoachId": ClipTree["CoachId"],
                "MoveType": ClipTree["MoveType"],
                "Color": [1, 1, 0, 0],
                "MotionPlatformSpecifics": Utils.getMPS(moveType=ClipTree["MoveType"]),
            }

            Tape["Clips"].append(Clip)

        for ClipTree in PictoClips:
            PictoName = ClipTree["PictoPath"]
            ext = settings.get("default_picto_ext", "png")

            Clip = {
                "__class": "PictogramClip",
                "Id": Utils.randomId(),
                "TrackId": Utils.randomId(),
                "IsActive": ClipTree["IsActive"],
                "StartTime": ClipTree["StartTime"],
                "Duration": ClipTree["Duration"],
                "PictoPath": f"world/maps/{MapName}/timeline/pictos/{PictoName}.{ext}".lower(),
                "CoachCount": ClipTree["CoachCount"],
            }

            Tape["Clips"].append(Clip)

        for ClipTree in GoldEffectClips:
            Clip = {
                "__class": "GoldEffectClip",
                "Id": Utils.randomId(),
                "TrackId": Utils.randomId(),
                "IsActive": ClipTree["IsActive"],
                "StartTime": ClipTree["StartTime"],
                "Duration": ClipTree["Duration"],
                "EffectType": ClipTree["GoldEffectType"],
            }

            Tape["Clips"].append(Clip)

        Tape["Clips"].sort(
            key=lambda x: x["Id"] - x["TrackId"] + (x["StartTime"] * 10000)
        )

        Utils.writeJSON(data=Tape, path=f"{outputDir}/{dtapeName}")

        Tape = {
            "__class": "Tape",
            "Clips": [],
            "TapeClock": 0,
            "TapeBarCount": 1,
            "FreeResourcesAfterPlay": 0,
            "MapName": MapName,
            "SoundwichEvent": "",
        }

        for ClipTree in HideHudClips:
            Clip = {
                "__class": "HideUserInterfaceClip",
                "Id": Utils.randomId(),
                "TrackId": Utils.randomId(),
                "IsActive": ClipTree["IsActive"],
                "StartTime": ClipTree["StartTime"],
                "Duration": ClipTree["Duration"],
                "EventType": 18,
                "CustomParam": "",
            }

            Tape["Clips"].append(Clip)

        Tape["Clips"].sort(
            key=lambda x: x["Id"] - x["TrackId"] + (x["StartTime"] * 10000)
        )

        Utils.writeJSON(data=Tape, path=f"{outputDir}/{mainSequenceName}")

    if "SongDesc" in tree:
        SongDescComponent = {
            "__class": "JD_SongDescTemplate",
            "MapName": tree["SongDesc"]["MapName"],
            "JDVersion": 2017,
            "OriginalJDVersion": 2017,
            "RelatedAlbums": tree["SongDesc"]["MapName"],
            "Artist": "Unknown Artist",
            "DancerName": "Unknown Dancer Name",
            "Title": "Unknown Title",
            "Credits": "Unknown Credits",
            "PhoneImages": Utils.createPhoneImages(
                coachCount=tree["SongDesc"]["NumCoach"], mapName=MapName
            ),
            "NumCoach": tree["SongDesc"]["NumCoach"],
            "MainCoach": -1,
            "Difficulty": tree["SongDesc"]["Difficulty"],
            "SweatDifficulty": tree["SongDesc"]["SweatDifficulty"],
            "backgroundType": 0,
            "LyricsType": 0,
            "Energy": 1,
            "Tags": ["main"],
            "Status": 3,
            "LocaleID": 4294967295,
            "MojoValue": 0,
            "CountInProgression": 1,
            "DefaultColors": {"lyrics": [1, 1, 0, 0], "theme": [1, 1, 1, 1]},
            "VideoPreviewPath": "",
        }

        Utils.writeJSON(
            data={
                "__class": "Actor_Template",
                "WIP": 0,
                "LOWUPDATE": 0,
                "UPDATE_LAYER": 0,
                "PROCEDURAL": 0,
                "STARTPAUSED": 0,
                "FORCEISENVIRONMENT": 0,
                "COMPONENTS": [SongDescComponent],
            },
            path=f"{outputDir}/songdesc.tpl.ckd",
        )


def convertMusicTrack(
    *, mapName: str = "EmptyMapName", tree: dict = {}, outputDir: str, mtName: str
):
    print("Converting MusicTrack")

    structure: dict = tree["m_structure"]["MusicTrackStructure"]
    audioExt = settings.get("default_audio_format_ext", "wav")

    MusicTrackComponent = {
        "__class": "MusicTrackComponent_Template",
        "trackData": {
            "__class": "MusicTrackData",
            "structure": {
                "__class": "MusicTrackStructure",
                "markers": list(map(lambda m: m["VAL"], structure["markers"])),
                "signatures": list(
                    map(
                        lambda s: {
                            "__class": "MusicSignature",
                            "marker": int(s["MusicSignature"]["marker"]),
                            "beats": int(s["MusicSignature"]["beats"]),
                        }
                        if s["MusicSignature"]
                        else None,
                        structure["signatures"],
                    )
                ),
                "sections": list(
                    map(
                        lambda s: {
                            "__class": "MusicSection",
                            "marker": int(s["MusicSection"]["marker"]),
                            "sectionType": int(s["MusicSection"]["sectionType"]),
                            "comment": "",
                        }
                        if s["MusicSection"]
                        else None,
                        structure["sections"],
                    )
                ),
                "startBeat": int(structure.get("startBeat", 0)),
                "endBeat": int(structure.get("endBeat", 0)),
                "fadeStartBeat": int(structure.get("fadeStartBeat", 0)),
                "useFadeStartBeat": structure.get("useFadeStartBeat", False),
                "fadeEndBeat": int(structure.get("fadeEndBeat", 0)),
                "useFadeEndBeat": structure.get("useFadeEndBeat", False),
                "videoStartTime": float(structure.get("videoStartTime", 0)),
                "previewEntry": int(structure.get("previewEntry", 0)),
                "previewLoopStart": int(structure.get("previewLoopStart", 0)),
                "previewLoopEnd": int(structure.get("previewLoopEnd", 0)),
                "volume": float(structure.get("volume", 0)),
                "fadeInDuration": int(structure.get("fadeInDuration", 0)),
                "fadeInType": int(structure.get("fadeInType", 0)),
                "fadeOutDuration": int(structure.get("fadeOutDuration", 0)),
                "fadeOutType": int(structure.get("fadeOutType", 0)),
            },
            "path": f"world/maps/{mapName}/audio/{mapName}.{audioExt}".lower(),
            "url": f"jmcs://jd-contents/{mapName}/{mapName}.ogg",
        },
    }

    Utils.writeJSON(
        data={
            "__class": "Actor_Template",
            "WIP": 0,
            "LOWUPDATE": 0,
            "UPDATE_LAYER": 0,
            "PROCEDURAL": 0,
            "STARTPAUSED": 0,
            "FORCEISENVIRONMENT": 0,
            "COMPONENTS": [MusicTrackComponent],
        },
        path=f"{outputDir}/{mtName}",
    )


def convertPictos(*, obj: any, outputDir: str):
    data = obj.read()

    width, height = round(data.__getitem__("m_Rect")["width"]), round(
        data.__getitem__("m_Rect")["height"]
    )

    rectX, rectY, rectWidth, rectHeight = (
        round(data.__getitem__("m_RD")["textureRect"]["x"]),
        round(data.__getitem__("m_RD")["textureRect"]["y"]),
        round(data.__getitem__("m_RD")["textureRect"]["width"]),
        round(data.__getitem__("m_RD")["textureRect"]["height"]),
    )

    canvas = Image.new("RGBA", (width, height), (255, 0, 0, 0))
    img = data.image

    img = img.convert("RGBA")

    position = (
        rectX,
        height - rectHeight - rectY,
    )

    canvas.paste(img, position)

    if 1.445 < width / height < 1.447:
        if width >= 512 and height >= 354:
            canvas = canvas.resize((1024, 512))
        else:
            canvas = canvas.resize((256, 256))

    canvas.save(f"{outputDir}/pictos/{data.name}.png".lower(), quality=100)

    canvas.close()
    img.close()


def main():
    print("Welcome to the Next2UbiArt conversion tool by Bezdrom")

    # Creating dirs
    os.makedirs("output", exist_ok=True)

    try:
        if os.listdir("input").__len__() == 0:
            return print("The /input directory is empty")

        for mapFolderName in os.listdir("input"):
            print(f"-- {mapFolderName} --")

            mapDir = f"input/{mapFolderName}"

            os.makedirs(f"output/{mapFolderName}", exist_ok=True)

            mapPackageName = (
                Utils.gnfnid(dir=mapDir, searchStr="mapPackage")
                or Utils.gnfnid(dir=mapDir, searchStr="mapPackage.bundle")
                or Utils.gnfnid(dir=mapDir, searchStr=f"{mapFolderName}.bundle")
                or Utils.gnfnid(
                    dir=mapDir, searchStr=f"{mapFolderName}_mapPackage.bundle"
                )
                or Utils.gnfnid(dir=mapDir, searchStr=f"{mapFolderName}_mapPackage")
            )

            coachesLargeName = (
                Utils.gnfnid(dir=mapDir, searchStr="coachesLarge")
                or Utils.gnfnid(dir=mapDir, searchStr="coachesLarge.bundle")
                or Utils.gnfnid(
                    dir=mapDir, searchStr=f"{mapFolderName}_coachesLarge.bundle"
                )
                or Utils.gnfnid(dir=mapDir, searchStr=f"{mapFolderName}_coachesLarge")
            )

            if mapPackageName is None:
                print(
                    f"mapPackage for {mapFolderName} not found in /input/{mapFolderName}/ directory"
                )

            """
            if coachesLargeName is None:
                print(
                    f"coachesLarge for {mapFolderName} not found in /input/{mapFolderName}/ directory"
                )
            """

            if mapPackageName:
                os.makedirs(f"output/{mapFolderName}/moves/wiiu", exist_ok=True)
                os.makedirs(f"output/{mapFolderName}/pictos", exist_ok=True)

                with open(f"{mapDir}/{mapPackageName}") as mpf:
                    env = UnityPy.load(f"{mapDir}/{mapPackageName}")

                    for obj in env.objects:
                        # print(obj.type.name)

                        if obj.type.name == "TextAsset":
                            data = obj.read()
                            with open(
                                f"output/{mapFolderName}/moves/wiiu/{(data.name.lower())}",
                                "wb+",
                            ) as f:
                                f.write(bytes(data.script))
                                f.close()

                        if obj.type.name == "MonoBehaviour":
                            if obj.serialized_type.nodes:
                                tree = obj.read_typetree()

                                # <main_song>.json
                                if tree["m_Name"].lower() == mapFolderName.lower():
                                    convertMapMB(
                                        tree=tree,
                                        outputDir=f"output/{mapFolderName}",
                                        ktapeName=f"{mapFolderName}_tml_karaoke.ktape.ckd".lower(),
                                        dtapeName=f"{mapFolderName}_tml_dance.dtape.ckd".lower(),
                                        mainSequenceName=f"{mapFolderName}_mainsequence.tape.ckd".lower(),
                                    )

                                # MusicTrack
                                if tree["m_Name"] == "":
                                    convertMusicTrack(
                                        mapName=mapFolderName,
                                        tree=tree,
                                        outputDir=f"output/{mapFolderName}",
                                        mtName=f"{mapFolderName}_musictrack.tpl.ckd".lower(),
                                    )

                        if obj.type.name == "Sprite":
                            convertPictos(obj=obj, outputDir=f"output/{mapFolderName}")

                    f.close()

                with open(f"{mapDir}/{mapPackageName}") as mpf:
                    print("Converting Pictos")

                    env = UnityPy.load(f"{mapDir}/{mapPackageName}")

                    for obj in env.objects:
                        if obj.type.name == "Sprite":
                            convertPictos(obj=obj, outputDir=f"output/{mapFolderName}")

                    f.close()

    except WindowsError:
        print("The script was not found /input directory, create it")


if __name__ == "__main__":
    main()
    input("Press ENTER to end the program...")
