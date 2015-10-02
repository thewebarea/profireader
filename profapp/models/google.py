from apiclient import discovery
from config import Config
import httplib2
from flask import session, jsonify, url_for, redirect, request
from apiclient.http import MediaFileUpload, MediaInMemoryUpload, MediaUpload, MediaIoBaseUpload
from oauth2client import client
from oauth2client.client import Credentials
from urllib import request as req

from urllib import parse
from ..constants.TABLE_TYPES import TABLE_TYPES
from sqlalchemy import Column
from .pr_base import Base, PRBase
from flask import g
from utils.db_utils import db
from urllib.error import HTTPError as errors
import io
from apiclient.errors import HttpError
import requests
import sys
import json
from ..controllers.errors import TooManyCredentialsInDb

class GoogleToken(Base, PRBase):
    __tablename__ = 'google_token'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    credentials = Column(TABLE_TYPES['credentials'], nullable=False)

    def __init__(self, credentials=None):
        super(GoogleToken, self).__init__()
        self.credentials = credentials

    @staticmethod
    def check_credentials_exist():
        """ Method check rather credentials is exist in db. Can be only one credentials in db.
         If None you should to redirect admin to google auth page.
         If >1 some think is wrong . Raise exception"""
        try:
            credentials = db(GoogleToken).count()
            if credentials < 2:
                return credentials
            else:
                raise TooManyCredentialsInDb({'message': 'credentials >1'})
        except TooManyCredentialsInDb as e:
            e = e.args[0]
            print(e['message'])

    def save_credentials(self):
        """ This method save and return your credentials to/from db in json format.
         When you will need credentials you have to convert json to object(
         method: Credentials().new_from_json ) """
        google = GoogleAuthorize()
        flow = google.get_auth_code(ret_flow=True)
        credentials = flow.step2_exchange(session['auth_code'])
        self.credentials = credentials.to_json()
        self.save()
        return self.credentials

    @staticmethod
    def get_credentials_from_db():
        """ Static method. This method make query from db to get json-credentials, and
         then return object correct credentials which has been made from json.
          Set httplib2.debuglevel = 4 to debug http"""
        # httplib2.debuglevel = 4
        json = db(GoogleToken).first().credentials
        cred = Credentials()
        credentials = cred.new_from_json(json)
        http = httplib2.Http()
        http = credentials.authorize(http)
        credentials.refresh(http)
        session['access_token'] = credentials.access_token
        return credentials

    @staticmethod
    def get_authorize_http():
        """ Method which is helpful to get authorize http from your credentials.
         Can be used for make some service from google api"""
        json = db(GoogleToken).first().credentials
        cred = Credentials()
        credentials = cred.new_from_json(json)
        http = httplib2.Http()
        http = credentials.authorize(http)
        return http

class GoogleAuthorize(object):
    """ This class can apply api_service name and api_version to build service which you want.
     Default youtube upload service. Method authorize return service with necessary token
     server-server . If you need to get token, use flask.session['credentials'] """

    __project_secret = Config.GOOGLE_API_SECRET_JSON

    def __init__(self, google_service_name=Config.YOUTUBE_API_SERVICE_NAME,
                 google_service_version=Config.YOUTUBE_API_VERSION,
                 scope=Config.YOUTUBE_API['UPLOAD']['SCOPE'],
                 redirect_uri=Config.YOUTUBE_API['UPLOAD']['REDIRECT_URI']):
        self.google_service_name = google_service_name
        self.google_service_version = google_service_version
        self.scope = scope
        self.redirect_uri = redirect_uri

    def get_auth_code(self, ret_flow=False):

        """ This method return link for google auth service if ret_flow parameter is not produced,
        else - return flow object. Helpful when you need to have code to make credentials """
        flow = client.flow_from_clientsecrets(self.__project_secret, self.scope,
                                              redirect_uri=self.redirect_uri)
        flow.params['access_type'] = 'offline'
        flow.params['approval_prompt'] = 'force'
        auth_uri = flow.step1_get_authorize_url()
        request_for_token = req.urlopen(auth_uri)
        url = request_for_token.geturl()
        return url if not ret_flow else flow

    @staticmethod
    def check_admins():
        return True if session.get('user_id') in Config.PROFIREADER_ADMINS else False

    def service_build(self):
        """ This method is helpful when you want to use google_api_client.
            Return authorized service """
        http = GoogleToken.get_authorize_http()
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

    def __init__(self, parts=None, video_file=None, body_dict=None, chunk_info=None):
        super(YoutubeApi, self).__init__()
        self.video_file = video_file
        self.body_dict = body_dict
        self.chunk_info = chunk_info
        self.resumable = True if self.chunk_info else False
        self.parts = parts
        self.youtube = self.service_build()
        self.start_session = Config.YOUTUBE_API['UPLOAD']['SEND_URI']

    def make_body_for_start_upload(self):
        """ make body to create request. category_id default 22, status default 'public'. """

        body = dict(snippet=dict(
                    title=self.body_dict.get('title') or '',
                    description=self.body_dict.get('description') or '',
                    tags=self.body_dict.get('tags'),
                    categoryId=self.body_dict.get('category_id') or 22),
                    status=dict(
                    privacyStatus=self.body_dict.get('status') or 'public'))
        return body

    def make_headers_for_start_upload(self, content_length):

        headers = {'authorization': 'Bearer {0}'.format(
            GoogleToken.get_credentials_from_db().access_token),
            'content-type': 'application/json; charset=utf-8',
            'content-length': content_length,
            'x-upload-content-length': int(self.chunk_info.get('total_size')),
            'x-upload-content-type': 'application/octet-stream'}
        return headers

    def make_encoded_url(self, body_keys):
        values = parse.urlencode(dict(uploadType='resumable', part=",".join(body_keys)))
        url_encoded = self.start_session % values
        return url_encoded

    def set_youtube_service_url_to_session(self):

        body = self.make_body_for_start_upload()
        url = self.make_encoded_url(body.keys())
        body = json.dumps(body).encode('utf8')
        headers = self.make_headers_for_start_upload(sys.getsizeof(body))
        try:
            r = req.Request(url=url, headers=headers,  method='POST')
            response = req.urlopen(r, data=body)
            session['url'] = response.headers.get('Location')
        except errors as e:
            print(e.headers)
            print(e.code)

    def make_headers_for_upload(self):
        headers = {'authorization': 'Bearer {0}'.format(session.get('access_token')),
                   'content-type': 'application/octet-stream',
                   'content-length': int(self.chunk_info.get('chunk_size')),
                   'content-range': 'bytes 0-{0}/{1}'.format(int(self.chunk_info.get('chunk_size'))-1, self.chunk_info.get('total_size'))}
        return headers

    def check_upload_status(self):
        headers = {'authorization': 'Bearer {0}'.format(session.get('access_token')),
                   'content-range': 'bytes */{0}'.format(self.chunk_info.get('total_size')),
                   'content-length': 0}
        r = req.Request(url=session['url'], headers=headers,  method='PUT')
        try:
            response = req.urlopen(r)
            return response
        except errors as e:
            print(e.code)

    def upload(self):

        if int(self.chunk_info.get('chunk_number')) == 0:
            self.set_youtube_service_url_to_session()
        headers = self.make_headers_for_upload()
        try:
            r = req.Request(url=session['url'], headers=headers, method='PUT')
            response = req.urlopen(r, data=self.video_file,)
            print(response)
            return response
        except errors as e:
            if e.code == 308:
                r = req.Request(url=session['url'], headers=headers, method='PUT')
                response = req.urlopen(r, data=self.video_file,)
            print(e.headers)
            print(e.msg)
