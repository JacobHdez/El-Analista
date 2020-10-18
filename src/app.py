from lib.tools.tools import clear
from time import sleep
import os
from lib.transcribe import transcribe
from lib.summary import summary
from lib.keyphrases import key_phrases
from lib.sentiment import sentiment

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
	transcribe_text = []
	if r == '1':
		media_file_name = path
		media_object_key = media_file_name[path.rfind('/') + 1:]

		transcribe_text.append(transcribe(media_file_name, media_object_key))

	elif r == '2':
		media_files_names = os.listdir(path)
		for media_object_key in media_files_names:
			media_file_name = path + media_object_key

			transcribe_text.append(transcribe(media_file_name, media_object_key))

	# ---------- sentiment ----------
	print('-' * 100)
	sentiment_out = []
	if r == '1':
		sentiment_out.append(sentiment(transcribe_text[0]))

	elif r == '2':
		for t_text in transcribe_text:
			sentiment_out.append(sentiment(t_text))

	# print(sentiment_out)

	# ---------- summary ----------
	print('-' * 100)
	summary_text = []
	if r == '1':
		summary_text.append(summary(transcribe_text[0])[0])

	elif r == '2':
		for t_text in transcribe_text:
			summary_text.append(summary(t_text)[0])

	# print(summary_text)

	# ---------- key phrases ----------
	print('-' * 100)
	keyp = []
	if r == '1':
		keyp.append(key_phrases(summary_text[0]))

	elif r == '2':
		for s_text in summary_text:
			keyp.append(key_phrases(s_text))

	# print(keyp)

	# ---------- class to be archived to be read in the nootebook to show result  ----------
	# ...


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
	input()