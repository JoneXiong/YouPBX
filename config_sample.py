# coding=utf-8


fs_conf_path = '/usr/local/freeswitch/conf/'

odbc_credentials = "freepybx:freepybx:secretpass1"


event_socket_conf = {
                     'host': '127.0.0.1',
                     'port': 8021,
                     'pwd': 'ClueCon'
                     }
FS_AGW_URL = 'http://127.0.0.1:8121'


main_server_conf = {
    'host': '0.0.0.0',
    'port': 8080
}

ws_url = 'ws://127.0.0.1:8080/ws'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'data.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
