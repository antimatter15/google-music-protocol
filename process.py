import os
directory = "musicman2.saz_FILES/raw/"
for f in os.listdir(directory):
	if f.endswith("_c.txt"):
		print directory + f
		fz = open(directory + f).read().split("\r\n\r\n")[0]
		if fz.startswith("CONNECT"):
			continue
		xf = f.replace("_c","")
		fh = open("parsed/"+xf, "w")
		fh.write(fz + "\n\n")
		fh.close()
		os.system("cat "+ directory + f +" | python strip.py | protoc --decode_raw >> parsed/"+xf)
		f = f.replace("_c.txt", "_s.txt")
		fz = open(directory + f).read().split("\r\n\r\n")[0]
		fh = open("parsed/"+xf, "a")
		fh.write("\n\n\n\n" + fz + "\n\n")
		fh.close()
		os.system("cat "+ directory + f +" | python strip.py | protoc --decode_raw >> parsed/"+xf)