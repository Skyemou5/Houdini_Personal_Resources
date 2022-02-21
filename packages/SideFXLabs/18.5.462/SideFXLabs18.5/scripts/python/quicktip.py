import hou
import os
import csv
import random
from hutil.Qt.QtCore import *
from hutil.Qt.QtGui import *
from hutil.Qt.QtWidgets import *


class Tip_Dialog(QDialog):
    def __init__(self, parent):
        super(Tip_Dialog, self).__init__(parent)

        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Quick Tips!")

        self.csvfile = hou.expandString("$SIDEFXLABS/misc/tips/Tip_Data.csv")
        self.numtips = 0
        self.currenttip = 0
        self.build_ui()
        self.Randomize()
        self.UpdateTip()

    def Randomize(self):
        with open(self.csvfile,"r") as data:
            self.numtips = sum(1 for row in data)
        self.currenttip = random.randint(0, self.numtips)
        

    def TipAtIndex(self, index):
        with open(self.csvfile,"r") as data:
            csv_reader = csv.reader(data)
            tips = list(csv_reader)
            return tips[index][0]

    def UpdateTip(self):
        self.tip_label.setText("({0}/{1}) {2}".format(self.currenttip+1, self.numtips, self.TipAtIndex(self.currenttip) ))

    def closeEvent(self, event):
        pass
        
    def RandomTip(self):
        self.Randomize()
        self.UpdateTip()
        

    def PrevTip(self):
        self.currenttip = max(0, self.currenttip-1)
        self.UpdateTip()

    def NextTip(self):
        self.currenttip = min(self.numtips-1, self.currenttip+1)
        self.UpdateTip()


    def build_ui(self):

      self.setMinimumSize(650, 100)

      layout = QVBoxLayout()

      self.tip_label = QLabel("Some Tip")
      tip_label_layout = QHBoxLayout()
      tip_label_layout.addWidget(self.tip_label)
      self.tip_label.setWordWrap(True)

      Prev_btn = QPushButton("Previous")
      Prev_btn.clicked.connect(self.PrevTip)

      Next_btn = QPushButton("Next")
      Next_btn.clicked.connect(self.NextTip)

      Random_btn = QPushButton("Random")
      Random_btn.clicked.connect(self.RandomTip)

      buttons_layout = QHBoxLayout()
      buttons_layout.addWidget(Prev_btn)
      buttons_layout.addWidget(Next_btn)
      buttons_layout.addWidget(Random_btn)

      layout.addLayout(tip_label_layout)
      layout.addLayout(buttons_layout)

      self.setLayout(layout)


def ShowQuickTip():
  dialog = Tip_Dialog(hou.ui.mainQtWindow())
  dialog.show()