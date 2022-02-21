# Houdini Batch Import
# Author: Michael Elton Widjaja
# Nov 2018

import hou
import os
import sys
from PySide2 import QtWidgets, QtUiTools, QtCore, QtGui

# UI
class Ui_BatchImport(object):
	def setupUi(self, BatchImport):
		BatchImport.setObjectName("BatchImport")
		BatchImport.resize(510, 590)
		BatchImport.setAutoFillBackground(False)
		BatchImport.setStyleSheet("background-color: rgb(40, 40, 40);\n"
"border-color: rgb(40, 40, 40);")
		self.gridLayout = QtWidgets.QGridLayout(BatchImport)
		self.gridLayout.setObjectName("gridLayout")
		self.verticalLayout = QtWidgets.QVBoxLayout()
		self.verticalLayout.setObjectName("verticalLayout")
		self.label = QtWidgets.QLabel(BatchImport)
		self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: bold 16pt \"Arial\";")
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.label.setObjectName("label")
		self.verticalLayout.addWidget(self.label)
		self.line_3 = QtWidgets.QFrame(BatchImport)
		self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_3.setObjectName("line_3")
		self.verticalLayout.addWidget(self.line_3)
		self.label_3 = QtWidgets.QLabel(BatchImport)
		self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: bold 10pt \"Arial\";")
		self.label_3.setObjectName("label_3")
		self.verticalLayout.addWidget(self.label_3)
		self.label_2 = QtWidgets.QLabel(BatchImport)
		self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 8pt \"Arial\";")
		self.label_2.setWordWrap(True)
		self.label_2.setObjectName("label_2")
		self.verticalLayout.addWidget(self.label_2)
		self.tree_files = QtWidgets.QTreeWidget(BatchImport)
		font = QtGui.QFont()
		font.setFamily("Arial")
		font.setPointSize(10)
		font.setWeight(50)
		font.setItalic(False)
		font.setBold(False)
		self.tree_files.setFont(font)
		self.tree_files.setAutoFillBackground(False)
		self.tree_files.setStyleSheet("QTreeWidget {\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(55, 55, 55);\n"
"font: 10pt \"Arial\";\n"
"}\n"
"\n"
"QTreeWidget::item:selected {\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(23, 76, 110);\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(55, 55, 55);\n"
"font: 10pt \"Arial\";\n"
"border: 0px\n"
"}")
		self.tree_files.setProperty("showDropIndicator", True)
		self.tree_files.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
		self.tree_files.setDefaultDropAction(QtCore.Qt.CopyAction)
		self.tree_files.setAlternatingRowColors(False)
		self.tree_files.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
		self.tree_files.setObjectName("tree_files")
		self.tree_files.header().setVisible(True)
		self.tree_files.header().setCascadingSectionResizes(False)
		self.verticalLayout.addWidget(self.tree_files)
		self.onegeoonefile = QtWidgets.QCheckBox(BatchImport)
		font = QtGui.QFont()
		font.setFamily("Arial")
		font.setPointSize(10)
		font.setWeight(50)
		font.setItalic(False)
		font.setBold(False)
		self.onegeoonefile.setFont(font)
		self.onegeoonefile.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 10pt \"Arial\";")
		self.onegeoonefile.setObjectName("onegeoonefile")
		self.verticalLayout.addWidget(self.onegeoonefile)
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.button_addFiles = QtWidgets.QPushButton(BatchImport)
		self.button_addFiles.setMinimumSize(QtCore.QSize(0, 20))
		font = QtGui.QFont()
		font.setFamily("Arial")
		font.setPointSize(10)
		font.setWeight(75)
		font.setItalic(False)
		font.setBold(True)
		self.button_addFiles.setFont(font)
		self.button_addFiles.setAutoFillBackground(False)
		self.button_addFiles.setStyleSheet("QPushButton {\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(55, 55, 55);\n"
"font: bold 10pt \"Arial\";\n"
"border: solid 4px;\n"
"border-color: rgb(55, 55, 55);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgb(85, 85, 85);\n"
"border-color: rgb(85, 85, 85);\n"
"}")
		self.button_addFiles.setAutoDefault(False)
		self.button_addFiles.setDefault(False)
		self.button_addFiles.setFlat(False)
		self.button_addFiles.setObjectName("button_addFiles")
		self.horizontalLayout.addWidget(self.button_addFiles)
		self.button_removeFiles = QtWidgets.QPushButton(BatchImport)
		self.button_removeFiles.setMinimumSize(QtCore.QSize(0, 20))
		font = QtGui.QFont()
		font.setFamily("Arial")
		font.setPointSize(10)
		font.setWeight(75)
		font.setItalic(False)
		font.setBold(True)
		self.button_removeFiles.setFont(font)
		self.button_removeFiles.setStyleSheet("QPushButton {\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(55, 55, 55);\n"
"font: bold 10pt \"Arial\";\n"
"border: solid 4px;\n"
"border-color: rgb(55, 55, 55);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgb(85, 85, 85);\n"
"border-color: rgb(85, 85, 85);\n"
"}")
		self.button_removeFiles.setObjectName("button_removeFiles")
		self.horizontalLayout.addWidget(self.button_removeFiles)
		self.button_removeAllFiles = QtWidgets.QPushButton(BatchImport)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.button_removeAllFiles.sizePolicy().hasHeightForWidth())
		self.button_removeAllFiles.setSizePolicy(sizePolicy)
		self.button_removeAllFiles.setMinimumSize(QtCore.QSize(0, 20))
		font = QtGui.QFont()
		font.setFamily("Arial")
		font.setPointSize(10)
		font.setWeight(75)
		font.setItalic(False)
		font.setBold(True)
		self.button_removeAllFiles.setFont(font)
		self.button_removeAllFiles.setStyleSheet("QPushButton {\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(55, 55, 55);\n"
"font: bold 10pt \"Arial\";\n"
"border: solid 4px;\n"
"border-color: rgb(55, 55, 55);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgb(85, 85, 85);\n"
"border-color: rgb(85, 85, 85);\n"
"}")
		self.button_removeAllFiles.setObjectName("button_removeAllFiles")
		self.horizontalLayout.addWidget(self.button_removeAllFiles)
		self.verticalLayout.addLayout(self.horizontalLayout)
		self.button_import = QtWidgets.QPushButton(BatchImport)
		self.button_import.setMinimumSize(QtCore.QSize(0, 40))
		font = QtGui.QFont()
		font.setFamily("Arial")
		font.setPointSize(10)
		font.setWeight(75)
		font.setItalic(False)
		font.setBold(True)
		self.button_import.setFont(font)
		self.button_import.setStyleSheet("QPushButton {\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 140, 0);\n"
"font: bold 10pt \"Arial\";\n"
"border: 0px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgb(0, 170, 0);\n"
"}")
		self.button_import.setObjectName("button_import")
		self.verticalLayout.addWidget(self.button_import)
		self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

		self.retranslateUi(BatchImport)
		QtCore.QMetaObject.connectSlotsByName(BatchImport)

	def retranslateUi(self, BatchImport):
		BatchImport.setWindowTitle(QtWidgets.QApplication.translate("BatchImport", "Form", None, -1))
		self.label.setText(QtWidgets.QApplication.translate("BatchImport", "Batch import", None, -1))
		self.label_3.setText(QtWidgets.QApplication.translate("BatchImport", "Drag and drop file(s) or press \"Add file(s)\"", None, -1))
		self.label_2.setText(QtWidgets.QApplication.translate("BatchImport", "* Supported extensions (also supports sequence): all extensions that are available in the file node.", None, -1))
		self.tree_files.headerItem().setText(0, QtWidgets.QApplication.translate("BatchImport", "Path", None, -1))
		self.tree_files.headerItem().setText(1, QtWidgets.QApplication.translate("BatchImport", "File", None, -1))
		self.onegeoonefile.setText(QtWidgets.QApplication.translate("BatchImport", "One geo, one file", None, -1))
		self.button_addFiles.setText(QtWidgets.QApplication.translate("BatchImport", "Add file(s)", None, -1))
		self.button_removeFiles.setText(QtWidgets.QApplication.translate("BatchImport", "Remove file(s)", None, -1))
		self.button_removeAllFiles.setText(QtWidgets.QApplication.translate("BatchImport", "Remove all file(s)", None, -1))
		self.button_import.setText(QtWidgets.QApplication.translate("BatchImport", "Import", None, -1))





