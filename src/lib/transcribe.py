# Programa basado en transcribe_basics.py como apoyo rapido.
# https://docs.aws.amazon.com/code-samples/latest/catalog/python-transcribe-transcribe_basics.py.html

import logging
import boto3
from time import time_ns
from botocore.exceptions import ClientError
from lib.tools.custom_waiter import CustomWaiter, WaitState
import requests
import sys

sys.path.append('../')
logger = logging.getLogger(__name__)

class TranscribeCompleteWaiter(CustomWaiter):
	def __init__(self, client):
		super().__init__(
			'TranscribeComplete',
			'GetTranscriptionJob',
			'TranscriptionJob.TranscriptionJobStatus',
			{'COMPLETED': WaitState.SUCCESS, 'FAILED': WaitState.FAILURE},
			client)

	def wait(self, job_name):
		self._wait(TranscriptionJobName=job_name)

def start_job(job_name, media_uri, media_format, language_code, transcribe_client, vocabulary_name=None):
	"""
	Starts a transcription job. This function returns as soon as the job is started.
	To get the current status of the job, call get_transcription_job. The job is
	successfully completed when the job status is 'COMPLETED'.

	:param job_name: The name of the transcription job. This must be unique for your AWS account.
	:param media_uri: The URI where the audio file is stored. This is typically in an Amazon S3 bucket.
	:param media_format: The format of the audio file. For example, mp3 or wav.
	:param language_code: The language code of the audio file. For example, en-US or ja-JP
	:param transcribe_client: The Boto3 Transcribe client.
	:param vocabulary_name: The name of a custom vocabulary to use when transcribing the audio file.
	:return: Data about the job.
	"""
	try:
		job_args = {
			'TranscriptionJobName': job_name,
			'Media': {'MediaFileUri': media_uri},
			'MediaFormat': media_format,
			'LanguageCode': language_code}
		if vocabulary_name is not None:
			job_args['Settings'] = {'VocabularyName': vocabulary_name}
		response = transcribe_client.start_transcription_job(**job_args)
		job = response['TranscriptionJob']
		logger.info("Started transcription job %s.", job_name)
	except ClientError:
		logger.exception("Couldn't start transcription job %s.", job_name)
		raise
	else:
		return job

def get_job(job_name, transcribe_client):
	"""
	Gets details about a transcription job.

	:param job_name: The name of the job to retrieve.
	:param transcribe_client: The Boto3 Transcribe client.
	:return: The retrieved transcription job.
	"""
	try:
		response = transcribe_client.get_transcription_job(
			TranscriptionJobName=job_name)
		job = response['TranscriptionJob']
		logger.info("Got job %s.", job['TranscriptionJobName'])
	except ClientError:
		logger.exception("Couldn't get job %s.", job_name)
		raise
	else:
		return job

def delete_job(job_name, transcribe_client):
	"""
	Deletes a transcription job. This also deletes the transcript associated with
	the job.

	:param job_name: The name of the job to delete.
	:param transcribe_client: The Boto3 Transcribe client.
	"""
	try:
		transcribe_client.delete_transcription_job(
			TranscriptionJobName=job_name)
		logger.info("Deleted job %s.", job_name)
	except ClientError:
		logger.exception("Couldn't delete job %s.", job_name)
		raise

def transcribe(media_file_name, media_object_key):
	logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

	s3_resource = boto3.resource('s3')
	transcribe_client = boto3.client('transcribe')

	print("Welcome to the Amazon Transcribe!")
	print('-' * 100)

	bucket_name = f'el-analista-bucket-{time_ns()}'
	print(f"Creating bucket {bucket_name} in {transcribe_client.meta.region_name} region.")
	bucket = s3_resource.create_bucket(
		Bucket = bucket_name,
		CreateBucketConfiguration = {
			'LocationConstraint': transcribe_client.meta.region_name})

	print(f"Uploading media file {media_file_name}.")
	bucket.upload_file(media_file_name, media_object_key)
	media_uri = f's3://{bucket.name}/{media_object_key}'

	job_name_simple = f'el-analista-{time_ns()}'
	print(f"Starting transcription job {job_name_simple}.")
	start_job(
		job_name_simple,
		f's3://{bucket.name}/{media_object_key}',
		media_object_key[media_object_key.rfind('.')+1:],
		'es-ES',
		transcribe_client)
	transcribe_waiter = TranscribeCompleteWaiter(transcribe_client)
	transcribe_waiter.wait(job_name_simple)
	job_simple = get_job(job_name_simple, transcribe_client)
	transcript_simple = requests.get(
		job_simple['Transcript']['TranscriptFileUri']).json()

	print('-'*88)
	print("Deleting jobs.")
	for job_name in [job_name_simple]:
		delete_job(job_name, transcribe_client)

	print("Deleting bucket.")
	bucket.objects.delete()
	bucket.delete()

	return transcript_simple['results']['transcripts'][0]['transcript']