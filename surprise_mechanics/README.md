### Surprise Mechanics ###

* surprise_mechanics.hiplc
Houdini file in which the lootbox is opened.

* fireworks.hiplc
Houdini file in which the opening animation is generated

* fireworks.json
Saves the Postion of Color of points for the opening animation.

* lootbox.otl
Houdini HDA for the lootbox
connect any node to the first input and press the Button in the Parameters.

Has a hidden "lootboxContents" parameter which has to point to the lootbox.json
By default this points to "$HIP/lootbox.json"

The python node inside this HDA has a "file" parameter which has to point to the node animation.
By default this points to "$HIP/fireworks.json"

* hou_readJson.py
is a copy of the code in the lootbox.otl

* hou_writeJson.py
is a copy of the code from the fireworks.hiplc

* surprise_mechanics.py
this module is imported in the lootbox.otl python module.
The Button calls the main function.

* icons:
created using a tool by PRDX / Bastian J. Schiffer
https://vimeo.com/223222233

Place them here
\Program Files\Side Effects Software\Houdini {VERSION}\houdini\config\NodeShapes