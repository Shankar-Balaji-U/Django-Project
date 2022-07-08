import json, os, shutil
from django.conf import settings
from json.decoder import JSONDecodeError



STORAGE_PATH = os.path.join(settings.MEDIA_ROOT, "")
TEMP_STORAGE_PATH = os.path.join(STORAGE_PATH, ".temp")


class JsonStorage:
	TEMP_FILE = None
	JSON_FILE = None
	data = {}
	def read(self, key=None):
		if key == None:
			return self.data
		else:
			return self.data[key]

	def write(self, key, value):
	
		with open(self.JSON_FILE, "w") as cfile, open(self.TEMP_FILE, "w") as tfile:
			self.data[key] = value
			json.dump(self.data, cfile, sort_keys=True, ensure_ascii=False, indent=4)
			json.dump(self.data, tfile, sort_keys=True, ensure_ascii=False, indent=4)
	
	def clean(self):
		shutil.rmtree(STORAGE_PATH) 
		


	def __init__(self, filename):
		
		if not os.path.exists(STORAGE_PATH):
			os.makedirs(STORAGE_PATH)
	
		if not os.path.exists(TEMP_STORAGE_PATH):
			os.makedirs(TEMP_STORAGE_PATH)

		file_path = os.path.join(STORAGE_PATH, filename+'.json')
		temp_path = os.path.join(STORAGE_PATH, '.temp\\'+filename+'_temp.json')


		if os.path.exists(file_path):
			with open(file_path, "r") as cfile:
				try:
					curr_data = json.load(cfile)
					self.data = curr_data
				except JSONDecodeError:
					if os.path.exists(temp_path):
						with open(file_path, "w") as cfile, open(temp_path, "r") as tfile:
							try:
								temp_data = json.load(tfile)
								self.data = temp_data
								json.dump(temp_data, cfile, sort_keys=True, ensure_ascii=False, indent=4)

							except JSONDecodeError:
								pass
		else:
			if os.path.exists(temp_path):
				with open(file_path, "w+") as cfile, open(temp_path) as tfile:
					try:
						temp_data = json.load(tfile)
						self.data = temp_data
						json.dump(temp_data, cfile, sort_keys=True, ensure_ascii=False, indent=4)

					except JSONDecodeError:
						pass
			else:
				with open(temp_path, "w+") as _:
					pass








json_storage = JsonStorage("jso")
# json_storage.write("name", "Shankar Balaji")
# a = json_storage.read("name")
# print(a)
