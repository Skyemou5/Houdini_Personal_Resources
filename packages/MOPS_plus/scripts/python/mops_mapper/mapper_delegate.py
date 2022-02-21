from PySide2 import QtWidgets, QtCore, QtGui
from mops_mapper import mapper_model, settings
import hou


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


class MapperAttributesDelegate(QtWidgets.QStyledItemDelegate):
    """
    This delegate handles the display of the "Attributes" table.
    Column 0 is attribute names, Column 1 is attribute types.
    Columns 3 and 4 contain the +/- buttons for adding or removing attributes.

    """
    def __init__(self):
        super(MapperAttributesDelegate, self).__init__()


    def paint(self, painter, option, index):
        # establish defaults
        painter.save()
        x = option.rect.left() + 5
        y = option.rect.top() + 10
        w = option.rect.width() - 10
        h = option.rect.height()
        text_rect = QtCore.QRectF(x, y, w, h)
        font = painter.font()
        pen = painter.pen()

        text = ""
        if index.column() < 2:
            if index.column() == 0:
                text = index.data(QtCore.Qt.DisplayRole)
            elif index.column() == 1:
                text = index.data(QtCore.Qt.DisplayRole)

            painter.setFont(font)
            painter.setPen(pen)

            metrics = painter.fontMetrics()
            elide = metrics.elidedText(text, QtCore.Qt.ElideMiddle, w)
            painter.drawText(text_rect, elide)

        else:
            x = option.rect.left()
            y = option.rect.top()
            w = option.rect.width()
            h = option.rect.height()
            btn_rect = QtCore.QRect(x, y, w, h)
            btn = QtWidgets.QStyleOptionButton()
            btn.rect = btn_rect
            if index.column() == 2:
                btn.text = "+"
            elif index.row() > 0:
                btn.text = "-"
            style = QtWidgets.QApplication.style()
            style.drawControl(QtWidgets.QStyle.CE_PushButton, btn, painter)

        painter.restore()

    def sizeHint(self, option, index):
        text = index.data(QtCore.Qt.DisplayRole)
        h = settings.ATTR_SECTION_HEIGHT
        if index.column() == 0:
            # attribute name. return 200px or the ideal width, whichever is larger.
            doc = QtGui.QTextDocument(text)
            w = doc.idealWidth() + 10
            min_width = 160
            out_width = max(min_width, w)
            return QtCore.QSize(out_width, h)
        elif index.column() == 1:
            # attribue type.
            doc = QtGui.QTextDocument(text)
            w = doc.idealWidth() + 30
            min_width = 140
            out_width = max(min_width, w)
            return QtCore.QSize(out_width, h)
        else:
            return QtCore.QSize(h, h)

    def createEditor(self, parent, option, index):
        editor = None
        if index.column() == 0:
            # line edit
            editor = QtWidgets.QLineEdit(parent)
            editor.setText(index.data(QtCore.Qt.DisplayRole))
        elif index.column() == 1:
            # combobox
            editor = QtWidgets.QComboBox(parent)
            for attr in settings.ATTR_TYPES:
                editor.addItem(attr)
            editor.setCurrentText(index.data(mapper_model.AttributeTypeRole))
            editor.activated.connect(self.setData)
        return editor

    def setData(self, editor):
        self.commitData.emit(self.sender())

    def setModelData(self, editor, model, index):
        value = None
        role = QtCore.Qt.EditRole
        if index.column() == 0:
            value = editor.text()
            model.setData(index, value, role)
        if index.column() == 1:
            value = editor.currentText()
            model.setData(index, value, role)


