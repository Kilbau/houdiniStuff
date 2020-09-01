"""
When creating a node gamble instead.
If lucky you might get a nice node like an attribute wrangle.
"""
import random
import json
import os

try:
	import hou
except:
	pass

def create_json(filename):
	"""
	write contents and odds as a json file
	"""
	contents = {
				"common": ["convert", "convertvdb", "vdbfrompolygons", "mountain::2.0", "matchsize", "switch", "polybevel::3.0"],
				"uncommon": ["copytopoints::2.0", "scatter::2.0", "groupcreate", "copyxform", "blast"],
				"rare": ["null", "merge", "xform"],
				"legendary": ["attribwrangle", "attribvop"]
				}

	odds = {
			"common": 0.5,
			"uncommon": 0.3,
			"rare": 0.15,
			"legendary": 0.05
			}

	lootbox = {
		"odds": odds,
		"contents": contents
		}

	with open(filename, "w") as f:
		json.dump(lootbox, f, indent=2)

def get_lootbox_json(filename):
	"""
	read json contents
	"""
	with open(filename) as f:
		lootbox = json.load(f)

	return lootbox
	# print(lootbox["odds"]["legendary"])
	# print(lootbox["contents"]["legendary"][0])

def create_content_nodes(lootbox):
	""" HOUDINI
	for each node in the json create a node inside the lootbox hda to display the different prices.
	"""
	pass

def open_lootbox(reward):
	""" HOUDINI
	creates the rewarded node.
	Maybe some animations play.
	update the icon of the lootbox hda and delete key.
	"""
	parent = "/obj/geo1" # TODO change to the current path of node["kwargs"]
	reward_node = parent.createNode(reward)
	reward_node.moveToGoodPosition #TODO move below lootbox

	node["kwargs"].setUserData("nodeshape", "boxOpen")

	key_node = hou.node(node["kwargs"].inputs()[0])
	key_node.detroy()

def get_reward(lootbox):
	"""
	get a random reward from the lootbox json.
	Different reward classes have different probabilities.
	Each node inside a reward class has the same probability to be chosen.
	"""
	lootbox_class = list(lootbox["odds"].keys())
	lootbox_odds = tuple(lootbox["odds"].values())

	# print(lootbox_class)
	# print(lootbox_odds)
	reward_class, *_ = random.choices(lootbox_class, lootbox_odds)
	print(reward_class)

	reward_node = random.choice(lootbox["contents"][reward_class])
	print(reward_node)

	return reward_node

def test_houdini():
	# import sys
	# sys.path.append("D:/Projects/houdiniStuff/surprise_mechanics")
	# import surprise_mechanics as sm
	# sm.test_houdini()

	print("test is working")

if __name__ == "__main__":
	filename = "lootbox.json"
	if os.path.isfile(filename) == False:
		create_json(filename)
	
	lootbox = get_lootbox_json(filename)
	get_reward(lootbox)
