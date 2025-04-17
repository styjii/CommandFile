### Usage

modify the target_directory in the script and use this:

```bash
python rename_files.py
```

#### Example usage in python command line

```bash
>>> from rename_files import rename_files
>>> # specified here your path
>>> target_directory = "/sdcard/drama"
>>> # get the new name of the files
>>> rename_files(
... extensions=["mp4", "avi"],
... source_directory=target_directory,
... name_template="DRAMA S{numbers[0]}E{numbers[1]}"
... )
[DRY RUN] /sdcard/drama/01DRAMA-01.mp4 -> /sdcard/drama/DRAMA S1E1.mp4
[DRY RUN] /sdcard/drama/01DRAMA-02.mp4 -> /sdcard/drama/DRAMA S1E2.mp4
[DRY RUN] /sdcard/drama/01DRAMA-03.mp4 -> /sdcard/drama/DRAMA S1E3.mp4
[DRY RUN] /sdcard/drama/01DRAMA-04.mp4 -> /sdcard/drama/DRAMA S1E4.mp4
>>> # rename files
>>> rename_files(
... extensions=["mp4", "avi"],
... source_directory=target_directory,
... name_template="DRAMA S{numbers[0]}E{numbers[1]}",
... dry_run=False
... )
[RENAMED] 01DRAMA-01.mp4 -> DRAMA S1E1.mp4
[RENAMED] 01DRAMA-02.mp4 -> DRAMA S1E2.mp4
[RENAMED] 01DRAMA-03.mp4 -> DRAMA S1E3.mp4
[RENAMED] 01DRAMA-04.mp4 -> DRAMA S1E4.mp4
```
