# set shape of Node
node.setUserData('nodeshape', "bulge")

# get all node shapes
editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
shapes = editor.nodeShapes()
print shapes

# create custom node shapes:
# https://vimeo.com/223222233