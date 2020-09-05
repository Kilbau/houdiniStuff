# extra parameters
# file: json_out: filepath were to save json
# int: endframe: $RFEND
# int: num_points: maximum number of points
import hou
import json

node = hou.pwd()
geo = node.geometry()

frame = int(hou.frame())

if frame == 1:
    #pos_dict = {"0":{}, "1":{}, "2":{}}
    points = node.parm("num_points").eval()
    pos_dict = {str(i):{} for i in range(points)}
    print("reset")

for point in geo.points():
    x, y, _ =  point.attribValue("P")
    id = point.attribValue("id")
    try:
        cd = point.attribValue("Cd")
    except:
        cd = (1,1,1)
    try:
        pos_dict[str(id)].update({frame:(x,y)})
        pos_dict[str(id)].update({"color_"+str(frame):cd})
        
    except:
        pass
    
#print(pos_dict)
if frame == node.parm("endframe").eval():
    print("writing json")
    #print(json.dumps(pos_dict, indent=2))
    with open(node.parm("json_out").eval(), "w") as f:
        json.dump(pos_dict, f, indent=2)
    
    hou.playbar.stop()

