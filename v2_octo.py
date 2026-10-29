from my_utils.v2_get_octo import getOcto_v2
import FreeCAD as App
import Part
V = App.Vector
import math

useCache = globals().get("__useCache__", False)
for3DPrint = globals().get("__for3DPrint__", False)
docName = "octo_v2"
try:
    doc = App.getDocument(docName)
except:
    doc = App.newDocument(docName)
for obj in list(doc.Objects):
    doc.removeObject(obj.Name)


octo = getOcto_v2(doc, for3DPrint, True)


rtnPart = octo