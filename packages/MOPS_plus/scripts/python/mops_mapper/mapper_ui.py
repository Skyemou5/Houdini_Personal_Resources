from PySide2 import QtWidgets, QtCore, QtGui
import json
from mops_mapper import mapper_model, mapper_delegate, mapper_view, settings
import hou


# TODO: better vector validation?

DEBUG = False


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


class MOPs_Attribute_Mapper(QtWidgets.QWidget):
    def __init__(self):
        super(MOPs_Attribute_Mapper, self).__init__()
        # create shared data structure
        items = list()
        attributes = list()
        self.currentNode = None
        self.currentColorIndex = None

        # create layout
        main_layout = QtWidgets.QVBoxLayout()
        items_view = mapper_view.MapperItemsView()
        items_model = mapper_model.MOPsMapperModel()
        items_proxy = mapper_model.MOPsMapperItemsProxy()
        items_proxy.setSourceModel(items_model)
        items_view.setModel(items_proxy)
        header = items_view.horizontalHeader()
        header.setStretchLastSection(True)
        items_view.verticalHeader().setDefaultSectionSize(settings.ATTR_SECTION_HEIGHT)
        items_view.verticalHeader().hide()
        items_view.setAlternatingRowColors(True)
        add_row_btn = QtWidgets.QPushButton("Add Row")
        add_files_btn = QtWidgets.QPushButton("Add From Files")
        add_ops_btn = QtWidgets.QPushButton("Add From OPs")
        remove_rows_btn = QtWidgets.QPushButton("Remove Selected Rows")
        normalize_btn = QtWidgets.QPushButton("Normalize Attr")
        if DEBUG:
            debug_btn = QtWidgets.QPushButton("Debug")

        buttons_layout = QtWidgets.QVBoxLayout()
        buttons_layout.addWidget(add_row_btn)
        buttons_layout.addWidget(add_files_btn)
        buttons_layout.addWidget(add_ops_btn)
        buttons_layout.addWidget(remove_rows_btn)
        buttons_layout.addWidget(normalize_btn)
        if DEBUG:
            buttons_layout.addStretch()
            buttons_layout.addWidget(debug_btn)

        buttons_layout.addStretch()
        buttons_layout.setSpacing(2)

        items_delegate = mapper_delegate.MapperValuesDelegate()
        items_view.setItemDelegate(items_delegate)

        # attributes view
        attrs_model = mapper_model.MOPsMapperAttributesProxy()
        attrs_view = mapper_view.MapperAttributesView()
        attrs_delegate = mapper_delegate.MapperAttributesDelegate()
        attrs_model.setSourceModel(items_model)
        attrs_view.setModel(attrs_model)
        attrs_view.setItemDelegate(attrs_delegate)
        attrs_view.verticalHeader().setDefaultSectionSize(settings.ATTR_SECTION_HEIGHT)
        attrs_view.verticalHeader().hide()
        attrs_view.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        attrs_view.setShowGrid(False)
        attrs_view.setAlternatingRowColors(True)
        attrs_view.setVerticalScrollMode(QtWidgets.QListView.ScrollPerPixel)
        attrs_header = attrs_view.horizontalHeader()
        attrs_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        attrs_header.resizeSection(2, settings.ATTR_SECTION_HEIGHT)
        attrs_header.resizeSection(3, settings.ATTR_SECTION_HEIGHT)
        attrs_header.setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
        attrs_header.setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)
        attrs_header.hide()

        attrs_layout = QtWidgets.QHBoxLayout()
        attrs_layout.addWidget(attrs_view)
        attrs_layout.addStretch()
        attrs_layout.addLayout(buttons_layout)
        attrs_layout.setStretch(0, 1)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        
        splitter.setStyleSheet("QSplitter::handle:vertical { "
                               "border-style: outset; "
                               "margin-top: 8px; "
                               "margin-bottom: 8px; "
                               "padding: 0px; "
                               "background-color: #494949; "
                               "border-width: 1px;"
                               "border-color: #696969; }"
                               "QSplitter::handle:vertical:hover { "
                               "background-color: #5f5541; }")

        attrs_widget = QtWidgets.QFrame()
        attrs_layout.setContentsMargins(0, 0, 0, 0)
        attrs_widget.setLayout(attrs_layout)
        splitter.addWidget(attrs_widget)
        splitter.addWidget(items_view)
        main_layout.addWidget(splitter)
        splitter.setStretchFactor(0, 1)
        splitter.setHandleWidth(4)

        # main_layout.addWidget(items_view)
        # main_layout.addLayout(attrs_layout)
        # main_layout.setStretch(0, 1)
        
        # wrapper
        wrapper = QtWidgets.QVBoxLayout()
        widget = QtWidgets.QWidget()
        widget.setLayout(main_layout)
        scroll = QtWidgets.QScrollArea()
        wrapper.setContentsMargins(0, 0, 0, 0)
        main_layout.setContentsMargins(4, 4, 4, 4)
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        wrapper.addWidget(scroll)
        self.setLayout(wrapper)
               
        # signals/slots
        add_row_btn.clicked.connect(self.addNewRow)
        remove_rows_btn.clicked.connect(self.removeRows)
        add_files_btn.clicked.connect(self.addRowsFromFiles)
        add_ops_btn.clicked.connect(self.addRowsFromOps)
        attrs_view.row_added.connect(self.addAttribute)
        attrs_view.row_removed.connect(self.removeAttribute)
        items_view.file_choice_event.connect(self.updateFileAttribute)
        items_view.op_choice_event.connect(self.updateOpAttribute)
        items_view.color_change_event.connect(self.updateColorAttribute)
        items_model.dataChanged.connect(self.updateNode)
        items_model.rowsRemoved.connect(self.updateNode)
        normalize_btn.clicked.connect(self.normalizeAttr)
        if DEBUG:
            debug_btn.clicked.connect(self.debug)

        # store things
        self.data = {
            'model': {
                        'items': items_model,
                        'proxy': items_proxy,
                        'attributes': attrs_model,
                     },
            'view':  {
                        'items': items_view,
                        'attributes': attrs_view,
                     },
            'header': header,
            'items': items,
            'attributes': attributes,
            'workingDirectory': None,
        }

        items_view.resizeColumnsToContents()
        attrs_view.resizeColumnsToContents()
        self.showEditors()
        
    def debug(self):
        self.data['model']['items'].debug()
        
    def addNewRow(self, row=None, *args):
        if not row:
            row = self.data['model']['items'].rowCount()
        self.data['model']['items'].insertRow(row)
        self.updateNode()

    def addAttribute(self, index, *args):
        # index here is a QModelIndex.
        out_index = self.data['model']['attributes'].mapToSource(index)
        self.data['model']['items'].insertColumn(out_index.column()+1, "attribute", "string")
        self.data['header'].setStretchLastSection(True)
        self.showEditors()
        self.updateNode()

    def removeAttribute(self, index, *args):
        # index here is a QModelIndex.
        out_index = self.data['model']['attributes'].mapToSource(index)
        self.data['model']['items'].removeColumn(out_index.column())
        self.data['header'].setStretchLastSection(True)
        self.showEditors()
        self.updateNode()

    def removeRows(self, *args):
        indexes = self.data['view']['items'].selectedIndexes()
        # break this down into rows
        rows = list()
        if indexes:
            for i in indexes:
                rows.append(i.row()+2)
        rows = list(set(rows))
        if rows:
            for i in sorted(rows, reverse=True):
                # print("removing row {}".format(i))
                self.data['model']['items'].removeRow(i)
        self.updateNode()

    def updateColorAttribute(self, index, *args):
        # if a color swatch in the view is updated, we have to inform the model here.
        current_color = index.data(QtCore.Qt.DisplayRole)
        parsed = current_color[1:-1].split(", ")
        # hou.ui.selectColor will crash on any builds prior to 18.0.398.
        version = hou.applicationVersion()
        new_picker = True
        if version[0] < 18:
            new_picker = False
        elif version[0] == 18 and version[1] == 0 and version[2] < 398:
            new_picker = False

        col = hou.Color((float(parsed[0]), float(parsed[1]), float(parsed[2])))
        if new_picker:
            new_color = hou.ui.selectColor(col)
        else:
            r = clamp(int(float(parsed[0]) * 255), 0, 255)
            g = clamp(int(float(parsed[1]) * 255), 0, 255)
            b = clamp(int(float(parsed[2]) * 255), 0, 255)
            col = QtGui.QColor(r, g, b, 255)
            new_color = QtWidgets.QColorDialog.getColor(col, self, title="Choose new color...", options=QtWidgets.QColorDialog.DontUseNativeDialog)
        if new_color is not None:
            #if new_color.isValid():
            str_color = ""
            if new_picker:
                str_color = "({}, {}, {})".format(new_color.rgb()[0], new_color.rgb()[1], new_color.rgb()[2])
            else:
                str_color = "({}, {}, {})".format(new_color.redF(), new_color.greenF(), new_color.blueF())
            self.data['model']['proxy'].setData(index, str_color, QtCore.Qt.EditRole)

    def updateFileAttribute(self, index, *args):
        current_file = index.data(QtCore.Qt.DisplayRole)
        current_dir = None
        try:
            current_dir = os.path.dirname(current_file)
        except:
            pass
        # TODO: allow for multiple select. get selected rows from view and update each row in sequence with the selected files
        new_files = hou.ui.selectFile(start_directory=current_dir, title="Select file...", collapse_sequences=False, multiple_select=True, chooser_mode=hou.fileChooserMode.Read)
        if new_files:
            new_files = new_files.split(";")
            rows = list()
            rows.append(index.row())
            indexes = self.data['view']['items'].selectedIndexes()
            for i in indexes:
                rows.append(i.row())
            rows = sorted(list(set(rows)))
            # print(rows)
            # print(new_files)
            for x in range(0, len(rows)):
                this_index = self.data['model']['proxy'].index(rows[x], index.column())
                file = None
                try:
                    file = new_files[x].strip()
                except:
                    pass
                if file:
                    self.data['model']['proxy'].setData(this_index, file, QtCore.Qt.EditRole)
        self.data['view']['items'].clearSelection()

    def updateOpAttribute(self, index, *args):
        current_path = index.data(QtCore.Qt.DisplayRole)
        # print("current path: {}".format(current_path))
        new_nodes = hou.ui.selectNode(relative_to_node=self.currentNode, title="Select node...", multiple_select=True)
        # print(new_node)
        if new_nodes:
            rows = list()
            rows.append(index.row())
            indexes = self.data['view']['items'].selectedIndexes()
            for i in indexes:
                rows.append(i.row())
            rows = sorted(list(set(rows)))
            for x in range(0, len(rows)):
                this_index = self.data['model']['proxy'].index(rows[x], index.column())
                op = None
                try:
                    op = new_nodes[x].strip()
                except:
                    pass
                if op:
                    self.data['model']['proxy'].setData(this_index, op, QtCore.Qt.EditRole)
        self.data['view']['items'].clearSelection()

    def normalizeAttr(self):
        # open up a dialog to pick which float attribute to normalize.
        all_attrs = list()
        for y in range(1, self.data['model']['items'].columnCount()):
            attr = self.data['model']['items'].items[0][y]
            datatype = self.data['model']['items'].items[1][y]
            # print("attr: {}, datatype: {}".format(attr, datatype))
            if datatype == "float":
                all_attrs.append(attr)
        if not all_attrs:
            hou.ui.displayMessage("You must create at least one float-type attribute to normalize.",
                                  title="No float attributes found!")
            return
        attr_choice = hou.ui.selectFromList(all_attrs, exclusive=True, title="Attribute to Modify",
                                            message="Select the float-type attribute to normalize.",
                                            column_header="Attributes", clear_on_cancel=True)
        if not attr_choice:
            return
        attr_choice = all_attrs[attr_choice[0]]
        attr_index = self.data['model']['items'].items[0].index(attr_choice)
        # evenly distribute values for this attribute for all rows.
        count = len(self.data['model']['items'].items)
        step = 1.0 / float(count-2)
        u = 0.0
        for x in range(2, count):
            index = self.data['model']['items'].index(x, attr_index)
            self.data['model']['items'].setData(index, str(u), QtCore.Qt.EditRole)
            u += step

    def addRowsFromFiles(self):
        # open up a houdini dialog to load one or more files.
        # open another modal to get the attribute name to add to.
        # for each file, add a new row to the table and set the attribute value to be the file path.
        all_attrs = list()
        for y in range(2, self.data['model']['items'].columnCount()):
            attr = self.data['model']['items'].items[0][y]
            datatype = self.data['model']['items'].items[1][y]
            if datatype == "string":
                all_attrs.append(attr)
        if not all_attrs:
            hou.ui.displayMessage("You must create at least one string-type attribute to add file paths to.", title="No string attributes found!")
            return
        files = hou.ui.selectFile(start_directory=self.data["workingDirectory"], title="Select files to add...", collapse_sequences=False, multiple_select=True, chooser_mode=hou.fileChooserMode.Read)
        if not files:
            return
        attr_choice = hou.ui.selectFromList(all_attrs, exclusive=True, title="Attribute to Modify", message="Select the string-type attribute to add filenames to.", column_header="Attributes", clear_on_cancel=True)
        if not attr_choice:
            return
        attr_choice = all_attrs[attr_choice[0]]
        # print("Attribute: {}".format(attr_choice))
        # get the index of the chosen attribute in the table.
        attr_index = self.data['model']['items'].items[0].index(attr_choice)
        # now iterate through each file and add rows.
        files = [f.strip() for f in files.split(';')]
        # first: if we only have three rows, and row 2 is default, remove it.
        if len(self.data['model']['items'].items) == 3:
            if self.data['model']['items'].items[2][0] == "0" and self.data['model']['items'].items[2][1] == "0" and self.data['model']['items'].items[2][2] == "default":
                self.data['model']['items'].removeRow(2)
        for file in files:
            self.addNewRow()
            index = self.data['model']['items'].createIndex(self.data['model']['items'].rowCount()-1, attr_index)
            self.data['model']['items'].setData(index, file, QtCore.Qt.EditRole)
        self.updateNode()

    def addRowsFromOps(self):
        all_attrs = list()
        for y in range(2, self.data['model']['items'].columnCount()):
            attr = self.data['model']['items'].items[0][y]
            datatype = self.data['model']['items'].items[1][y]
            if datatype == "string":
                all_attrs.append(attr)
        if not all_attrs:
            hou.ui.displayMessage("You must create at least one string-type attribute to add file paths to.",
                                  title="No string attributes found!")
            return
        ops = hou.ui.selectNode(relative_to_node=self.currentNode, title="Select nodes to add...", multiple_select=True)
        if not ops:
            return
        attr_choice = hou.ui.selectFromList(all_attrs, exclusive=True, title="Attribute to Modify",
                                            message="Select the string-type attribute to add filenames to.",
                                            column_header="Attributes", clear_on_cancel=True)
        if not attr_choice:
            return
        attr_choice = all_attrs[attr_choice[0]]
        # first: if we only have three rows, and row 2 is default, remove it.
        if len(self.data['model']['items'].items) == 3:
            if self.data['model']['items'].items[2][0] == "0" and self.data['model']['items'].items[2][1] == "0" and \
                    self.data['model']['items'].items[2][2] == "default":
                self.data['model']['items'].removeRow(2)
        # print("Attribute: {}".format(attr_choice))
        # get the index of the chosen attribute in the table.
        attr_index = self.data['model']['items'].items[0].index(attr_choice)
        for op in ops:
            self.addNewRow()
            index = self.data['model']['items'].createIndex(self.data['model']['items'].rowCount()-1, attr_index)
            # self.data['model']['items'].setData(index, "/"+op.strip("/"), QtCore.Qt.EditRole)
            self.data['model']['items'].setData(index, op, QtCore.Qt.EditRole)
        self.updateNode()

    def showEditors(self):
        # open persistent editors on all appropriate indices.
        model = self.data['model']['attributes']
        rows = model.rowCount()
        cols = model.columnCount()
        view = self.data['view']['attributes']
        for x in range(0, rows):
            for y in range(1, cols):
                index = model.createIndex(x, y)
                view.openPersistentEditor(index)

    def setCurrentNode(self, node):
        # tell this thing what node it should be saving/loading data from.
        self.currentNode = node
        # print("current node: {}".format(node.name()))
        # load data from this node and populate the model.
        tabledatastr = node.parm("tabledata").eval()
        tabledata = json.loads(tabledatastr)
        self.data['model']['items'].resetToState(tabledata)
        # brute force reset the attributes model.
        self.data['model']['attributes'].sourceModelReset()
        self.showEditors()

    def updateNode(self):
        # when the internal model is updated, this function sets the new tabledata string
        # for the current node, saving any modifications.
        # print("updating json")
        tabledata = self.data['model']['items'].items
        tabledatastr = json.dumps(tabledata)
        self.currentNode.parm("tabledata").set(tabledatastr)
        # for some reason the callback isn't firing...?
        kwargs = {"node": self.currentNode}
        self.currentNode.hdaModule().onDataChanged(kwargs)

