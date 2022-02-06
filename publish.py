import os
import shutil

error = False

p = "/storage/emulated/0/C4ssandra/Bot/commands"
t = "/data/data/com.termux/files/home/storage/Programming/Bot/commands"
for root, folders, files in os.walk(p, topdown=False):
	#print(root, folders, files)
	if "__pycache__" in root:
		continue
	for folder in folders:
		if folder != "__pycache__":
			if os.path.exists((root + folder).replace(p, t)):
				print("Copy")
			else:
				try:
					os.mkdir((root + "/" + folder).replace(p, t))
					print("Created", folder)
				except Exception as e:
					print(e)
					error = True
				
	for file in files:
		if ".json" in file:
			pass
		src = root + "/" + file
		dst = root.replace(p, t) + "/" + file
		try:
			shutil.copy(src, dst)
		except Exception as e:
			print(e)
			error = True
		print("Copied", file)
		
if not error:
	print("\nCopied\n")
	os.system("sudo git add -A")
	os.system("sudo git commit -m . ")
	os.system("sudo git push")
	print("\nPublished\n")
else:
	print("Copy Error Git Aborted")