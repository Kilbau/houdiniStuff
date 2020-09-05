"""
When creating a node gamble instead.
If lucky you might get a nice node like an attribute wrangle.
"""
import random
import json
import os
import time

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

	colors = {
			"common": (1, 1, 1), # grey
			"uncommon": (0, 0.75, 1.5), # blue
			"rare": (0.85, 0, 1.7), # purple
			"legendary": (1.9, 1.6, 0) # yellow
			}

	lootbox = {
		"odds": odds,
		"contents": contents,
		"colors": colors
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
	for each node in the json 
	create a node inside the lootbox hda to display the different prices.
	"""
	pass

def bias_rewards(contents, odds):
	"""
	return a biased list to be used with the random.choice method
	workaround because python 2.x doesnt have a random.choices method
	"""
	zipped = zip(contents, odds)
	lst = [[i[0]] * int(i[1]*100) for i in zipped]
	new = [b for i in lst for b in i]
	return new


def get_reward(node, lootbox):
	"""
	get a random reward from the lootbox json.
	Different reward classes have different probabilities.
	Each node inside a reward class has the same probability to be chosen.
	"""
	lootbox_class = list(lootbox["odds"].keys())
	# lootbox_odds = tuple(lootbox["odds"].values()) #for random.choices
	lootbox_odds = list(lootbox["odds"].values())

	# print(lootbox_class)
	# print(lootbox_odds)
	# reward_class, *_ = random.choices(lootbox_class, lootbox_odds) # 3.x
	
	# reward_class = "uncommon"

	biased_rewards = bias_rewards(lootbox_class, lootbox_odds) # 2.x
	reward_class = random.choice(biased_rewards) # 2.x
	# print(reward_class)

	reward_node = random.choice(lootbox["contents"][reward_class])
	# print(reward_node)

	# set the reward color parm
	reward_color = lootbox["colors"][reward_class]
	node.parmTuple("color").set(reward_color)

	return reward_node

def get_key(node):
	"""HOUDINI
	returns the key that is connected to the hda
	if not found return None
	"""
	try:
		key_node = node.inputs()[0]
		return key_node
	except:
		return None

def play_animation():
	"""
	plays opening animation
	"""
	hou.setFrame(1)
	hou.playbar.play()


def test_houdini():
	# import sys
	# sys.path.append("D:/Projects/houdiniStuff/surprise_mechanics")
	# import surprise_mechanics as sm
	# sm.test_houdini()

	# requries commeting of random.choices() line else it throws errors in H

	print("test is not working")

def open_lootbox(node, reward):
	""" HOUDINI
	creates the rewarded node.
	Maybe some animations play.
	update the icon of the lootbox hda and delete key.
	"""

	# get postion for reward node under HDA
	node_pos = list(node.position())
	node_pos[1] -= 1
	node_pos = tuple(node_pos)

	# creates reward node
	# parent = node.node("../")
	# reward_node = parent.createNode(reward)
	# reward_node.setPosition(node_pos)

	# set reward parameter
	node.parmTuple("reward_pos").set(node_pos)
	node.parm("reward").set(reward)

	# sets shape of hda to open
	node.setUserData("nodeshape", "boxOpen")

def main(kwargs):
	""" HOUDINI
	just call this function in houdini to open a chest
	"""
	node = kwargs["node"]

	node.setDisplayFlag(1)
	node.setRenderFlag(1)

	key_node = get_key(node)
	try:
		key_node.destroy()
	
	except:
		print("No Key found")

	else:
		filename = node.parm("lootboxContents").eval()
		lootbox = get_lootbox_json(filename)

		reward = get_reward(node, lootbox)

		play_animation()
		open_lootbox(node, reward)



# if __name__ == "__main__":
# 	filename = "lootbox.json"
# # 	if os.path.isfile(filename) == False:
# # 		create_json(filename)
	
# 	lootbox = get_lootbox_json(filename)
# 	get_reward(None, lootbox)
