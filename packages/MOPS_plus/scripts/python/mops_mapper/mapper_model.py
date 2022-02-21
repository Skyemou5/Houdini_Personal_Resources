import pickle
from PySide2 import QtCore
from future.utils import iteritems

ObjectRole = QtCore.Qt.UserRole + 1
ValuesRole = QtCore.Qt.UserRole + 2
TypesRole = QtCore.Qt.UserRole + 3
AttributeNameRole = QtCore.Qt.UserRole + 4
AttributeTypeRole = QtCore.Qt.UserRole + 5


class MOPsMapperModel(QtCore.QAbstractTableModel):
    # items[0] is a list of attributes.
    # items[1] is a list of attribute types.
    # all further items are actual lists of values for these attributes.
    def __init__(self, parent=None):
        super(MOPsMapperModel, self).__init__(parent)
        self.items = list()
        self.items.append(["index", "key", "attribute"])
        self.items.append(["int", "int", "string"])
        self.items.append(["0", "0", "default"])
        
    def debug(self):
        print("\n====================")
        print("Qt Model:")
        for i in self.items:
            print(i)
        print("\n")

        
    def data(self, index, role):
        col = index.column()
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole or role == QtCore.Qt.ToolTipRole:
            item = self.items[index.row()]
            if col == 0:
                return str(index.row()-2)
            return item[col]
        elif role == AttributeNameRole:
            item = self.items[0]
            return item[col]
        elif role == AttributeTypeRole:
            item = self.items[1]
            return item[col]
        return None

    def resetToState(self, data):
        # completely reset the model to match a new items list.
        self.beginResetModel()
        self.items[:] = []
        for i in data:
            self.items.append(i)
        self.endResetModel()
        
    def rowCount(self, parent=None):
        return len(self.items)
        
    def columnCount(self, parent=None):
        return len(self.items[0])
        
    def setData(self, index, value, role):
        row = index.row()
        col = index.column()
        if role == AttributeNameRole:
            row = 0
        elif role == AttributeTypeRole:
            row = 1
        old_value = self.data(index, role)
        # convert the data to a formatted string if it's a vector or color.
        if isinstance(value, (list, tuple)):
            value = "({}, {}, {})".format(value[0], value[1], value[2])
        self.items[row][col] = value
        out_index = self.createIndex(row, col)
        self.dataChanged.emit(out_index, out_index, role)
        # if we just changed the attribute type, we need to update all values for that attribute.
        if row == 1:
            self.changeAttributeType(col, old_value, value)
        return True
        
    def insertRow(self, row, values=None):
        # validate that the item has all the requisite attributes.
        attrs_count = len(self.items[0])
        if values is None:
            values = list()
        col = 0
        while(len(values) < attrs_count):
            default = "0"
            attr_type = self.items[1][col]
            if attr_type == "string":
                default = ""
            elif attr_type in ("vector3", "color"):
                default = "(0.0, 0.0, 0.0)"
            if col < 2:
                # this is the row index
                default = row-2
            values.append(default)
            col += 1

        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self.items.insert(row, values)
        self.endInsertRows()

    def insertRows(self, row, count, parent=QtCore.QModelIndex()):
        # required for internal move
        # print("inserting rows {}-{}".format(row, row+count-1))
        self.beginInsertRows(QtCore.QModelIndex(), row, row+count-1)
        for x in range(row, row+count):
            data = list()
            for y in range(self.columnCount()):
                data.append("")
            self.items.insert(x, data)
        # print(self.items)
        self.endInsertRows()
        return True

    def removeRow(self, row):
        self.beginRemoveRows(QtCore.QModelIndex(), row, row)
        self.items.pop(row)
        self.endRemoveRows()

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        # required for internal move
        # print("removing rows {}-{}".format(row, row+count-1))
        self.beginRemoveRows(QtCore.QModelIndex(), row, row+count-1)
        for x in range(row, row+count):
            self.items.pop(row)
        self.endRemoveRows()
        # print(self.items)
        return True

    # def moveRows(self, srcParent, row, count, dstParent, dstRow):
    #     # required for internal move
    #     print("calling moveRows")
    #     self.beginMoveRows(QtCore.QModelIndex(), row, row+count-1, QtCore.QModelIndex(), dstRow)
    #     for x in range(0, count):
    #         copy_data = self.items[row]
    #         # adjust index
    #         copy_data[0] = dstRow+x
    #         self.items.insert(dstRow+x, copy_data)
    #         index = row+1
    #         if dstRow > row:
    #             index = row
    #         self.items.pop(index)
    #     self.endMoveRows()
    #     return True
        
    def insertColumn(self, col=None, attribute="attribute", type="string"):
        # every item in self.items will need to have this new attribute inserted.
        # row 0 will get the attribute name. row 1 will get the type.
        if col is None:
            col = self.columnCount()
        # if another attribute by the same name already exists, we need to append a suffix.
        attrs = self.items[0]
        suffix = 1
        if attribute in attrs:
            while attribute+str(suffix) in attrs:
                suffix += 1
            attribute = attribute + str(suffix)

        self.beginInsertColumns(QtCore.QModelIndex(), col, col)
        for x in range(0, len(self.items)):
            if x==0:
                # update attribute name
                self.items[x].insert(col, attribute)
            elif x==1:
                # update attribute type
                self.items[x].insert(col, type)
            else:
                # update items with default attribute value
                default = 0
                if type == "string":
                    default = ""
                self.items[x].insert(col, default)
        self.endInsertColumns()
        
    def removeColumn(self, column):
        self.beginRemoveColumns(QtCore.QModelIndex(), column, column)
        # pop the column from all rows.
        for x in range(0, len(self.items)):
            self.items[x].pop(column)
        self.endRemoveColumns()
        
    def flags(self, index):
        f = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled
        if index.row() == -1:
            f = f | QtCore.Qt.ItemIsDropEnabled
        if index.column() > 0 and index.row() > 1 and index.data(AttributeTypeRole) != "color":
            f = f | QtCore.Qt.ItemIsEditable
        return f

    def reset(self):
        self.beginResetModel()
        self.items[:] = []
        self.endResetModel()
        
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.items[0][section]

    def setHeaderData(self, section, orientation, value, role):
        if orientation == QtCore.Qt.Horizontal:
            self.items[0][section] = value
            self.headerDataChanged.emit(QtCore.Qt.Horizontal, section, section)

    def supportedDropActions(self):
        return QtCore.Qt.MoveAction

    def changeAttributeType(self, column, old_type, new_type):
        """
        convert every item in self.items over to the newly-set attribute type.
        :param column: the column index of the attribute that was modified.
        :param old_type: the previous datatype.
        :param new_type: the new datatype.
        :return: None
        """
        for row in range(2, len(self.items)):
            index = self.createIndex(row, column)
            value = self.data(index, role=QtCore.Qt.DisplayRole)
            new_value = value
            if old_type == "int":
                if new_type == "string":
                    new_value = str(value)
                elif new_type == "float":
                    new_value = float(value)
                elif new_type == "vector3":
                    new_value = (value, 0.0, 0.0)
                elif new_type == "color":
                    new_value = (value, 0.0, 0.0)
            elif old_type == "float":
                if new_type == "int":
                    new_value = int(value)
                elif new_type == "string":
                    new_value = str(value)
                elif new_type == "vector3":
                    new_value = (value, 0.0, 0.0)
                elif new_type == "color":
                    new_value = (value, 0.0, 0.0)
            elif old_type == "string":
                if new_type == "int":
                    try:
                        new_value = int(float(value))
                    except ValueError:
                        new_value = 0
                elif new_type == "float":
                    try:
                        new_value = float(value)
                    except ValueError:
                        new_value = 0.0
                elif new_type == "vector3":
                    # try to parse it?
                    try:
                        new_value = value[1:-1].split(", ")
                        if len(new_value) != 3:
                            new_value = (0.0, 0.0, 0.0)
                    except:
                        new_value = (0.0, 0.0, 0.0)
                elif new_type == "color":
                    try:
                        new_value = value[1:-1].split(", ")
                        if len(new_value) != 3:
                            new_value = (0.0, 0.0, 0.0)
                    except:
                        new_value = (0.0, 0.0, 0.0)
            elif old_type == "vector3":
                # parse the current string into a tuple.
                value_list = value[1:-1].split(", ")
                if new_type == "int":
                    new_value = int(float(value_list[0]))
                elif new_type == "float":
                    new_value = value_list[0]
                elif new_type == "color":
                    new_value = "({}, {}, {})".format(value_list[0], value_list[1], value_list[2])
                elif new_type == "string":
                    new_value = "({}, {}, {})".format(value_list[0], value_list[1], value_list[2])
            elif old_type == "color":
                # parse the current string into a tuple.
                value_list = value[1:-1].split(", ")
                if new_type == "int":
                    new_value = int(float(value_list[0]))
                elif new_type == "float":
                    new_value = value_list[0]
                elif new_type == "vector3":
                    new_value = "({}, {}, {})".format(value_list[0], value_list[1], value_list[2])
                elif new_type == "string":
                    new_value = "({}, {}, {})".format(value_list[0], value_list[1], value_list[2])
            # set data for the new item.
            self.setData(index, new_value, QtCore.Qt.EditRole)

    # def dropMimeData(self, data, action, row, col, parent):
    #     # row = parent.row()
    #     # col = 0
    #     # if row == -1:
    #     #     row = self.rowCount()
    #     response = super(MOPsMapperModel, self).dropMimeData(data, action, row, 0, parent)
    #     # print("dropping mime data at row {}".format(parent.row()))
    #     return response


