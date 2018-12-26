def file_append(filename, data):
	f = open(filename,'w+')
	f.write(data)
	f.close