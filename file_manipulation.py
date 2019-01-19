def file_append(filename, data):
	f = open(filename, "a")
	f.write(data)
	f.write("\r\n")
	f.close
