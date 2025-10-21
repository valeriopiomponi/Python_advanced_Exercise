# main.py
from pathlib import Path

from semmeta.metadata_extractor_module import SEMMetaData
from semmeta.json_cleaner_module import JSONCleaner
from semmeta.visualizer_module import Visualizer


def build_raw_json(image_name: str) -> Path:
    """
    Uses SEMMetaData to open the .tif, gather EXIF + instrument metadata,
    and write output/<stem>_raw.json
    """
    sem = SEMMetaData()
    img = sem.OpenCheckImage(Path("imgs") / image_name)
    sem.ImageMetadata(img)

    exif_keys, exif_numbers = sem.SEMEXIF()
    found, missing = sem.GetExifMetadata(img, exif_keys, exif_numbers)
    exif_dict = sem.ExifMetaDict(found, missing)

    ins_list = sem.GetInsMetadata()
    ins_dict = sem.InsMetaDict(ins_list)

    stem = Path(image_name).stem
    out_path = Path("output") / f"{stem}_raw.json"
    semdict = {"exif": exif_dict, "instrument": ins_dict}
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sem.WriteSEMJson(out_path, semdict)
    return out_path


def main():
    # Ask for file name (can be with or without .tif)
    name = input("Enter the name of the image (.tif), e.g. LIL_test_defect02.tif: ").strip()
    if not name.lower().endswith(".tif"):
        name = f"{Path(name).stem}.tif"

    # 1) Extract & write RAW metadata JSON
    raw_path = build_raw_json(name)
    print(f"[1/3] Raw metadata saved to: {raw_path}")

    # 2) Clean JSON (remove None / 'null') -> output/<stem>_cleaned.json
    cleaner = JSONCleaner(output_dir="output")
    cleaned_path = cleaner.run(Path(name).stem)
    print(f"[2/3] Cleaned metadata saved to: {cleaned_path}")

    # 3) Visualize: show the image and print the small table
    viz = Visualizer(imgs_dir="imgs", output_dir="output")
    df = viz.run(Path(name).stem)
    print("\n[3/3] Visualization complete.")


if __name__ == "__main__":
    main()
