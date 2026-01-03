from pathlib import Path
import zipfile

src_root = Path(r"C:\Users\NAME\Desktop\ERA-5\era5_data")
out_root = Path(r"C:\Users\NAME\Desktop\ERA-5\extracted")
out_root.mkdir(parents=True, exist_ok=True)

zip_paths = list(src_root.rglob("*.nc"))  # your "nc" are actually zip files
print(f"Found {len(zip_paths)} zipped .nc files")

for zp in zip_paths:
    # Create a folder per archive (prevents name collisions)
    target_dir = out_root / zp.stem
    target_dir.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(zp, "r") as z:
            z.extractall(target_dir)
        print(f"Extracted: {zp.name} -> {target_dir}")
    except zipfile.BadZipFile:
        print(f"BAD ZIP (corrupt?): {zp}")
