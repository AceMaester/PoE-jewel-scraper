#Imports
from bs4 import BeautifulSoup
import urllib.request

mod_list={}
#incinerater
#spell dam, fire dam, life, spell dam + shield, cast speed +shield
URL_LIST=["moinimooginuta", "hositetatusono", "kaoritawatuoma", "ikokanihabaite", "tonotokokobako"]
MOD_WEIGHT_FILE = "incinerate_weights.txt"

# #phys wander
# #phys dam, wand phys, wand as, life, area dam
# URL_LIST=["inakimohonagok", "anikuniniyumiy", "hinonikikomkey", "kaoritawatuoma", "rikosahiwonira"]
# MOD_WEIGHT_FILE = "phys_wander_weights.txt"

SCORE_THRESHOLD = 35

class Item:
	def __init__(self, name, seller, price):
		self.name = name
		self.seller = seller
		self.price = price
		self.mods =[]
		self.score = 0
		
	def print(self):
		#return "name: " + str(self.name) + " seller: " + str(self.seller) + " price: " + str(self.price) + " mod score: " + str(self.score)
		if self.price == "":		
			return str(self.name) + ", " + str(self.seller) + ", no price, " + str(self.score)
		else:
			return str(self.name) + ", " + str(self.seller) + ", " + str(self.price) + ", " + str(self.score)
		
	def add_mod(self, name, value):
		self.mods.append(( name,value))
	
	def calculate_score(self):
		global mod_list
		self.score = 0
		for mod in self.mods:
			mod_score = float(mod_list[mod[0]])*float(mod[1])
			self.score += mod_score
		self.score = round(self.score, 2)
		return self.score
	
	def print_mods(self):
		for mod in self.mods:
			print("\t",mod[0]," ",mod[1])


#Read and parse the standard input 
def load_input():
	input_file = open(MOD_WEIGHT_FILE, 'r')
	
	has_line = True
	global mod_list
	
	while has_line:
		mod = input_file.readline().strip().split(",")
		if mod[0] == "0":
			has_line = False
			break
		
		mod_list[mod[0]] = float(mod[1])
		
	input_file.close()

load_input()
for url in URL_LIST:
	print(url, flush=True)
	with urllib.request.urlopen("http://poe.trade/search/" + url) as response:
	   html = response.read() 
	soup = BeautifulSoup(html, "html.parser")

	item_list = []
	for tag in soup.find_all("tbody"):
		item = Item(tag["data-name"], tag["data-ign"], tag["data-buyout"])
		item_list.append(item)
		for mod in tag.find_all(class_="mods"):
			for li in mod('li'):
				mod_name = li["data-name"]
				mod_value = li["data-value"]
				if mod_name[0] != "$":
					item.add_mod(mod_name, mod_value)
		item.calculate_score()

		
	item_list.sort(key=lambda x: x.score, reverse=True)
	#print score if it is greater than the score-threshold
	for item in item_list:
		if item.score >= SCORE_THRESHOLD:
			print(item.print(), flush=True)
			item.print_mods()
	print()
			
