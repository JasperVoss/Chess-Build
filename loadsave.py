def save_array(x, path):
	file = open(path, 'w')
	string = ''
	if len(x) == 0:
		pass
	else:
		if type(x[0]) == list:
			for i in x:
				for j in i:
					string += str(j) + ' '
				string = string[:-1]
				string += '\n'
		else:
			for i in x:
				string += str(i) + ' '
			string = string[:-1]

	file.write(string)
	file.close()

def load_array(path):
	x = ['']
	y = []
	file = open(path, 'r')
	for t in file.read():
		if t == ' ':
			x.append('')
		elif t == '\n':
			y.append(x)
			x = ['']
		else:
			x[-1] += t

	file.close()

	if y == []:
		return x
	else:
		return y