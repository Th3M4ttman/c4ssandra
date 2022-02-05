
import os
import shutil

for base, dirs, files in os.walk("/storage/emulated/0/C4ssandra/Bot/commands"):
	for file in files:
		if dirs != ["__pycache__"] or ".json" in file or ".joblib" in file:
			continue
		
		
		src = "/storage/emulated/0/C4ssandra/Bot/commands/" + file
		dst = "/data/data/com.termux/files/home/storage/Programming/Bot/commands/" + file
		if os.path.exists(dst):
			os.remove(dst)
		shutil.copy(src, dst)
print("Copied")

os.system("sudo git add -A;sudo git commit -m .;sudo git push")