# Batch import script
class BatchImport(QtWidgets.QWidget, Ui_BatchImport):

	def __init__(self, *args, **kwargs):
		QtWidgets.QWidget.__init__(self)
		Ui_BatchImport.__init__(self)
		self.setupUi(self)
		self.setWindowTitle(self.tr("Batch import - by Michael Elton Widjaja"))
		self.setAcceptDrops(True)

		# Create connections
		self.button_addFiles.clicked.connect(self.addFiles)
		self.button_removeFiles.clicked.connect(self.removeFiles)
		self.button_removeAllFiles.clicked.connect(self.removeAllFiles)
		self.button_import.clicked.connect(self.importGeometries)

		self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

		# Initialize variables
		self.list_files = []
		self.ext = (
			".geo.gz", 
			".bgeo.gz", 
			".hclassic.gz", 
			".bhclassic.gz", 
			".geo.sc", 
			".bgeo.sc", 
			".hclassic.sc", 
			".bhclassic.sc", 
			".json.gz", 
			".bjson.gz", 
			".json.sc", 
			".bjson.sc", 
			".bhclassic.lzma", 
			".bgeo.lzma", 
			".hclassic.bz2", 
			".bgeo.bz2", 
			".geo.lzma", 
			".hclassic.lzma", 
			".geo.bz2", 
			".bhclassic.bz2", 
			".geo", 
			".bgeo", 
			".hclassic", 
			".bhclassic", 
			".geogz", 
			".bgeogz", 
			".hclassicgz", 
			".bhclassicgz", 
			".geosc", 
			".bgeosc", 
			".hclassicsc", 
			".bhclassicsc", 
			".json", 
			".bjson", 
			".jsongz", 
			".bjsongz", 
			".jsonsc", 
			".bjsonsc", 
			".poly", 
			".bpoly", 
			".d", 
			".rib", 
			".vdb", 
			".pc", 
			".pmap", 
			".off", 
			".iges", 
			".igs", 
			".ply", 
			".obj", 
			".pdb", 
			".lw", 
			".lwo", 
			".bstl", 
			".eps", 
			".ai", 
			".stl", 
			".dxf", 
			".abc", 
			".fbx"
		)

	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls():
			event.accept()
		else:
			event.ignore()

	def dropEvent(self, event):
		files = [unicode(u.toLocalFile()) for u in event.mimeData().urls()]
		for f in files:
			if f in self.list_files:
				print f, " already exists in list."
				continue
			elif f.endswith(self.ext):
				self.list_files.append(f)
				filename = f.split("/")[-1]
				filepath = os.path.split(f)[0] + "/"
				item = QtWidgets.QTreeWidgetItem()
				item.setText(0, filepath)
				item.setText(1, filename)
				self.tree_files.addTopLevelItem(item)
				#print unicode(item.text(1)) + " has been added to list."
			else:
				print "Warning: Unsupported file format."
				continue
	
	def addFiles(self):
		file_fullPath = hou.ui.selectFile(title="Select file(s)", file_type=hou.fileType.Geometry, multiple_select=True)
		if (bool(file_fullPath) == False):
			pass
		else:
			file_fullPath_split = file_fullPath.split(" ; ")
			for file in file_fullPath_split:
				if file in self.list_files:
					print file, " already exists in list."
					continue
				elif file.endswith(self.ext):
					self.list_files.append(file)
					filename = file.split("/")[-1]
					filepath = os.path.split(file)[0] + "/"
					item = QtWidgets.QTreeWidgetItem()
					item.setText(0, filepath)
					item.setText(1, filename)
					self.tree_files.addTopLevelItem(item)
					#print unicode(item.text(1)) + " has been added to list."
				else:
					print "Warning: Unsupported file format."
					continue

	def removeFiles(self):
		items = self.tree_files.selectedItems()
		if not items:
			return
		for item in items:
			filepath = unicode(item.text(0))
			filename = unicode(item.text(1))
			file = filepath + filename
			#print filename + " has been removed from list."
			self.list_files.remove(file)
			item_index = self.tree_files.indexOfTopLevelItem(item)
			self.tree_files.takeTopLevelItem(item_index)

	def removeAllFiles(self):
		self.tree_files.clear()
		self.list_files = []
		#print "List has been cleared."

	def importGeometries(self):
		if len(self.list_files) == 0:
			hou.ui.displayMessage("Nothing to be imported.", buttons=('OK',), severity=hou.severityType.Warning)
			return

		if self.onegeoonefile.isChecked():
			for i, file in enumerate(self.list_files, 0):
				filename = file.split("/")[-1]
				for i in self.ext:
					filename = filename.rsplit(i, 1)[0]
				filename = filename.replace("$", "")
				geo = hou.node("/obj").createNode("geo", run_init_scripts=False, node_name=filename + "_geo")
				geo.setDisplayFlag(False)
				geo.moveToGoodPosition()
				if file.endswith(".abc"):
					file_node = geo.createNode("alembic", node_name=filename)
					file_node.parm("fileName").set(file)
				else:
					file_node = geo.createNode("file", node_name=filename)
					file_node.parm("file").set(file)
		else:
			geo = hou.node("/obj").createNode("geo", run_init_scripts=False, node_name="batch_import")
			geo.setDisplayFlag(False)
			geo.setGenericFlag(hou.nodeFlag.DisplayComment,True)
			geo.setComment("Total file(s): " + str(len(self.list_files)) + "\n")
			for i, file in enumerate(self.list_files, 0):
				filename = file.split("/")[-1]
				for i in self.ext:
					filename = filename.rsplit(i, 1)[0]
				filename = filename.replace("$", "")
				if file.endswith(".abc"):
					file_node = geo.createNode("alembic", node_name=filename)
					file_node.parm("fileName").set(file)
				else:
					file_node = geo.createNode("file", node_name=filename)
					file_node.parm("file").set(file)
			geo.layoutChildren()

		hou.ui.displayMessage("Batch import successful", buttons=('OK',), severity=hou.severityType.Message)





w = BatchImport()
w.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
w.show()