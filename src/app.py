from lib.tools.tools import *
from time import sleep
import os
from lib.transcribe import *

def menu():
	while True:
		print('---- Menu ----')
		print('[1] Add file.')
		print('[2] Add files.')
		print('[0] EXIT.')
		res = input(': ')

		if res == '0': break
		elif res == '1':
			print('\nPlease indicate the path of the file to be processed')
			fpath = input(': ')

			if os.path.isfile(fpath) == False:
				# raise(Exception(f'Oops!  {fpath} is not an expected filepath parameter.  Try again...'))
				print(f'Oops!  {fpath} is not an expected filepath parameter.  Try again...')
			else:
				return res, fpath

		elif res == '2':
			print('\nPlease indicate the path of the folder with files to be processed')
			path = input(': ')

			if os.path.isdir(path) == False:
				# raise(Exception(f'Oops!  {path} is not an expected path parameter.  Try again...'))
				print(f'Oops!  {path} is not an expected path parameter.  Try again...')
			else:
				return res, path

		else:
			raise(Exception(f'Oops!  {res} is not an expected menu paramater.  Try again...'))

		print('\n\n')

	return res, None

def main():
	# ---------- select option ----------
	r, path = menu()
	if r == '0': return

	# ---------- transcribe ----------
	print('-' * 100)
	text = []
	if r == '1':
		media_file_name = path
		media_object_key = media_file_name[path.rfind('/') + 1:]

		text.append(transcribe(media_file_name, media_object_key))

	elif r == '2':
		media_files_names = os.listdir(path)
		for media_object_key in media_files_names:
			media_file_name = path + media_object_key

			text.append(transcribe(media_file_name, media_object_key))

	print(text)


if __name__ == '__main__':
	clear()
	sleep(1)
	print('-' * 100)
	print('Welcome to "El Analista" demo!')
	print('-' * 100)

	main()

	print('-' * 100)
	print("Thanks for trying!")
	print('-' * 100)