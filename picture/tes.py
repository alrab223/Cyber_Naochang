import os,glob,shutil
path="24hour"
files = os.listdir("24hour")
files_dir = [int(f) for f in files if os.path.isdir(os.path.join(path, f))]
sort_file = sorted(files_dir)
file_list = glob.glob(f"24hour/{sort_file[0]}/*.txt")
print(file_list)
shutil.rmtree(f"24hour/{sort_file[22]}")