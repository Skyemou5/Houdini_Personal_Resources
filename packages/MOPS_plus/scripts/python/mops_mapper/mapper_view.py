from PySide2 import QtCore, QtWidgets
from mops_mapper import mapper_model
import hou

class MapperAttributesView(QtWidgets.QTableView):

    row_added = QtCore.Signal("QModelIndex")
    row_removed = QtCore.Signal("QModelIndex")

    def __init__(self, parent=None):
        super(MapperAttributesView, self).__init__(parent)

    def mouseReleaseEvent(self, event):
        # look for button presses in cols 2 or 3... these are to add or remove attributes.
        if event.button() == QtCore.Qt.LeftButton:
            index = self.indexAt(event.pos())
            # print("{},{}".format(index.row(), index.column())
            if index.column() == 2:
                self.row_added.emit(index)
            elif index.column() == 3 and index.row() > 0:
                self.row_removed.emit(index)

        # to prevent the whole selection system from fucking up with our event, we need to kick the event
        # back to the parent class so everything works as expected
        return super(MapperAttributesView, self).mouseReleaseEvent(event)


class MapperItemsView(QtWidgets.QTableView):
    color_change_event = QtCore.Signal("QModelIndex")
    file_choice_event = QtCore.Signal("QModelIndex")
    op_choice_event = QtCore.Signal("QModelIndex")

    def __init__(self, parent=None):
        super(MapperItemsView, self).__init__(parent)
        self.viewport().setAttribute(QtCore.Qt.WA_Hover, True)
        self.setSelectionBehavior(self.SelectRows)
        self.setDragEnabled(True)
        # self.setAcceptDrops(True)
        # self.viewport().setAcceptDrops(True)
        self.setDragDropMode(self.InternalMove)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)
        self.setVerticalScrollMode(QtWidgets.QListView.ScrollPerPixel)

    def mouseReleaseEvent(self, event):
        # if the given cell is color-type, we want to open up a color picker and then tell the model to update.
        if event.button() == QtCore.Qt.LeftButton:
            index = self.indexAt(event.pos())
            datatype = index.data(mapper_model.AttributeTypeRole)
            if datatype == "color":
                # open the color dialog. if a color is picked, emit the signal that the main UI will be listening for.
                self.color_change_event.emit(index)
                return True
            elif datatype == "string":
                # check to see if we clicked on either of the buttons on the right side of the cell.
                # right side -30 px is the op chooser, -60 px is the file chooser.
                cell_rect = self.visualRect(index)
                right_test = QtCore.QRect(cell_rect.left()+cell_rect.width()-30, cell_rect.top(), cell_rect.left()+cell_rect.width(), cell_rect.bottom())
                if right_test.contains(event.pos()):
                    self.op_choice_event.emit(index)
                    return True
                left_test = QtCore.QRect(right_test.left()-30, right_test.top(), right_test.left(), right_test.bottom())
                if left_test.contains(event.pos()):
                    self.file_choice_event.emit(index)
                    return True
        return super(MapperItemsView, self).mouseReleaseEvent(event)
