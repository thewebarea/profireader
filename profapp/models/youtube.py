import urllib.request
# from config import Config

# class YutubeApi:
#
#     def __init__(self, youtube_url=Config.YOUTUBE_UPLOAD):
#         self.youtube_url = youtube_url
#
#     def upload(self, header=None, file_info=None, file=None):
#         print(headers['Content-Type'])
#         print(headers['Content-Type'])
#         print(header)
#         req = urllib.request.Request(self.youtube_url, method='POST', headers={
#             'authorization': 'client_secrets.json',
#             'host': 'www.googleapis.com',
            # 'content-length': header['Content-Length'],
            # 'content-range': '0-{0}/{1}'.format(file_info['chunkSize'], file_info['totalSize']),
            # 'content-type': 'application/json; charset=UTF-8'
            # 'Content-Type': 'video/*'
        # })
        # response = urllib.request.urlopen(req)

# import urllib.error
# import httplib2
# import os
# import random
# import sys
# import time
# from apiclient.discovery import build
# from apiclient.errors import HttpError
# from apiclient.http import MediaFileUpload
# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.file import Storage
# from oauth2client.tools import argparser, run_flow
#
# class YoutubeApi:
#
#     def __init__(self, max_retries=1, retriable_status_codes=(500, 502, 503, 504),
#                  youtube_url=Config.YOUTUBE_UPLOAD):
#
#         httplib2.RETRIES = 1
#         self.max_retries = max_retries
#         self.retriable_status_codes = retriable_status_codes
#         self.client_secrets_file = Config.CLIENT_SECRETS_FILE
#         self.missing_client_secrets_message = Config.MISSING_CLIENT_SECRETS_MESSAGE
#         self.youtube_api_version = Config.YOUTUBE_API_VERSION
#         self.youtube_api_service_name = Config.YOUTUBE_API_SERVICE_NAME
#         self.youtube_url = youtube_url
#
#     VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")
#
#     def get_authenticated_service(self, args=None):
#         flow = flow_from_clientsecrets(self.client_secrets_file, scope=self.youtube_url,
#                                        message=self.missing_client_secrets_message)
#         storage = Storage("%s-oauth2.json" % sys.argv[0])
#         credentials = storage.get()
#         if credentials is None or credentials.invalid:
#             credentials = run_flow(flow, storage, args)
#
#         return build(self.youtube_api_service_name, self.youtube_api_version,
#                      http=credentials.authorize(httplib2.Http()))
#
#     def initialize_upload(self, youtube, options):
#         tags = None
#         if options['--keywords']:
#             tags = options.keywords.split(",")
#
#         body=dict(
#                   snippet=dict(
#                                title=options['--title'],
#                                description=options['--description'],
#                                tags=['--tags'],
#                                categoryId=options['--category']
#                                  ),
#                   status=dict(
#                   privacyStatus=options['--privacyStatus']
#                    )
#                      )
#         insert_request = youtube.videos().insert(
#         part=options.keys(),
#         body=body,
#         media_body=MediaFileUpload(options['--file'], chunksize=-1, resumable=True)
#         )
#         self.resumable_upload(insert_request)
#
#     def resumable_upload(self, insert_request):
#         response = None
#         error = None
#         retry = 0
#         while response is None:
#             try:
#                 print ("Uploading file...")
#                 status, response = insert_request.next_chunk()
#                 if 'id' in response:
#                     print ("Video id '%s' was successfully uploaded." % response['id'])
#                 else:
#                     exit("The upload failed with an unexpected response: %s" % response)
#             except HttpError as e:
#                  if e.resp.status in e:
#                      error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
#                                                              e.content)
#                  else:
#                      raise
#             except self.retriable_status_codes as e:
#                  error = "A retriable error occurred: %s" % e
#
#         if error is not None:
#             print (error)
#             retry += 1
#             if retry > self.max_retries:
#                 exit("No longer attempting to retry.")
#
#             max_sleep = 2 ** retry
#             sleep_seconds = random.random() * max_sleep
#             print ("Sleeping %f seconds and then retrying..." % sleep_seconds)
#             time.sleep(sleep_seconds)
#
#     def run(self, request):
#
#         print(request.files['file'].stream.read(-1))
#         args = {'--file': request.files['file'].stream.read(-1),
#                 '--title': 'some text',
#                 "--description": "Test Description",
#                 '--category': '22',
#                 "--keywords": 'some',
#                 '--privacyStatus': 'public',
#                 }
#         youtube = self.get_authenticated_service(args)
#
#         self.initialize_upload(youtube, args)#
import httplib2
from oauth2client import gce
from apiclient.discovery import build
from config import Config
from apiclient.http import MediaFileUpload
import os

class YoutubeApi:
    def __init__(self):
        self.credentials = gce.AppAssertionCredentials(
            scope='https://www.googleapis.com/auth/devstorage.read_write')
        self.http = self.credentials.authorize(httplib2.Http())
        self.youtube = build(Config.YOUTUBE_API_SERVICE_NAME, Config.YOUTUBE_API_VERSION,
                             developerKey=Config.SECRET_KEY)

    def p(self, request):

        print(os.getcwd())
        self.youtube.videos().insert(
            part='id',
            body=dict(snippet=dict(title='yyy',
                                   description='new file',
                                   tags=["cool", "video", "more keywords"],
                                   categoryId='22'),
                      status=dict(
                      privacyStatus='public')),
            media_body=MediaFileUpload('/home/viktor/Downloads/avro.mp4',
                                       chunksize=-1, resumable=True)).execute(self.http)
        # video = self.youtube.videos().list(id='cHBAj2SIg9E', part='id').execute(self.http)
        # print(video)
