# import urllib.request
# # from config import Config
#
# # class YutubeApi:
# #
# #     def __init__(self, youtube_url=Config.YOUTUBE_UPLOAD):
# #         self.youtube_url = youtube_url
# #
# #     def upload(self, header=None, file_info=None, file=None):
# #         print(headers['Content-Type'])
# #         print(headers['Content-Type'])
# #         print(header)
# #         req = urllib.request.Request(self.youtube_url, method='POST', headers={
# #             'authorization': 'client_secrets.json',
# #             'host': 'www.googleapis.com',
#             # 'content-length': header['Content-Length'],
#             # 'content-range': '0-{0}/{1}'.format(file_info['chunkSize'], file_info['totalSize']),
#             # 'content-type': 'application/json; charset=UTF-8'
#             # 'Content-Type': 'video/*'
#         # })
#         # response = urllib.request.urlopen(req)
#
# # import urllib.error
# # import httplib2
# # import os
# # import random
# # import sys
# # import time
# # from apiclient.discovery import build
# # from apiclient.errors import HttpError
# # from apiclient.http import MediaFileUpload
# # from oauth2client.client import flow_from_clientsecrets
# # from oauth2client.file import Storage
# # from oauth2client.tools import argparser, run_flow
# #
# # class YoutubeApi:
# #
# #     def __init__(self, max_retries=1, retriable_status_codes=(500, 502, 503, 504),
# #                  youtube_url=Config.YOUTUBE_UPLOAD):
# #
# #         httplib2.RETRIES = 1
# #         self.max_retries = max_retries
# #         self.retriable_status_codes = retriable_status_codes
# #         self.client_secrets_file = Config.CLIENT_SECRETS_FILE
# #         self.missing_client_secrets_message = Config.MISSING_CLIENT_SECRETS_MESSAGE
# #         self.youtube_api_version = Config.YOUTUBE_API_VERSION
# #         self.youtube_api_service_name = Config.YOUTUBE_API_SERVICE_NAME
# #         self.youtube_url = youtube_url
# #
# #     VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")
# #
# #     def get_authenticated_service(self, args=None):
# #         flow = flow_from_clientsecrets(self.client_secrets_file, scope=self.youtube_url,
# #                                        message=self.missing_client_secrets_message)
# #         storage = Storage("%s-oauth2.json" % sys.argv[0])
# #         credentials = storage.get()
# #         if credentials is None or credentials.invalid:
# #             credentials = run_flow(flow, storage, args)
# #
# #         return build(self.youtube_api_service_name, self.youtube_api_version,
# #                      http=credentials.authorize(httplib2.Http()))
# #
# #     def initialize_upload(self, youtube, options):
# #         tags = None
# #         if options['--keywords']:
# #             tags = options.keywords.split(",")
# #
# #         body=dict(
# #                   snippet=dict(
# #                                title=options['--title'],
# #                                description=options['--description'],
# #                                tags=['--tags'],
# #                                categoryId=options['--category']
# #                                  ),
# #                   status=dict(
# #                   privacyStatus=options['--privacyStatus']
# #                    )
# #                      )
# #         insert_request = youtube.videos().insert(
# #         part=options.keys(),
# #         body=body,
# #         media_body=MediaFileUpload(options['--file'], chunksize=-1, resumable=True)
# #         )
# #         self.resumable_upload(insert_request)
# #
# #     def resumable_upload(self, insert_request):
# #         response = None
# #         error = None
# #         retry = 0
# #         while response is None:
# #             try:
# #                 print ("Uploading file...")
# #                 status, response = insert_request.next_chunk()
# #                 if 'id' in response:
# #                     print ("Video id '%s' was successfully uploaded." % response['id'])
# #                 else:
# #                     exit("The upload failed with an unexpected response: %s" % response)
# #             except HttpError as e:
# #                  if e.resp.status in e:
# #                      error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
# #                                                              e.content)
# #                  else:
# #                      raise
# #             except self.retriable_status_codes as e:
# #                  error = "A retriable error occurred: %s" % e
# #
# #         if error is not None:
# #             print (error)
# #             retry += 1
# #             if retry > self.max_retries:
# #                 exit("No longer attempting to retry.")
# #
# #             max_sleep = 2 ** retry
# #             sleep_seconds = random.random() * max_sleep
# #             print ("Sleeping %f seconds and then retrying..." % sleep_seconds)
# #             time.sleep(sleep_seconds)
# #
# #     def run(self, request):
# #
# #         print(request.files['file'].stream.read(-1))
# #         args = {'--file': request.files['file'].stream.read(-1),
# #                 '--title': 'some text',
# #                 "--description": "Test Description",
# #                 '--category': '22',
# #                 "--keywords": 'some',
# #                 '--privacyStatus': 'public',
# #                 }
# #         youtube = self.get_authenticated_service(args)
# #
# #         self.initialize_upload(youtube, args)#
# import httplib2
# from apiclient.discovery import build
# from config import Config
# import os
# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.file import Storage
# from oauth2client.tools import argparser, run_flow
# import sys
# import urllib.request as r
# from urllib.parse import urlencode
# from oauth2client import client
# from flask import url_for, redirect
#
#
# class YoutubeApi:
#     def __init__(self):
#
#         self.client_email = '664683051441-2hdt6etj4v6k2hqr11lj1u5p09gds617@developer.gserviceaccount.com'
#         # self.youtube = build(Config.YOUTUBE_API_SERVICE_NAME, Config.YOUTUBE_API_VERSION,
#         #                      developerKey=Config.SECRET_KEY)
#         # with open("/home/viktor/profireader/service_key.json") as f:
#         #     self.private_key = f.read()
#         # self.credentials = AppAssertionCredentials(Config.YOUTUBE_UPLOAD)
#
#     @staticmethod
#     def get_authenticated_service(args):
#
#         response = urllib.request.urlopen('https://accounts.google.com/o/oauth2/token')
#         # flow = flow_from_clientsecrets(Config.CLIENT_SECRETS_FILE,
#         # scope=Config.YOUTUBE_UPLOAD,
#         # message=Config.MISSING_CLIENT_SECRETS_MESSAGE)
#         # storage = Storage("%s-oauth2.json" % sys.argv[0])
#         # credentials = storage.get()
#         #
#         # if credentials is None or credentials.invalid:
#         #     credentials = run_flow(flow, storage, args)
#         #     return build(Config.YOUTUBE_API_SERVICE_NAME, Config.YOUTUBE_API_VERSION,
#         #                  http=credentials.authorize(httplib2.Http()))
#     def p(self):
#
#          flow = client.flow_from_clientsecrets(Config.CLIENT_SECRETS_FILE,
#          scope=Config.YOUTUBE_UPLOAD, redirect_uri=url_for())
#          auth_code = flow.step1_get_authorize_url()
#          credentials = flow.step2_exchange(auth_code)
#          http_auth = credentials.authorize(httplib2.Http())
#          print(http_auth)
#
#
#         # url = "https://accounts.google.com/o/oauth2/token"
#         # headers = {'content-type': 'application/x-www-form-urlencoded'}
#         #
#         # data = {'code': '4/ux5gNj-_asasasmIu4DOD_gNZdjX9EtOFf',
#         #         'client_id': '664683051441-ur16e99ckrinb667sqetm9cnm09ku3c0.apps.googleusercontent.com',
#         #         'client_secret': 'sGbR8eaMPMsLSlXAu5u-NgG9',
#         #         'redirect_uri': 'http://aprofi.d.ntaxa.com/filemanager/send/',
#         #         'grant_type': 'authorization_code'}
#         # data = urlencode(data).encode('utf-8')
#         # url = 'https://accounts.google.com/o/oauth2/token?' \
#         #       'client_id=664683051441-ur16e99ckrinb667sqetm9cnm09ku3c0.apps.googleusercontent.com&' \
#         #       'redirect_uri=http://aprofi.d.ntaxa.com/filemanager/send/&' \
#         #       'scope=https://www.googleapis.com/auth' \
#         #       'response_type=4/ux5gNj-_mIu4DOD_gNZdjX9EtOFf&access_type=offline&'
#         # req = urllib.request.Request(url, headers=headers, data=data, method='POST')
#         # f = urllib.request.urlopen(req)
#         # print(f)
#         # argparser.add_argument("--auth_host_name", default='http://aprofi.d.ntaxa.com')
#         # argparser.add_argument("--file", default=('{0}/avro.pm4', os.getcwd()), help=False)
#         # argparser.add_argument("--title", help="Video title", default="Test Title")
#         # argparser.add_argument("--description", help="Video description",
#         # default="Test Description")
#         # argparser.add_argument("--category", default="22",
#         # help="Numeric video category. " +
#         # "See https://developers.google.com/youtube/v3/docs/videoCategories/list")
#         # argparser.add_argument("--keywords", help="Video keywords, comma separated",
#         # default="")
#         # argparser.add_argument("--privacyStatus", choices=['private'],
#         # default='public', help="Video privacy status.")
#         # args = argparser.parse_args()
#         # self.get_authenticated_service(args)
#     #     http_auth = self.credentials.authorize(Http())
#     #     youtube = build(Config.YOUTUBE_API_SERVICE_NAME, Config.YOUTUBE_API_VERSION, http=http_auth)
#     #     response = youtube.videos().list(id='QC46Zc1ijtI').execute()
#     #     print(response)
#     #     print(os.getcwd())
#         # self.youtube.videos().insert(
#         #     part='id',
#         #     body=dict(snippet=dict(title='yyy',
#         #                            description='new file',
#         #                            tags=["cool", "video", "more keywords"],
#         #                            categoryId='22'),
#         #               status=dict(
#         #               privacyStatus='public')),
#         #     media_body=MediaFileUpload('/home/viktor/Downloads/avro.mp4',
#         #                                chunksize=-1, resumable=True)).execute(self.http)
#         # video = self.youtube.videos().list(id='cHBAj2SIg9E', part='id').execute(self.http)
#         # print(video)

