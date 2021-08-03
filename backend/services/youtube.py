import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
 

class YoutubeApi:
    youtube_service = None
    authenticated = False

    @staticmethod
    def authenticate():
        if YoutubeApi.authenticated:
            return

        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = os.environ["YOUTUBE_CLIENT_CREDS_FILENAME"]

        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        YoutubeApi.youtube_service = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
        YoutubeApi.authenticated = True

    @staticmethod
    def get_playlist_info(playlist_id):
        request_args = {
            'part': 'contentDetails, id, snippet',
            'id': playlist_id,
        }
        request = YoutubeApi.youtube_service.playlists().list(**request_args)
        response = request.execute()

        return response

    @staticmethod
    def get_playlist_items(playlist_id, page_token=None):
        request_args = {
            'part': 'contentDetails, id, snippet',
            'playlistId': playlist_id,
            'maxResults': 50,
        }
        if page_token:
            request_args['pageToken'] = page_token

        request = YoutubeApi.youtube_service.playlistItems().list(**request_args)
        response = request.execute()
        
        return response

    @staticmethod
    def get_full_playlist_items(playlist_id):
        items = []
        first_page = YoutubeApi.get_playlist_items(playlist_id)
        print(first_page)
        items.extend(first_page['items'])

        next_page_token = first_page.get('nextPageToken')
        while next_page_token:
            next_page = YoutubeApi.get_playlist_items(playlist_id, next_page_token)
            items.extend(next_page['items'])
            next_page_token = next_page.get('nextPageToken')
            print(len(items))

        return items

    
