import os
import sys
from semmeta import SEMMeta, CLEANER, SEMVisualizer

def main():
    if len(sys.argv) < 2:
        raise SystemExit(f"usage: {sys.argv[0]} <SEM image path>")

    semimage = sys.argv[1]
    image_name = os.path.splitext(os.path.basename(semimage))[0]
    #print("image name", image_name)

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    if os.path.isfile(semimage) and semimage.endswith(SEMMeta.semext):
        print(f"\nProcessing SEM IMAGE:", semimage)
        img = SEMMeta.OpenCheckImage(semimage)

        if img:
            print("Good image for processing", semimage)

            image_metadata, image_tags = SEMMeta.ImageMetadata(img)
            exif_keys, exif_number = SEMMeta.SEMEXIF
            found_exif_metadata, none_exif_metadata = SEMMeta.GetExifMetadata(img, exif_keys, exif_number)
            allexif_metadict = SEMMeta.ExifMetaDict(found_exif_metadata, none_exif_metadata)

            instrument_metadata = SEMMeta.GetInsMetadata
            instrument_meta_dict = SEMMeta.InsMetaDict(instrument_metadata)
            
            #img_name_dict = {"ImageOriginalName": semimage}
            #SEM_FULLMD_Dict = {**img_name_dict, **allexif_metadict, **instrument_meta_dict}
            
            SEM_FULLMD_Dict = {**allexif_metadict, **instrument_meta_dict}

            # Define output paths
            output_path_raw = os.path.join("output", f"{image_name}_RAW_SEMMetaData.json")
            output_path_cleaned = os.path.join("output", f"{image_name}_CLEANED_SEMMetaData.json")


            # Write raw metadata
            SEMMeta.WriteSEMJson(output_path_raw, SEM_FULLMD_Dict)


            # Clean and save cleaned metadata
            cleaned_data = CLEANER.process(output_path_raw)
            CLEANER.save_cleaned(output_path_cleaned)


            # Visualize image and metadata
            visualizer = SEMVisualizer(json_path=output_path_cleaned, image_path=semimage)
            visualizer.show_image_with_table()

        else:
            print("Bad image for processing", semimage)
    else:
        print("Invalid image path or unsupported format:", semimage)

if __name__ == "__main__":
    main()