from apiclient import discovery
from config import Config
import httplib2
from flask import session, jsonify, url_for, redirect, request
from apiclient.http import MediaFileUpload
from oauth2client import client
from urllib import request as req

class GoogleAuthorize(object):
    """ This class can apply api_service name and api_version to build service which you want.
     Default youtube upload service. Method authorize return service with necessary token
     server-server . If you need to get token, use flask.session['credentials'] """

    __developer_key = Config.GOOGLE_API_SECRET_KEY
    __project_secret = Config.GOOGLE_API_SECRET_JSON

    def __init__(self, google_service_name=Config.YOUTUBE_API_SERVICE_NAME,
                 google_service_version=Config.YOUTUBE_API_VERSION,
                 scope=Config.YOUTUBE_SCOPES['UPLOAD']):
        self.google_service_name = google_service_name
        self.google_service_version = google_service_version
        self.scope = scope

    def get_auth_code(self):

        flow = client.flow_from_clientsecrets(self.__project_secret, self.scope,
                                              redirect_uri=Config.YOUTUBE_REDIRECT_URL)
        auth_uri = flow.step1_get_authorize_url()
        request_for_token = req.urlopen(auth_uri)
        url = request_for_token.geturl()
        return url

    def authorize(self):

        flow = client.flow_from_clientsecrets(self.__project_secret, self.scope,
                                              redirect_uri=Config.YOUTUBE_REDIRECT_URL)
        credentials = flow.step2_exchange(session['auth_code'])
        http = httplib2.Http()
        http = credentials.authorize(http)
        return http

    def service_build(self):
        http = self.authorize()
        service = discovery.build(self.google_service_name, self.google_service_version,
                                  http=http)
        return service

