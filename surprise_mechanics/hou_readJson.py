# extra parameters
# file: file: filepath to json to json
# float: pos_mult: multiplier of postion
# int: endframe: $RFEND
# int: openframe: frame on which to create the reward

import hou
import json

node = hou.pwd()
lootbox = node.node("../")

parent = hou.node("/obj/geo1/")

orig_pos = tuple(lootbox.position())

with open(node.parm("file").eval()) as f:
    data = json.load(f)

frame = int(hou.frame())

for id in data.keys():
    name = "null_"+str(id)
    
    null = hou.node("/obj/geo1/"+name)
    if null == None:
        null = parent.createNode("null", name)
    
    try:
        pos = tuple(data[str(id)][str(frame)])
        
        pos_scale =  node.parm("pos_mult").eval()
        pos = pos[0] * pos_scale, pos[1] * pos_scale
        pos = (pos[0] + orig_pos[0], pos[1] + orig_pos[1])
        
        color = tuple(data[str(id)]["color_"+str(frame)])
        if color[0] == -1:
            # set to color matching to rarity
            # read from json
            color = node.parmTuple("test_color").eval()
        
        null.setColor(hou.Color(color))
        null.setPosition(pos)
        
    except KeyError:
        null.setPosition((-100,0))
        pass
        
if frame == node.parm("openframe").eval():
    reward_name = node.node("../").parm("reward").eval()
    reward_pos = node.node("../").parmTuple("reward_pos").eval()
    reward_col = node.node("../").parmTuple("color").eval()
    
    reward_node = parent.createNode(reward_name)
    reward_node.setPosition(reward_pos)
    reward_node.setColor(hou.Color(reward_col))
        
if frame == node.parm("endframe").eval():
    hou.playbar.stop()
    node.node("../").bypass(1)
    hou.setFrame(1)