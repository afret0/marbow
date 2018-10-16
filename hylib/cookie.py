#-*- coding: utf-8 -*-

import sqlite3
import os
import win32crypt

def get_chrome_cookies(url):
	cookie_file_path = os.path.join(os.environ['LOCALAPPDATA'], r'Google\Chrome\User Data\Default\Cookies')

	conn = sqlite3.connect(cookie_file_path)

	ret_dict = {}
	for row in conn.execute("select host_key, name, path, value, encrypted_value from cookies"):
		if row[0] != url:
			continue
		ret = None
		ret = win32crypt.CryptUnprotectData(row[4], None, None, None, 0)

		ret_dict[row[1]] = ret[1]
	conn.close()

	return ret_dict