class YoutubeApi(GoogleAuthorize):
    """ Use this class for upload videos, get videos, create channels. Body should be dict like this:
        {
         "title": "My video title",
         "description": "This is a description of my video",
         "tags": ["profireader", "video", "more keywords"],
         "categoryId": 22
         "status": "public"
         }
         Optional you can upload videos via chunks.
         If you would, pass chunk info (dict) to constructor like:
         chunk_size = 20000 (in bytes), chunk_number = 1, total_size = 1000000
         Requirements : parts = 'snippet' .Pass to this what would you like to return from
          youtube server. (id, snippet, status, contentDetails, fileDetails, player,
          processingDetails, recordingDetails, statistics, suggestions, topicDetails)"""

    def __init__(self, parts, video_file=None, body_dict=None, chunk_info=None):
        super(YoutubeApi, self).__init__()
        self.video_file = video_file
        self.body_dict = body_dict
        self.chunk_info = chunk_info
        self.resumable = True if self.chunk_info else False
        self.parts = parts
        self.youtube = self.service_build()

    def make_body(self):
        """ make body to create request. category_id default 22, status default 'public'. """

        body = {"snippet": {"title": self.body_dict.get('title') or '',
                            "description": self.body_dict.get('description') or '',
                            "tags": self.body_dict.get('tags'),
                            "categoryId": self.body_dict.get('category_id') or 22
                            },
                "status": {"privacyStatus": self.body_dict.get('status') or 'public',
                           "embeddable": True,
                           "license": "youtube"
                           }
                }
        return body

    def upload(self):

        upload_video = self.youtube.videos().insert(part=self.parts,
                                                    body=self.make_body(),
                                                    media_body=self.video_file).execute()

