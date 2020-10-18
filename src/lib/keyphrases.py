import boto3
import json

a, na = 'áéíóú', 'aeiou'
trans = str.maketrans(a, na)

def key_phrases(text):
	comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

	print('Calling DetectKeyPhrases')
	keyp = comprehend.detect_key_phrases(Text=text, LanguageCode='es')
	print('End of DetectKeyPhrases\n')

	return keyp