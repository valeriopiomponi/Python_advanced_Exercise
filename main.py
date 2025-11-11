from pathlib import Path
from semmeta.metadata_extractor_module import SEMMetaData
from semmeta.json_cleaner_module import JSONCleaner
from semmeta.visualizer_module import Visualizer

def main():
    name = input("Enter image file name (e.g. LIL_test_defect02.tif): ").strip()
    if not name.lower().endswith(".tif"):
        name = f"{Path(name).stem}.tif"

    # 1) raw metadata
    sem = SEMMetaData()
    img = sem.OpenCheckImage(Path("imgs") / name)
    sem.ImageMetadata(img)
    exif_keys, exif_nums = sem.SEMEXIF()
    found, missing = sem.GetExifMetadata(img, exif_keys, exif_nums)
    exif_dict = sem.ExifMetaDict(found, missing)
    ins_list = sem.GetInsMetadata()
    ins_dict = sem.InsMetaDict(ins_list)
    raw_path = Path("output") / f"{Path(name).stem}_raw.json"
    sem.WriteSEMJson(raw_path, {"exif": exif_dict, "instrument": ins_dict})
    print(f"[1/3] wrote {raw_path}")

    # 2) cleaned json
    cleaner = JSONCleaner()
    cleaned_path = cleaner.run(Path(name).stem)
    print(f"[2/3] wrote {cleaned_path}")

    # 3) visualize
    viz = Visualizer()
    viz.run(Path(name).stem)
    print("[3/3] done")

if __name__ == "__main__":
    main()