class MOPsMapperItemsProxy(QtCore.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(MOPsMapperItemsProxy, self).__init__(parent)

    def filterAcceptsRow(self, row, parent=QtCore.QModelIndex()):
        if row > 1:
            return True
        return False

    def data(self, index, role):
        source_model = self.sourceModel()
        source_index = self.mapToSource(index)
        return source_model.data(source_index, role)

    def setData(self, index, value, role):
        source_model = self.sourceModel()
        source_index = self.mapToSource(index)
        source_model.setData(source_index, value, role)
        self.dataChanged.emit(index, index, role)
        return True

    def dropMimeData(self, data, action, row, col, parent):
        if row == -1:
            row = self.rowCount()
        response = super(MOPsMapperItemsProxy, self).dropMimeData(data, action, row, 0, parent)
        return response


class MOPsMapperAttributesProxy(QtCore.QAbstractProxyModel):
    def __init__(self, parent=None):
        super(MOPsMapperAttributesProxy, self).__init__(parent)

    def setSourceModel(self, new_model):
        # the QAbstractProxyModel doesn't do any signal forwarding... at all.
        # we'll have to manually connect signals from the source model to this model.
        self.beginResetModel()
        super(MOPsMapperAttributesProxy, self).setSourceModel(new_model)
        new_model.modelReset.connect(self.sourceModelReset)
        new_model.dataChanged.connect(self.sourceDataChanged)
        new_model.columnsInserted.connect(self.sourceColumnsInserted)
        new_model.columnsRemoved.connect(self.sourceColumnsInserted)
        self.endResetModel()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return self.sourceModel().columnCount()-1

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 4

    def mapToSource(self, proxyindex):
        # map proxy index to source index.
        source_model = self.sourceModel()
        row = proxyindex.row()
        col = proxyindex.column()
        out_index = source_model.createIndex(col, row+1)
        return out_index

    def mapFromSource(self, sourceindex):
        # map source index to proxy index.
        row = sourceindex.row()
        col = sourceindex.column()
        out_index = self.createIndex(col-1, row)
        return out_index

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if row < 0 or row > self.rowCount() - 1 or column < 0 or column > self.columnCount() - 1:
            return QtCore.QModelIndex()
        return self.createIndex(row, column)

    def parent(self, index):
        return QtCore.QModelIndex()

    def data(self, index, role):
        source_index = self.mapToSource(index)
        if index.column() < 2:
            return self.sourceModel().data(source_index, role)
        return None

    def setData(self, index, value, role):
        source_index = self.mapToSource(index)
        success = self.sourceModel().setData(source_index, value, role)
        if(index.column() == 0):
            # also update header data
            self.sourceModel().setHeaderData(source_index.column(), QtCore.Qt.Horizontal, value, role)
        return success

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return "Attribute"
                elif section == 1:
                    return "Type"
        return None

    def insertRow(self, row, parent=QtCore.QModelIndex()):
        test_index = self.createIndex(row, 0)
        out_index = self.mapToSource(test_index)
        self.sourceModel().insertColumn(out_index.column())
        return True

    def flags(self, index):
        if index.column() < 2:
            f = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
            datatype = self.data(index, AttributeTypeRole)
            if datatype != "color":
                f = f | QtCore.Qt.ItemIsEditable
            elif datatype == "color" and index.column() == 0:
                f = f | QtCore.Qt.ItemIsEditable
            return f
        return QtCore.Qt.NoItemFlags

    def sourceDataChanged(self, topLeft, bottomRight, roles):
        row_min = 99999
        row_max = 0
        col_min = 99999
        col_max = 0
        valid_index = False
        for x in range(topLeft.row(), bottomRight.row()):
            for y in range(topLeft.column(), bottomRight.column()):
                index = self.sourceModel().createIndex(x, y)
                this_index = self.mapFromSource(index)
                if not this_index.isValid():
                    continue
                row_min = min(row_min, this_index.row())
                row_max = max(row_max, this_index.row())
                col_min = min(col_min, this_index.column())
                col_max = max(col_max, this_index.column())
                valid_index = True
        if valid_index:
            this_topLeft = self.createIndex(row_min, col_min)
            this_topRight = self.createIndex(row_max, col_max)
            self.dataChanged.emit(this_topLeft, this_topRight, roles)

    def sourceColumnsInserted(self, parent, start, end):
        # this is way brute force but it seems to work?
        start_index = self.createIndex(0, 0)
        end_index = self.createIndex(self.rowCount()-1, self.columnCount()-1)
        self.layoutChanged.emit()
        self.dataChanged.emit(start_index, end_index, (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole))

    def sourceModelReset(self):
        self.beginResetModel()
        self.endResetModel()

