import boto3
import json

def utf8len(s):
    return len(s.encode('utf-8'))

def sentiment(text):
	comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

	l = utf8len(text)
	diff = l - 5000
	if diff > 0:
		m = diff // 2
		text = text[m:-m]

	print('Calling DetectSentiment')
	sent = comprehend.detect_sentiment(Text=text, LanguageCode='es')
	print('End of DetectSentiment\n')

	return sent