import os
import glob
import pathlib
import mimetypes

def video_modification(video_path):
	
	video_path_list = video_path.split('/')
	output_path = video_path[:-1]+'/new-'+video_path[-1]
  
	print('Trimming video:',video_path[-1])
	start_sec = input("Start from:")
	end_sec = input("End in:")
	command = f"ffmpeg -i {video_path} -ss {start_sec} -to {end_sec} -c:v copy -c:a copy {output_path}"

	print('\n')
	print(command)
	#os.system(command)
 
def path_grabber(ext=''):
	f_list = glob.glob("*"+ext)
	dir_list = []
	file_list = []
	i = 0
	for f in f_list:
		if pathlib.Path(f).is_dir():
			dir_list.append(f)
		else:
			i+= 1
			file_list.append([f,os.path.getsize(f),mimetypes.guess_type(f)])

	return file_list, dir_list


def file_choose(file_list):
	
	for f in file_list:
		print(file_list.index(f)+1,f[0])

	choose_fnr = int(input("Choose file: "))
	f_name = file_list[choose_fnr-1][0]
	f_ext = pathlib.Path(f_name).suffix
	print('File:',f_name,'  ext:',f_ext,'\nStats:',pathlib.Path(f_name).stat())
	
	return f_name, f_ext

print(os.get_terminal_size())
print('\nLista plików i katalogów w:',os.getcwd()) # pathlib.sys.executable)
files_list, dirs_list = path_grabber(ext='')

print('\nIlość plików:',len(files_list))
print('Ilość katalogów:',len(dirs_list))

print('\n1. Pokaż listę plików.')
print('2. Pokaż listę katalogów.')
print()
print('q. wyjdź ', end='\t')
while True:
	i = input()
	print()
	if i == '1':
		f_name, f_ext = file_choose(files_list)

	elif i == '2':
		pass
	elif i == 'q':
		SystemExit()


if f_ext in ('mp4','video'):
  video_modification(os.getcwd()+'/'+f_name)
