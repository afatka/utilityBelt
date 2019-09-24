"""
Utility Belt

This script allows you to pop out each individual 'professionalism' test for one off runs.

Written by: Adam Fatka
adam.fatka@gmail.com
www.fatkaforce.com


"""
import maya.cmds as cmds
from utilityBelt import utilities as utils 
reload(utils)



class utilityBeltGUI(object):
	"""

	This class sets up the GUI for the Maya Utility Belt.
	  The Maya Utility belt is a toolset to check the scene for 'professionalism' attributes. 
	  Such as; 

	  -The existence of a master/root node.
	  -Objects with default names
	  -the association with display layers: more specifically if objects are visible if all display layers are vis = 0
	  -Objects with transforms (non 0 values for translate and rotate, non 1 values for scale)
	  -Objects with construction history, exceptions made in method
	  -Objects/Nodes whose pivots are not centered
	  -Objects with N-gons
	  -Objects with triangles
	  -Objects with nonManifold geometry
	  -Objects with lamina faces
	  
	  There is also a basic count utility that counts the length of the selection.

	  """


	def __init__(self):
		self.log('GUI initializing', prefix = 'strandard')
		# self.shBtn = {}
		self.iconBtn = {}

		#path for icons. 
		self.path = utils.__file__.rpartition('/')
		self.path = (str(self.path[0]) + '/')
		self.iconPath = (str(self.path) + 'icons/')

		#main window width and height
		self.winWidthHeight = (100,162)
		#popup windows height and width
		self.popupWinWidthHeight = (300,50)

		self.utilityObject = utils.utilities()
		self.utilityBeltGUI()
		self.initialize()
		
	#debugging log - turn hush = True to silence
	def log(self, message, prefix = 'Debug', hush=True):
	    if not hush:
	        print("%s : %s " % (prefix,message))

	#initializes the utilies class. Collects nodes and prepares them for battle. Resets the class when needed. 
	def initialize(self, *args):
		self.log('initialized', prefix = 'Standard')
		self.utilityObject = utils.utilities()
		self.utilityObject.masterNodes = self.utilityObject.masterGroupTest()
		self.utilityObject.collectedNodes = self.utilityObject.nodeCollector(self.utilityObject.masterNodes)
		#colects transform nodes. 
		self.utilityObject.sortedNodes = self.utilityObject.sortNodeList(self.utilityObject.collectedNodes, 'transform')
		self.log("starting shelf activation")
		for key in self.iconBtn:
			cmds.iconTextButton(self.iconBtn[key], edit = True, enable = True)


	#runs the check for a master node and presents its findings at the annual gala 
	def masterGroupCheck(self, *args):
		self.log('MasterGroupCheck', prefix = 'Standard')

		if cmds.window("MasterNode_Utility_Window", exists = True):
		            cmds.deleteUI("MasterNode_Utility_Window", window=True)

		##After script completion comment out this section. 
		##This section forces Maya to recreate the window dimensions each time
		if cmds.windowPref("MasterNode_Utility_Window",exists = True):
		    cmds.windowPref("MasterNode_Utility_Window",remove=True)
		            
		cmds.window("MasterNode_Utility_Window", resizeToFitChildren=True, widthHeight = self.popupWinWidthHeight)
		cmds.paneLayout(configuration = 'horizontal2', staticHeightPane = 2)
		cmds.textScrollList('masterNode_textScroll', numberOfRows=8, allowMultiSelection=True, showIndexedItem=4, selectCommand = 'import maya.cmds as cmds;\ncmds.select(cmds.textScrollList("masterNode_textScroll", query = True, selectItem = True))')
		for item in self.utilityObject.masterNodes:
			cmds.textScrollList('masterNode_textScroll',edit = True, append = str(item))
		cmds.button(label = "Close", command = 'import maya.cmds as cmds; cmds.deleteUI("MasterNode_Utility_Window", window=True)')
		cmds.setParent('..')
		cmds.showWindow("MasterNode_Utility_Window")

	#Uses the utility class to check for default names on the objects 
	def defaultNamesCheck(self, *args):
		self.log('defaultNamesCheck', prefix = 'Standard')

		#if the attribute has already been created there is no purpose in wasting the cycles to create it again.
		try:
			self.utilityObject.hasDefaultName
		except AttributeError:
			self.log('AttributeError -- Creating hasDefaultName class attr')
			#grabs method specific data and sets attr hasDefaultName to that hold that data
			self.utilityObject.hasDefaultName = self.utilityObject.compareDefaultNames(self.utilityObject.sortedNodes)

		if cmds.window("DefaultName_Utility_Window", exists = True):
		            cmds.deleteUI("DefaultName_Utility_Window", window=True)

		##After script completion comment out this section. 
		##This section forces Maya to recreate the window dimensions each time
		if cmds.windowPref("DefaultName_Utility_Window",exists = True):
		    cmds.windowPref("DefaultName_Utility_Window",remove=True)
		            
		cmds.window("DefaultName_Utility_Window", resizeToFitChildren=True, widthHeight = self.popupWinWidthHeight)
		cmds.paneLayout(configuration = 'horizontal2', staticHeightPane = 2)
		cmds.textScrollList('DefaultName_textScroll', numberOfRows=8, allowMultiSelection=True, showIndexedItem=4, selectCommand = 'import maya.cmds as cmds;\ncmds.select(cmds.textScrollList("DefaultName_textScroll", query = True, selectItem = True))')
		for item in self.utilityObject.hasDefaultName:
			cmds.textScrollList('DefaultName_textScroll',edit = True, append = str(item))
		cmds.columnLayout(adjustableColumn = True)
		cmds.button('DefaultName_Select', label = 'Select Objects with Default Names', command = 'import maya.cmds as cmds;cmds.select(clear = True);\nfor item in %r:\n cmds.select(item, add=True)' % self.utilityObject.hasDefaultName)
		cmds.button('DefaultName_Button', label = ("Count: %s  - Close Window" % len(self.utilityObject.hasDefaultName)), command = 'import maya.cmds as cmds; cmds.deleteUI("DefaultName_Utility_Window", window=True)')
		cmds.setParent('..')
		cmds.showWindow()

	#Uses the utility class to check for objects on display layers
	def displayLayersCheck(self):
		self.log('displayLayersCheck', prefix = 'Standard')
		self.log('displayLayersCheck not operational.')
		#if the attribute has already been created there is no purpose in wasting the cycles to create it again.
		try:
			self.utilityObject.visibleNodes
		except AttributeError:
			self.log('AttributeError -- Creating displayLayers class attr')
			self.displayLayers = self.utilityObject.findLayers()
			self.initialLayerStates = self.utilityObject.collectLayerState(self.displayLayers)
			self.utilityObject.hideAllLayers(self.displayLayers)
			self.utilityObject.visibleNodes = self.utilityObject.visibilityBulkTest(self.utilityObject.sortedNodes)
			self.utilityObject.setLayersVisibility(self.displayLayers, self.initialLayerStates)

		if cmds.window("displayLayer_Utility_Window", exists = True):
		            cmds.deleteUI("displayLayer_Utility_Window", window=True)

		##After script completion comment out this section. 
		##This section forces Maya to recreate the window dimensions each time
		if cmds.windowPref("displayLayer_Utility_Window",exists = True):
		    cmds.windowPref("displayLayer_Utility_Window",remove=True)
		            
		cmds.window("displayLayer_Utility_Window", resizeToFitChildren=True, widthHeight = self.popupWinWidthHeight)
		cmds.paneLayout(configuration = 'horizontal2', staticHeightPane = 2)
		cmds.textScrollList('displayLayer_textScroll', numberOfRows=8, allowMultiSelection=True, showIndexedItem=4, selectCommand = 'import maya.cmds as cmds;\ncmds.select(cmds.textScrollList("displayLayer_textScroll", query = True, selectItem = True))')
		for item in self.utilityObject.visibleNodes:
			cmds.textScrollList('displayLayer_textScroll',edit = True, append = str(item))
		cmds.columnLayout(adjustableColumn = True)
		cmds.button('displayLayer_Select', label = 'Select Non-Layered Objects', command = 'import maya.cmds as cmds;cmds.select(clear = True);\nfor item in %r:\n cmds.select(item, add=True)' % self.utilityObject.visibleNodes)
		cmds.button('displayLayer_Button', label = ("Count: %s  - Close Window" % len(self.utilityObject.visibleNodes)), command = 'import maya.cmds as cmds; cmds.deleteUI("displayLayer_Utility_Window", window=True)')
		cmds.setParent('..')
		cmds.showWindow()

	#Uses the utility class to check for frozen transforms
	def frozenTransformsCheck(self):
		self.log('frozenTransformsCheck', prefix = 'Standard')

		#if the attribute has already been created there is no purpose in wasting the cycles to create it again.
		try:
			self.utilityObject.notFrozen
		except AttributeError:
			self.log('AttributeError -- Creating notFrozen class attr')
			#grabs method specific data and sets attr notFrozen to that hold that data
			self.utilityObject.notFrozen = self.utilityObject.frozenTransforms(self.utilityObject.sortedNodes)

		if cmds.window("notFrozen_Utility_Window", exists = True):
		            cmds.deleteUI("notFrozen_Utility_Window", window=True)

		##After script completion comment out this section. 
		##This section forces Maya to recreate the window dimensions each time
		if cmds.windowPref("notFrozen_Utility_Window",exists = True):
		    cmds.windowPref("notFrozen_Utility_Window",remove=True)
		            
		cmds.window("notFrozen_Utility_Window", resizeToFitChildren=True, widthHeight = self.popupWinWidthHeight)
		cmds.paneLayout(configuration = 'horizontal2', staticHeightPane = 2)
		cmds.textScrollList('notFrozen_textScroll', numberOfRows=8, allowMultiSelection=True, showIndexedItem=4, selectCommand = 'import maya.cmds as cmds;\ncmds.select(cmds.textScrollList("notFrozen_textScroll", query = True, selectItem = True))')
		for item in self.utilityObject.notFrozen:
			cmds.textScrollList('notFrozen_textScroll',edit = True, append = str(item))
		cmds.columnLayout(adjustableColumn = True)
		cmds.button('notFrozen_Select', label = 'Select Non-Frozen Nodes', command = 'import maya.cmds as cmds;cmds.select(clear = True);\nfor item in %r:\n cmds.select(item, add=True)' % self.utilityObject.notFrozen)
		cmds.button('notFrozen_Button', label = ("Count: %s  - Close Window" % len(self.utilityObject.notFrozen)), command = 'import maya.cmds as cmds; cmds.deleteUI("notFrozen_Utility_Window", window=True)')
		cmds.setParent('..')
		cmds.showWindow()

	#Uses the utility class to check for construction history
	def constructionHistoryCheck(self):
		self.log('constructionHistoryCheck', prefix = 'Standard')

		#if the attribute has already been created there is no purpose in wasting the cycles to create it again.
		try:
			self.utilityObject.hasHistory
		except AttributeError:
			self.log('AttributeError -- Creating hasHistory class attr')
			#grabs method specific data and sets attr hasHistory to that hold that data
			self.utilityObject.hasHistory = self.utilityObject.historyFinder(self.utilityObject.sortedNodes)

		if cmds.window("hasHistory_Utility_Window", exists = True):
		            cmds.deleteUI("hasHistory_Utility_Window", window=True)

		##After script completion comment out this section. 
		##This section forces Maya to recreate the window dimensions each time
		if cmds.windowPref("hasHistory_Utility_Window",exists = True):
		    cmds.windowPref("hasHistory_Utility_Window",remove=True)
		            
		cmds.window("hasHistory_Utility_Window", resizeToFitChildren=True, widthHeight = self.popupWinWidthHeight)
		cmds.paneLayout(configuration = 'horizontal2', staticHeightPane = 2)
		cmds.textScrollList('hasHistory_textScroll', numberOfRows=8, allowMultiSelection=True, showIndexedItem=4, selectCommand = 'import maya.cmds as cmds;\ncmds.select(cmds.textScrollList("hasHistory_textScroll", query = True, selectItem = True))')
		for item in self.utilityObject.hasHistory:
			cmds.textScrollList('hasHistory_textScroll',edit = True, append = str(item))
		cmds.columnLayout(adjustableColumn = True)
		cmds.button('hasHistory_Select', label = 'Select Objects with History', command = 'import maya.cmds as cmds;cmds.select(clear = True);\nfor item in %r:\n cmds.select(item, add=True)' % self.utilityObject.hasHistory)
		cmds.button('hasHistory_Button', label = ("Count: %s  - Close Window" % len(self.utilityObject.hasHistory)), command = 'import maya.cmds as cmds; cmds.deleteUI("hasHistory_Utility_Window", window=True)')
		cmds.setParent('..')
		cmds.showWindow()

	#Uses the utility class to check for centered pivots
	def centeredPivotsCheck(self):
		self.log('centeredPivotsCheck', prefix = 'Standard')

		#if the attribute has already been created there is no purpose in wasting the cycles to create it again.
		try:
			self.utilityObject.pivotsNotCenter
		except AttributeError:
			self.log('AttributeError -- Creating pivotsNotCenter class attr')
			#grabs method specific data and sets attr pivotsNotCenter to that hold that data
			self.utilityObject.pivotsNotCenter = self.utilityObject.pivotsCentered(self.utilityObject.sortedNodes)

		if cmds.window("pivotsNotCenter_Utility_Window", exists = True):
		            cmds.deleteUI("pivotsNotCenter_Utility_Window", window=True)

		##After script completion comment out this section. 
		##This section forces Maya to recreate the window dimensions each time
		if cmds.windowPref("pivotsNotCenter_Utility_Window",exists = True):
		    cmds.windowPref("pivotsNotCenter_Utility_Window",remove=True)
		            
		cmds.window("pivotsNotCenter_Utility_Window", resizeToFitChildren=True, widthHeight = self.popupWinWidthHeight)
		cmds.paneLayout(configuration = 'horizontal2', staticHeightPane = 2)
		cmds.textScrollList('pivotsNotCenter_textScroll', numberOfRows=8, allowMultiSelection=True, showIndexedItem=4, selectCommand = 'import maya.cmds as cmds;\ncmds.select(cmds.textScrollList("pivotsNotCenter_textScroll", query = True, selectItem = True))')
		for item in self.utilityObject.pivotsNotCenter:
			cmds.textScrollList('pivotsNotCenter_textScroll',edit = True, append = str(item))
		cmds.columnLayout(adjustableColumn = True)
		cmds.button('pivotsNotCenter_Select', label = 'Select NonCentered Pivots', command = 'import maya.cmds as cmds;cmds.select(clear = True);\nfor item in %r:\n cmds.select(item, add=True)' % self.utilityObject.pivotsNotCenter)
		cmds.button('pivotsNotCenter_Button', label = ("Count: %s  - Close Window" % len(self.utilityObject.pivotsNotCenter)), command = 'import maya.cmds as cmds; cmds.deleteUI("pivotsNotCenter_Utility_Window", window=True)')
		cmds.setParent('..')
		cmds.showWindow()

	#Uses the utility class to check for ngons
	def nGonFinder(self):
		self.log('nGonFinder', prefix = 'Standard')

		#if the attribute has already been created there is no purpose in wasting the cycles to create it again.
		try:
			self.utilityObject.nSidedObjects
		except AttributeError:
			self.log('AttributeError -- Creating nSidedbjects and nSidedFaces class attr')
			#grabs method specific data and sets attr notFrozen to that hold that data
			self.utilityObject.nSidedObjects, self.utilityObject.nSidedFaces = self.utilityObject.nGonFinder(self.utilityObject.sortedNodes)

		if cmds.window("nGonFinder_Utility_Window", exists = True):
		            cmds.deleteUI("nGonFinder_Utility_Window", window=True)

		##After script completion comment out this section. 
		##This section forces Maya to recreate the window dimensions each time
		if cmds.windowPref("nGonFinder_Utility_Window",exists = True):
		    cmds.windowPref("nGonFinder_Utility_Window",remove=True)
		            
		cmds.window("nGonFinder_Utility_Window", resizeToFitChildren=True, widthHeight = self.popupWinWidthHeight)
		cmds.paneLayout(configuration = 'horizontal2', staticHeightPane = 2)
		cmds.textScrollList('nGonFinder_textScroll', numberOfRows=8, allowMultiSelection=True, showIndexedItem=4, selectCommand = 'import maya.cmds as cmds;\ncmds.select(cmds.textScrollList("nGonFinder_textScroll", query = True, selectItem = True))')
		for item in self.utilityObject.nSidedObjects:
			cmds.textScrollList('nGonFinder_textScroll',edit = True, append = str(item))
		cmds.columnLayout(adjustableColumn = True)
		form = cmds.formLayout('nGon_FormLayout', numberOfDivisions = 100)
		button1 = cmds.button('nGonObjects_Select', label = 'Select nSidedObjects', command = 'import maya.cmds as cmds;cmds.select(clear = True);\nfor item in %r:\n cmds.select(item, add=True)' % self.utilityObject.nSidedObjects)
		button2 = cmds.button('nGonFaces_Select', label = 'Select nSidedFaces', command = 'import maya.cmds as cmds;cmds.select(clear = True);\nfor item in %r:\n cmds.select(item, add=True)' % self.utilityObject.nSidedFaces)
		cmds.formLayout(form, edit = True, 
			attachForm =[
			(button1, 'top',2),
			(button1, 'left', 2),
			(button1, 'bottom', 2),
			(button2, 'top', 2),
			(button2, 'right', 2),
			(button2, 'bottom', 2)
			], 
			attachControl = [
			(button1,'right',2, button2),
			(button2, 'left', 2, button1)
			],
			attachPosition = [
			(button1, 'right', 1, 50),
			(button2, 'left', 1, 50)
			])
		cmds.setParent('..')
		cmds.button('nGonFinder_Button', label = ("N-gons: %s  - Close Window" % len(self.utilityObject.nSidedFaces)), command = 'import maya.cmds as cmds; cmds.deleteUI("nGonFinder_Utility_Window", window=True)')
		cmds.setParent('..')
		cmds.showWindow()

	#Uses the utility class to check for triangles
	def triFinder(self):
		self.log('triFinder', prefix = 'Standard')

		#if the attribute has already been created there is no purpose in wasting the cycles to create it again.
		try:
			self.utilityObject.triObjects
		except AttributeError:
			self.log('AttributeError -- Creating triObjects and triFaces class attr')
			#grabs method specific data and sets attr notFrozen to that hold that data
			self.utilityObject.triObjects, self.utilityObject.triFaces = self.utilityObject.triFinder(self.utilityObject.sortedNodes)

		if cmds.window("triFinder_Utility_Window", exists = True):
		            cmds.deleteUI("triFinder_Utility_Window", window=True)

		##After script completion comment out this section. 
		##This section forces Maya to recreate the window dimensions each time
		if cmds.windowPref("triFinder_Utility_Window",exists = True):
		    cmds.windowPref("triFinder_Utility_Window",remove=True)
		            
		cmds.window("triFinder_Utility_Window", resizeToFitChildren=True, widthHeight = self.popupWinWidthHeight)
		cmds.paneLayout(configuration = 'horizontal2', staticHeightPane = 2)
		cmds.textScrollList('triFinder_textScroll', numberOfRows=8, allowMultiSelection=True, showIndexedItem=4, selectCommand = 'import maya.cmds as cmds;\ncmds.select(cmds.textScrollList("triFinder_textScroll", query = True, selectItem = True))')
		for item in self.utilityObject.triObjects:
			cmds.textScrollList('triFinder_textScroll',edit = True, append = str(item))
		cmds.columnLayout(adjustableColumn = True)
		form = cmds.formLayout('tri_FormLayout', numberOfDivisions = 100)
		button1 = cmds.button('triObjects_Select', label = 'Select triObjects', command = 'import maya.cmds as cmds;cmds.select(clear = True);\nfor item in %r:\n cmds.select(item, add=True)' % self.utilityObject.triObjects)
		button2 = cmds.button('triFaces_Select', label = 'Select triFaces', command = 'import maya.cmds as cmds;cmds.select(clear = True);\nfor item in %r:\n cmds.select(item, add=True)' % self.utilityObject.triFaces)
		cmds.formLayout(form, edit = True, 
			attachForm =[
			(button1, 'top',2),
			(button1, 'left', 2),
			(button1, 'bottom', 2),
			(button2, 'top', 2),
			(button2, 'right', 2),
			(button2, 'bottom', 2)
			], 
			attachControl = [
			(button1,'right',2, button2),
			(button2, 'left', 2, button1)
			],
			attachPosition = [
			(button1, 'right', 1, 50),
			(button2, 'left', 1, 50)
			])
		cmds.setParent('..')
		cmds.button('triFinder_Button', label = ("Triangles: %s  - Close Window" % len(self.utilityObject.triFaces)), command = 'import maya.cmds as cmds; cmds.deleteUI("triFinder_Utility_Window", window=True)')
		cmds.setParent('..')
		cmds.showWindow()

	#Uses the utility class to check for nonmanifold geometry
	def nonManifoldFinder(self):
		self.log('nonManifoldFinder', prefix = 'Standard')

		#if the attribute has already been created there is no purpose in wasting the cycles to create it again.
		try:
			self.utilityObject.nonManifoldObjects
		except AttributeError:
			self.log('AttributeError -- Creating nonManifoldObjects and nonManifoldComponents class attr')
			#grabs method specific data and sets attr notFrozen to that hold that data
			self.utilityObject.nonManifoldObjects, self.utilityObject.nonManifoldComponents = self.utilityObject.nonManifoldFinder(self.utilityObject.sortedNodes)

		if cmds.window("nonManifoldFinder_Utility_Window", exists = True):
		            cmds.deleteUI("nonManifoldFinder_Utility_Window", window=True)

		##After script completion comment out this section. 
		##This section forces Maya to recreate the window dimensions each time
		if cmds.windowPref("nonManifoldFinder_Utility_Window",exists = True):
		    cmds.windowPref("nonManifoldFinder_Utility_Window",remove=True)
		            
		cmds.window("nonManifoldFinder_Utility_Window", resizeToFitChildren=True, widthHeight = self.popupWinWidthHeight)
		cmds.paneLayout(configuration = 'horizontal2', staticHeightPane = 2)
		cmds.textScrollList('nonManifoldFinder_textScroll', numberOfRows=8, allowMultiSelection=True, showIndexedItem=4, selectCommand = 'import maya.cmds as cmds;\ncmds.select(cmds.textScrollList("nonManifoldFinder_textScroll", query = True, selectItem = True))')
		for item in self.utilityObject.nonManifoldObjects:
			cmds.textScrollList('nonManifoldFinder_textScroll',edit = True, append = str(item))
		cmds.columnLayout(adjustableColumn = True)
		form = cmds.formLayout('nonManifold_FormLayout', numberOfDivisions = 100)
		button1 = cmds.button('nonManifoldObjects_Select', label = 'Select nonManifoldObjects', command = 'import maya.cmds as cmds;cmds.select(clear = True);\nfor item in %r:\n cmds.select(item, add=True)' % self.utilityObject.nonManifoldObjects)
		button2 = cmds.button('nonManifoldFComponents_Select', label = 'Select nonManifoldComponents', command = 'import maya.cmds as cmds;cmds.select(clear = True);\nfor item in %r:\n cmds.select(item, add=True)' % self.utilityObject.nonManifoldComponents)
		cmds.formLayout(form, edit = True, 
			attachForm =[
			(button1, 'top',2),
			(button1, 'left', 2),
			(button1, 'bottom', 2),
			(button2, 'top', 2),
			(button2, 'right', 2),
			(button2, 'bottom', 2)
			], 
			attachControl = [
			(button1,'right',2, button2),
			(button2, 'left', 2, button1)
			],
			attachPosition = [
			(button1, 'right', 1, 50),
			(button2, 'left', 1, 50)
			])
		cmds.setParent('..')
		cmds.button('nonManifoldFinder_Button', label = ("nonManifoldComponents: %s  - Close Window" % len(self.utilityObject.nonManifoldComponents)), command = 'import maya.cmds as cmds; cmds.deleteUI("nonManifoldFinder_Utility_Window", window=True)')
		cmds.setParent('..')
		cmds.showWindow()

	#Uses the utility class to check for lamina faces
	def laminaFinder(self):
		self.log('laminaFinder', prefix = 'Standard')

		#if the attribute has already been created there is no purpose in wasting the cycles to create it again.
		try:
			self.utilityObject.laminaObjects
		except AttributeError:
			self.log('AttributeError -- Creating laminaObjects and laminaFaces class attr')
			#grabs method specific data and sets attr notFrozen to that hold that data
			self.utilityObject.laminaObjects, self.utilityObject.laminaFaces = self.utilityObject.laminaFinder(self.utilityObject.sortedNodes)

		if cmds.window("laminaFinder_Utility_Window", exists = True):
		            cmds.deleteUI("laminaFinder_Utility_Window", window=True)

		##After script completion comment out this section. 
		##This section forces Maya to recreate the window dimensions each time
		if cmds.windowPref("laminaFinder_Utility_Window",exists = True):
		    cmds.windowPref("laminaFinder_Utility_Window",remove=True)
		            
		cmds.window("laminaFinder_Utility_Window", resizeToFitChildren=True, widthHeight = self.popupWinWidthHeight)
		cmds.paneLayout(configuration = 'horizontal2', staticHeightPane = 2)
		cmds.textScrollList('laminaFinder_textScroll', numberOfRows=8, allowMultiSelection=True, showIndexedItem=4, selectCommand = 'import maya.cmds as cmds;\ncmds.select(cmds.textScrollList("laminaFinder_textScroll", query = True, selectItem = True))')
		for item in self.utilityObject.laminaObjects:
			cmds.textScrollList('laminaFinder_textScroll',edit = True, append = str(item))
		cmds.columnLayout(adjustableColumn = True)
		form = cmds.formLayout('lamina_FormLayout', numberOfDivisions = 100)
		button1 = cmds.button('laminaObjects_Select', label = 'Select laminaObjects', command = 'import maya.cmds as cmds;cmds.select(clear = True);\nfor item in %r:\n cmds.select(item, add=True)' % self.utilityObject.laminaObjects)
		button2 = cmds.button('laminaFaces_Select', label = 'Select laminaFaces', command = 'import maya.cmds as cmds;cmds.select(clear = True);\nfor item in %r:\n cmds.select(item, add=True)' % self.utilityObject.laminaFaces)
		cmds.formLayout(form, edit = True, 
			attachForm =[
			(button1, 'top',2),
			(button1, 'left', 2),
			(button1, 'bottom', 2),
			(button2, 'top', 2),
			(button2, 'right', 2),
			(button2, 'bottom', 2)
			], 
			attachControl = [
			(button1,'right',2, button2),
			(button2, 'left', 2, button1)
			],
			attachPosition = [
			(button1, 'right', 1, 50),
			(button2, 'left', 1, 50)
			])
		cmds.setParent('..')
		cmds.button('laminaFinder_Button', label = ("Lamina Faces: %s  - Close Window" % len(self.utilityObject.laminaFaces)), command = 'import maya.cmds as cmds; cmds.deleteUI("laminaFinder_Utility_Window", window=True)')
		cmds.setParent('..')
		cmds.showWindow()

	#Uses the utility class to count the number of selected objects
	def countProc(self):
		self.log('countProc', prefix = 'Standard')
		countTemp = cmds.ls(selection = True)

		if cmds.window("Count_Utility_Window", exists = True):
		            cmds.deleteUI("Count_Utility_Window", window=True)

		##After script completion comment out this section. 
		##This section forces Maya to recreate the window dimensions each time
		if cmds.windowPref("Count_Utility_Window",exists = True):
		    cmds.windowPref("Count_Utility_Window",remove=True)
		            
		cmds.window("Count_Utility_Window", resizeToFitChildren=True, widthHeight = self.popupWinWidthHeight)
		cmds.columnLayout(adjustableColumn = True)
		cmds.button('Count_Button', label = ("Count: %s  - Close Window" % len(countTemp)), command = 'import maya.cmds as cmds; cmds.deleteUI("Count_Utility_Window", window=True)')
		cmds.setParent('..')
		cmds.showWindow()

	#This function creates the GUI for the autoProGui Supplemental
	def utilityBeltGUI(self):

		if cmds.window("Maya_Utility_Window", exists = True):
		            cmds.deleteUI("Maya_Utility_Window", window=True)
		            
		cmds.window("Maya_Utility_Window", resizeToFitChildren=False, widthHeight = self.winWidthHeight, sizeable = False)

		##After script completion comment out this section. 
		##This section forces Maya to recreate the window dimensions each time
		if cmds.windowPref("Maya_Utility_Window",exists = True):
		    cmds.windowPref("Maya_Utility_Window",remove=True)
		######################################################################
		    
		cmds.columnLayout('utilColumn', adjustableColumn = True,  rowSpacing = 3)
		cmds.button(label = 'Reinitialize', command = self.initialize)

		cmds.gridLayout(numberOfColumns = 3)

		self.iconBtn['masterGroups'] =  cmds.iconTextButton(style='iconOnly', image1=(self.iconPath + 'icon_masterGroup.png'), 
									label="MasterGroup", annotation="Master Groups", enable = False, command= self.masterGroupCheck)
		self.iconBtn['defaultNames'] = cmds.iconTextButton(style='iconOnly',image1=(self.iconPath + 'icon_defaultNames.png'),
								 label="DefaultNames", annotation="Default Names",enable = False,
								 command=self.defaultNamesCheck)
		self.iconBtn['displayLayers'] = cmds.iconTextButton(style='iconOnly',image1=(self.iconPath + 'icon_displayLayers.png'),
								 label="DisplayLayers", annotation="Display Layers",enable = False,
								 command=self.displayLayersCheck)
		self.iconBtn['frozenTransforms'] = cmds.iconTextButton(style='iconOnly',image1=(self.iconPath + 'icon_notFrozen.png'),
								 label="FrozenTransforms", annotation="Frozen Transforms",enable = False,
								 command=self.frozenTransformsCheck)
		self.iconBtn['constructionHistory'] = cmds.iconTextButton(style='iconOnly',image1=(self.iconPath + 'icon_hasHistory.png'),
								 label="ConstructionHistory", annotation="Construction History",enable = False,
								 command=self.constructionHistoryCheck)
		self.iconBtn['centeredPivots'] = cmds.iconTextButton(style='iconOnly',image1=(self.iconPath + 'icon_notCentered.png'),
								 label="CenteredPivots", annotation="Centered Pivots",enable = False,
								 command=self.centeredPivotsCheck)
		self.iconBtn['nGonFinder'] = cmds.iconTextButton(style='iconOnly',image1=(self.iconPath + 'icon_nGonFinder.png'),
								 label="NGonFinder", annotation="N-Gon Finder",enable = False,
								 command=self.nGonFinder)
		self.iconBtn['triFinder'] = cmds.iconTextButton(style='iconOnly',image1=(self.iconPath + 'icon_triFinder.png'),
								 label="triFinder", annotation="Tri Finder",enable = False,
								 command=self.triFinder)
		self.iconBtn['nonManifoldFinder'] = cmds.iconTextButton(style='iconOnly',image1=(self.iconPath + 'icon_nonManifoldFinder.png'),
								 label="nonManifoldFinder", annotation="NonManifold Finder",enable = False,
								 command=self.nonManifoldFinder)
		self.iconBtn['laminaFinder'] = cmds.iconTextButton(style='iconOnly',image1=(self.iconPath + 'icon_laminaFinder.png'),
								 label="laminaFinder", annotation="Lamina Finder",enable = False,
								 command=self.laminaFinder)
		self.iconBtn['count'] = cmds.iconTextButton(style='iconOnly',image1=(self.iconPath + 'icon_count.png'),
								 label="count", annotation="Count",enable = False,
								 command=self.countProc)
		cmds.setParent('..')
		cmds.setParent('..')
		cmds.showWindow("Maya_Utility_Window")

		cmds.window(frontWindow = True)