class MapperValuesDelegate(QtWidgets.QStyledItemDelegate):
    """
    creates custom editors with validators depending on the column's datatype.
    """
    def __init__(self):
        super(MapperValuesDelegate, self).__init__()

    def paint(self, painter, option, index):
        # establish defaults
        painter.save()
        text_rect = option.rect.adjusted(5, 5, 0, -5)
        font = painter.font()
        pen = painter.pen()
        bgcolor = settings.COLORS["bg"]["idle"]
        if option.state & QtWidgets.QStyle.State_Selected:
            bgcolor = settings.COLORS["bg"]["selected"]
        bgcolor = QtGui.QColor(bgcolor)
        if not option.state & QtWidgets.QStyle.State_Selected and index.row() % 2 != 0:
            bgcolor = bgcolor.lighter(120)
        painter.setBrush(QtGui.QBrush(bgcolor))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(option.rect)
        painter.restore()

        painter.save()
        datatype = index.data(mapper_model.AttributeTypeRole)

        if index.column() > 1 and datatype == "color":
            value = index.data(QtCore.Qt.DisplayRole)
            parsed = value[1:-1].split(", ")
            r = clamp(int(float(parsed[0]) * 255), 0, 255)
            g = clamp(int(float(parsed[1]) * 255), 0, 255)
            b = clamp(int(float(parsed[2]) * 255), 0, 255)
            color_rect = QtCore.QRectF(option.rect)
            color = QtGui.QColor(r, g, b, 255)
            brush = QtGui.QBrush(color)
            painter.setBrush(brush)
            painter.setPen(QtGui.Qt.NoPen)
            painter.drawRect(color_rect)
            painter.restore()
        else:
            if datatype == "string":
                text_rect = text_rect.adjusted(0, 0, -70, 0)

            text = str(index.data(QtCore.Qt.DisplayRole))
            metrics = painter.fontMetrics()
            elide = metrics.elidedText(text, QtCore.Qt.ElideMiddle, text_rect.width())
            painter.drawText(text_rect, elide)
            if datatype == "string":
                file_rect = QtCore.QRect(option.rect.right()-60, option.rect.top(), 30, 30)
                file_btn = QtWidgets.QStyleOptionButton()
                file_btn.rect = file_rect
                file_btn.icon = QtGui.QIcon(settings.ICONS["file_chooser"])
                file_btn.iconSize = QtCore.QSize(30, 30)
                style = QtWidgets.QApplication.style()
                style.drawControl(QtWidgets.QStyle.CE_PushButton, file_btn, painter)

                op_rect = QtCore.QRect(file_rect.x() + file_rect.width(), option.rect.top(), 30, 30)
                op_btn = QtWidgets.QStyleOptionButton()
                op_btn.rect = op_rect
                op_btn.icon = QtGui.QIcon(settings.ICONS["op_chooser"])
                op_btn.iconSize = QtCore.QSize(30, 30)
                style = QtWidgets.QApplication.style()
                style.drawControl(QtWidgets.QStyle.CE_PushButton, op_btn, painter)

            painter.restore()

    def createEditor(self, parent, option, index):
        # if the attribute is color-type, create a houdini-friendly color picker.
        # if it's a vector3, int, or float, apply a QValidator to ensure that the syntax is correct.
        datatype = index.data(mapper_model.AttributeTypeRole)
        editor = None
        value = index.data(QtCore.Qt.DisplayRole)
        if index.column() > 1 and datatype == "color":
            return None
        elif datatype == "string":
            editor = QtWidgets.QLineEdit(parent)
            editor.setText(str(value))
        elif datatype == "int":
            editor = QtWidgets.QLineEdit(parent)
            editor.setText(str(value))
            validator = QtGui.QIntValidator()
            editor.setValidator(validator)
        elif datatype == "float":
            editor = QtWidgets.QLineEdit(parent)
            editor.setText(str(value))
            validator = QtGui.QDoubleValidator()
            editor.setValidator(validator)
        elif datatype == "vector3":
            editor = QtWidgets.QLineEdit(parent)
            editor.setText(value)
            regex = "\([\d\.]+, [\d\.]+, [\d\.]+\)"
            validator = QtGui.QRegExpValidator(regex)
            editor.setValidator(validator)
        return editor

    def setData(self, editor):
        self.commitData.emit(self.sender())

    def setModelData(self, editor, model, index):
        value = editor.text()
        role = QtCore.Qt.EditRole
        model.setData(index, value, role)
