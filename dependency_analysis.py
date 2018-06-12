import sqlite3
from graphviz import Digraph
import argparse
import sqlite3
import ntpath


def is_from_import(class_paths, line):
	for class_path in class_paths:
		path_name = ntpath.basename(class_path[0])
		path_name = path_name.split('.')[0]+"."
		if(path_name in line):
			return path_name
	return ""

def unify(class_paths, sqlite_file, trial):
	
	
	conn = sqlite3.connect(sqlite_file)
	cursor = conn.cursor()
	cursor.execute('''select name
			from function_activation
			where trial_id = (?) and id=1''', (trial,))


	main_file = cursor.fetchone()[0]

	with open(main_file) as f:
		main_lines = f.readlines()
		f.close()

	class_lines = []

	for class_path in class_paths:
		fc = open(class_path[0], "r")
		class_lines += fc.readlines()
		class_lines.append("\n")
		fc.close()

	new_file_name = main_file.replace('.py', '')
	new_file_name = new_file_name + '-unified.py'
	new_file = open(new_file_name, 'w')
	new_file.write("".join(class_lines))


	for line in main_lines:
		if('import' not in line):
			path_name = is_from_import(class_paths, line)
			if(path_name != ''):
				line = line.replace(path_name, "")
			new_file.write(line)
	print("Your script has classes in different files, an auxilary script " +new_file_name+" was created so you can run noworkflow and our script again and get the dependencies.")

	new_file.close()
	conn.close()


def remove_duplicates(duplicated_list):
	aux_list = []
	for element in duplicated_list:
		if(element not in aux_list):
			aux_list.append(element)
	return aux_list

# <__main__.IdUff object at 0x1070ab6a0>  to IdUff
def object_string_to_class(obj_string):
	aux = obj_string.split(' ')[0]
	return(aux.split('.')[1])

def print_dependency(list_dependencies):
	for d in list_dependencies:
		print(d[0]+"  ---->   "+d[1])


def generate_graph(dependencies):
	g = Digraph('G', filename='DG.gv')
	
	for d in dependencies:
		if(d[0] != d[1]):
			g.edge(d[0], d[1])

	g.view()

def get_separate_files(sqlite_file, trial):
	conn = sqlite3.connect(sqlite_file)
	cursor = conn.cursor()
	cursor.execute(''' select m.path, d.trial_id
				from module as m , dependency as d
				where trial_id= (?)
	 ''', (trial,))
	class_paths = []
	for row in cursor:
		class_paths.append(row)

	return class_paths

def set_dependencies(sqlite_file, trial):

	conn = sqlite3.connect(sqlite_file)
	cursor = conn.cursor()
	#acha a dependencia de metodos
	cursor.execute(''' select FA.id, O.name, F.name, V.value, FA.trial_id
				from object O, function_def F, object_value V, function_activation FA
				where O.trial_id = (?) and
				F.trial_id = (?) and
				FA.trial_id = (?) and 
				V.trial_id = (?) and
				O.function_def_id = F.id and 
				V.function_activation_id=FA.id and
				V.name=substr(O.name,1,instr(O.name, '.')-1) and
				FA.name=substr(F.name,instr(F.name, '.')+1, length (F.name))
	 ''', (trial, trial, trial, trial,))

	dependency_01 = []

	# percorre as tuplas verificando object value self para garantir que está certo e depois salva as dependencias do tipo 01
	methods_dependency = []

	for row in cursor:
		methods_dependency.append(row)

	print("\nMethods dependencies:")

	to_print_methods_dependencies = []

	# percorre as tuplas verificando object value self para garantir que está certo e depois salva as dependencias do tipo 01
	for md in methods_dependency:

		func_activation = md[2]
		func_class = func_activation.split('.')[0]

		cursor.execute('''select value
			from object_value
			where function_activation_id = (?) and 
			name = 'self'
			''', (md[0],))

		for row in cursor:
			if(func_class in row[0]):
				#TODO: imprime varias vezes a mesma coisa
				string_to_print = md[2] + "\tuses\t" + md[1]
				if(string_to_print not in to_print_methods_dependencies):
					to_print_methods_dependencies.append(string_to_print)
					dependency_01.append([func_class, object_string_to_class(md[3])])

	for d in to_print_methods_dependencies:
		print(d)

	print()
	print_dependency(dependency_01)

	#acha dependencia de variaveis atraves de argumentos
	cursor.execute('''select FA.id, FA.name, OV.name, OV.value, FA.trial_id
	from object_value OV, function_activation FA
	where FA.trial_id = (?) and 
	OV.trial_id = (?) and
	FA.id = OV.function_activation_id and
	OV.type='ARGUMENT' ''', (trial, trial,))

	fa_arguments = {}
	fa_methods = {}

	#salva os argumentos de cada método 
	for row in cursor:
		fa_methods[row[0]] = row[1]
		if (row[0] in fa_arguments):
			fa_arguments[row[0]][row[2]] = row[3]
		else:
			fa_arguments[row[0]] = {row[2] : row[3]}

	# analisa os argumentos de cada método para achar as dependencias
	dependency_02 = []
	print("\nDependencies in arguments:")

	for fa, arg in fa_arguments.items():
		has_dependency = arg['self']
		parameters = ""
		for name, value in arg.items():
			if(name != 'self' and 'object' in value):
				parameters += name + " "
				dependency_02.append([object_string_to_class(has_dependency), object_string_to_class(value)])
		if(parameters != ""):
			print(fa_methods[fa] + "\tuses\t" + parameters )

	print()
	print_dependency(dependency_02)

	dependencies = dependency_01 + dependency_02


	generate_graph(remove_duplicates(dependencies))

	conn.close()


def main():
	parser = argparse.ArgumentParser(description='Dependency analysis')
	parser.add_argument("--db", help="set the path of the noworkflow db.sqlite", required=True)
	#parser.add_argument("--unify", help="If you have a script that has classes in different files")
	parser.add_argument("--trial", help="The number of the trial you want to do the analysis", required=True)
	args = parser.parse_args()

	# "/Users/tayanemoura/Documents/uff/mestrado/e-science/teste_mesma_classe_2/.noworkflow/db.sqlite"
	class_paths = get_separate_files(args.db, args.trial)
	if (class_paths):
		unify(class_paths, args.db, args.trial)
	else:
		set_dependencies(args.db, args.trial)

if __name__ == '__main__':
	main()	