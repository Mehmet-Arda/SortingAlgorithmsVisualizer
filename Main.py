import sys

from PyQt5 import QtGui, QtWidgets,QtCore
from PyQt5.QtCore import QEvent,Qt,QEvent

from PyQt5.QtWidgets import QMainWindow, QApplication, QSlider , QLabel,QLineEdit,QSizePolicy,QGraphicsDropShadowEffect,QSizeGrip
from MainWindow import Ui_MainWindow
from PyQt5.QtGui import QIntValidator,QFont,QFontDatabase,QColor,QIcon,QMouseEvent


import time
import numpy as np
import random

import math
import threading

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class TrackedArray():

    def __init__(self, arr):
        self.arr = np.copy(arr)
        self.reset()

    def track(self, key, access_type):

        self.indices.append(key)
        self.values.append(self.arr[key])
        self.access_type.append(access_type)
        self.full_copies.append(np.copy(self.arr))

    def getActivity(self, index=None):

        if (index == None):
            return [(i, op) for (i, op) in zip(self.indices, self.access_type)]
        else:
            return (self.indices[index], self.access_type[index])
        
      

    def reset(self):

        self.full_copies = []
        self.access_type = []
        self.indices = []
        self.values = []

    def __getitem__(self, key):
        
        self.track(key, "get")
        return self.arr.__getitem__(key)

    def __setitem__(self, key, value):
        
        self.track(key, "set")
        return self.arr.__setitem__(key, value)

    def __len__(self):

        return self.arr.__len__()



class Main(QMainWindow):

    def __init__(self):

        super(Main, self).__init__()

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        disabledBackground="#737373"
        disabledBorderColor="#A8A29E"

        enabledBackground="#1E293B"
        enabledBorderColor="white"

        id = QFontDatabase.addApplicationFont(":/fonts/fonts/Quicksand-Medium.ttf")
        
        families = QFontDatabase.applicationFontFamilies(id)
        
        self.font0=QFont(families[0],14)
        self.font1=QFont(families[0],13)
        self.font2=QFont(families[0],11)
        self.font3=QFont(families[0],9)
        self.font4=QFont(families[0],9)
        
        self.ui.frame_left_side_panel.setStyleSheet("border-radius:0px;")
        self.ui.frame_application_header.setStyleSheet("border-top-right-radius:8px; border-top-left-radius:8px;")
        self.ui.frame_left_side_panel.setStyleSheet(" border-bottom-left-radius:8px;")

        self.ui.label_application_title.setFont(self.font0)
        self.ui.lbl_animation_speed.setFont(self.font2)
        self.ui.lbl_list_create_title.setFont(self.font2)
        self.ui.radioButton_manuel_list.setFont(self.font3)
        self.ui.radioButton_random_list.setFont(self.font3)
        self.ui.btn_manuel_list_remove_item.setFont(self.font3)
        self.ui.btn_manuel_list_remove_all_items.setFont(self.font3)

        self.ui.lineEdit_manuel_list_0.setFont(self.font3)

        self.ui.lbl_min.setFont(self.font3)
        self.ui.lbl_max.setFont(self.font3)
        self.ui.lbl_length.setFont(self.font3)

        self.ui.frame_random_list_label_container.setMinimumWidth(210)
        
        self.ui.lineEdit_random_list_min.setFont(self.font3)
        self.ui.lineEdit_random_list_max.setFont(self.font3)
        self.ui.lineEdit_random_list_length.setFont(self.font3)
        self.ui.lbl_validation_message.setFont(self.font3)
        
        self.ui.lbl_sorting_algorithms_title.setFont(self.font3)
        self.ui.lbl_sorting_graph_type_title.setFont(self.font3)

        for x in range(0,self.ui.frame_sorting_algorithms.layout().count()):
            self.ui.frame_sorting_algorithms.layout().itemAt(x).widget().setFont(self.font3)

        for x in range(0,self.ui.frame_sorting_graph_type.layout().count()):
            self.ui.frame_sorting_graph_type.layout().itemAt(x).widget().setFont(self.font3)

        for x in range(0,self.ui.frame.layout().count()):
            self.ui.frame.layout().itemAt(x).widget().setFont(self.font3)

        for x in range(0,self.ui.frame_2.layout().count()):
            self.ui.frame_2.layout().itemAt(x).widget().setFont(self.font3)




        for x in range(0,self.ui.frame_3.layout().count()):
            self.ui.frame_3.layout().itemAt(x).widget().setFont(self.font4)

        for x in range(0,self.ui.frame_4.layout().count()):
            self.ui.frame_4.layout().itemAt(x).widget().setFont(self.font4)


        for x in range(0,self.ui.frame_5.layout().count()):
            self.ui.frame_5.layout().itemAt(x).widget().setFont(self.font4)


        for x in range(0,self.ui.frame_comparison_count_container.layout().count()):
            self.ui.frame_comparison_count_container.layout().itemAt(x).widget().setFont(self.font4)


        self.ui.lbl_complexity_analysis_title.setFont(self.font4)

        
        


        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow=QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0,83,157,550))

        self.ui.centralwidget.setGraphicsEffect(self.shadow)

       

        self.ui.btn_minimize.clicked.connect(lambda:self.showMinimized())

        self.ui.btn_close.clicked.connect(self.closeWindow)

        def moveWindow(e):

            ctrl=True

            if self.isMaximized()==False:
                if e.buttons() == Qt.LeftButton:

                    try:
                        self.move(self.pos()+e.globalPos()-self.clickPosition)
                    except:
                        ctrl=False

                    if ctrl:
                        self.clickPosition=e.globalPos()
                        e.accept()


        self.ui.frame_application_header.mouseMoveEvent=moveWindow

        QSizeGrip(self.ui.btn_size_grip)

        

        self.ui.btn_restore_maximize.clicked.connect(self.RestoreMaximizeWindow)
        self.ui.btn_restore_maximize.setIcon(QtGui.QIcon(":/icons/icons/maximize.png"))

        self.ui.btn_create.setEnabled(False)
        self.ui.btn_start.setEnabled(False)
        self.ui.btn_pause_resume.setEnabled(False)
        self.ui.btn_reset.setEnabled(False)

        self.ui.lineEdit_random_list_min.installEventFilter(self)
        self.ui.lineEdit_random_list_max.installEventFilter(self)
        self.ui.lineEdit_random_list_length.installEventFilter(self)

        self.ui.lineEdit_random_list_min.textChanged.connect(self.RandomListMinMaxLength)
        self.ui.lineEdit_random_list_max.textChanged.connect(self.RandomListMinMaxLength)
        self.ui.lineEdit_random_list_length.textChanged.connect(self.RandomListMinMaxLength)

        self.ui.lineEdit_random_list_min.setMaxLength(4)
        self.ui.lineEdit_random_list_max.setMaxLength(4)
        self.ui.lineEdit_random_list_length.setMaxLength(4)

        self.ui.btn_manuel_list_remove_item.clicked.connect(self.ManuelListRemoveItem)

        self.ui.btn_manuel_list_remove_all_items.clicked.connect(self.ManuelListRemoveAllItems)

        self.ui.radioButton_random_list.setChecked(False)

        self.ui.frame_random_list.setEnabled(False)
        self.ui.frame_manuel_list.setEnabled(False)


        self.ui.radioButton_manuel_list.clicked.connect(self.onClickedManuelListRadio)
        self.ui.radioButton_random_list.clicked.connect(self.onClickedRandomListRadio)
        self.ui.radioButton_manuel_list.setChecked(False)
        self.ui.radioButton_random_list.setChecked(False)


        self.ui.lineEdit_random_list_min.setValidator(QIntValidator(-1000,1000,self))
        self.ui.lineEdit_random_list_max.setValidator(QIntValidator(-1000,1000,self))
        self.ui.lineEdit_random_list_length.setValidator(QIntValidator(0,100,self))

        

        self.ManuelListLineEdit=self.ui.lineEdit_manuel_list_0

        

        self.ManuelListLineEdit.setValidator(QIntValidator(-1000,1000,self))

        self.ManuelListLineEdit.installEventFilter(self)

        self.ManuelListLineEdit.textChanged.connect(self.ManuelListTextChangedValidation)
        


       
        self.ui.btn_create.clicked.connect(self.CreateGraph)

        self.ui.btn_start.clicked.connect(self.StartVisualization)

        self.ui.btn_pause_resume.clicked["bool"].connect(self.PauseResumeAnimation)

        self.ui.btn_reset.clicked.connect(self.ResetGraph)

        self.ui.horizontalSlider_animation_speed.valueChanged.connect(self.ChangeAnimationSpeed)

        self.speed=60

        self.ui.horizontalSlider_animation_speed.setEnabled(True)
        self.isAnimationStarted=False
        self.speedChanged=False

        self.isAnimationResuming=False

        self.isAnimationReseted=True


        self.sortingAlgorithmIndex=1
        self.graphType=1


        self.sortingAlgorithmAndGraphTypeList=self.ui.frame_sorting_algorithms.findChildren(QtWidgets.QRadioButton)+self.ui.frame_sorting_graph_type.findChildren(QtWidgets.QRadioButton)


        for x in self.sortingAlgorithmAndGraphTypeList:
            
            x.toggled.connect(self.SortingAlgorithmAndGraphTypeSelection)

    
        self.ylimMaxIncreaseAmount=1

        self.comparisonCount=0

        self.comparisonCopyArray=[]

        self.compCountIndex=0
        self.interval=3

        self.unsortedColor="#A8A29E"
        self.sortedColor="#15803D"
        self.edgeColor="#57534E"


        self.stemMarkerFaceColor="grey"
        self.stemMarkerEdgeColor="black"

        self.stemMarkerEdgeWidth=1
        self.stemStemLinesColor="grey"
        self.stemBaseLineColor="grey"

        self.stemLineFormat="--"
        self.stemMarkerFormat="o"


        self.getOperationColor="#EA580C"
        self.setOperationColor="#22C55E"

        self.alpha=1
        self.linewidth=1


        self.graphColor=self.unsortedColor

        self.validationControl=False


        


    def closeWindow(self):

        try:
            self.t.cancel()

        except:
            print("Zamanlayıcı kapalı")

        self.close() 

        

        

    def mousePressEvent(self,event):

        self.clickPosition=event.globalPos()


    def RestoreMaximizeWindow(self):

        if self.isMaximized():
            self.showNormal()

            self.ui.btn_restore_maximize.setIcon(QtGui.QIcon(":/icons/icons/maximize.png"))

        else:

            self.showMaximized()
            self.ui.btn_restore_maximize.setIcon(QtGui.QIcon(":/icons/icons/minimize.png"))


        

    def SortingAlgorithmAndGraphTypeSelection(self):

        rb = self.sender()

        oldGraphType=self.graphType

        match rb.objectName():

            case "radioButton_selection_sort": 
                self.sortingAlgorithmIndex=0
                self.ui.lbl_best_case_equation.setText("n<sup>2</sup>")
                self.ui.lbl_average_case_equation.setText("n<sup>2</sup>")
                self.ui.lbl_worst_case_equation.setText("n<sup>2</sup>")

            case "radioButton_bubble_sort": 
                self.sortingAlgorithmIndex=1
                self.ui.lbl_best_case_equation.setText("n")
                self.ui.lbl_average_case_equation.setText("n<sup>2</sup>")
                self.ui.lbl_worst_case_equation.setText("n<sup>2</sup>")

            case "radioButton_insertion_sort": 
                self.sortingAlgorithmIndex=2
                self.ui.lbl_best_case_equation.setText("n")
                self.ui.lbl_average_case_equation.setText("n<sup>2</sup>")
                self.ui.lbl_worst_case_equation.setText("n<sup>2</sup>")
            case "radioButton_merge_sort": 
                self.sortingAlgorithmIndex=3
                self.ui.lbl_best_case_equation.setText("n.log(n)")
                self.ui.lbl_average_case_equation.setText("n.log(n)")
                self.ui.lbl_worst_case_equation.setText("n.log(n)")

            case "radioButton_quick_sort": 
                self.sortingAlgorithmIndex=4
                self.ui.lbl_best_case_equation.setText("n.log(n)")
                self.ui.lbl_average_case_equation.setText("n.log(n)")
                self.ui.lbl_worst_case_equation.setText("n<sup>2</sup>")

            case "radioButton_scatter_graph": self.graphType=0
            case "radioButton_bar_graph": self.graphType=1
            case "radioButton_stem_graph": self.graphType=2


        if oldGraphType != self.graphType:

            self.ButtonsEnableDisable(self.ui.btn_start,False)

            self.ui.MplWidget.canvas.axes.cla()

            self.ui.MplWidget.canvas.draw()

            self.ButtonsEnableDisable(self.ui.btn_reset,False)
            self.ui.btn_reset.setText("Sıfırla")




        

    def ManuelListTextChangedValidation(self):

        if self.isAnimationReseted:

            ManuelListLineEditCount=self.ui.frame_manuel_list.layout().count()

            ctrl=True

            for x in range(ManuelListLineEditCount):

                if self.ui.frame_manuel_list.layout().itemAt(x).widget().text()=="" or ManuelListLineEditCount<=1:
    
                    ctrl=False
                    self.ButtonsEnableDisable(self.ui.btn_start,False)
                    self.ButtonsEnableDisable(self.ui.btn_create,False)
               
                    self.ui.MplWidget.canvas.axes.cla()
                    self.ui.MplWidget.canvas.draw()

                    self.validationControl=False
               

            if ctrl:
                self.ButtonsEnableDisable(self.ui.btn_create,True)
                self.validationControl=True

            
        

               
               
               
               


        

    def eventFilter(self,source,event):

        currentLineEdit = self.ui.frame_manuel_list.layout().itemAt(self.ui.frame_manuel_list.layout().count()-1).widget()

        if (event.type() == QEvent.KeyPress and source is currentLineEdit):
            print('basılan tuş:', (event.key(), event.text()))

            if event.key()==32 or event.key()==16777217 or event.key()==16777220:

                if currentLineEdit.text()!="":
                    self.ManuelListLineEditPressed()
        

        return super(Main, self).eventFilter(source, event)
        
    



    def RandomListMinMaxLength(self):
        
        if self.isAnimationReseted:
            
            listMax=self.ui.lineEdit_random_list_max.text()
            listMin=self.ui.lineEdit_random_list_min.text()
            listLength=self.ui.lineEdit_random_list_length.text()

            if listMax !="" and listMin !="" and listMax !="-" and listMin !="-"  :
            
                if int(listMax) > int(listMin) :

                    self.ui.lbl_validation_message.setText("")

                    if listLength !="" and listMax !="" and listMin !="":

                        if int(listLength)>1:
                            #self.ui.btn_create.setEnabled(True)
                            self.ButtonsEnableDisable(self.ui.btn_create,True)

                            self.validationControl=True
                        else :
                            #self.ui.btn_create.setEnabled(False)
                            self.ButtonsEnableDisable(self.ui.btn_create,False)
                            self.ButtonsEnableDisable(self.ui.btn_start,False)

                            self.ui.MplWidget.canvas.axes.cla()
                            self.ui.MplWidget.canvas.draw()

                            self.validationControl=False

                    else:
                        #self.ui.btn_create.setEnabled(False)
                        self.ButtonsEnableDisable(self.ui.btn_create,False)
                        self.ButtonsEnableDisable(self.ui.btn_start,False)

                        self.ui.MplWidget.canvas.axes.cla()
                        self.ui.MplWidget.canvas.draw()
                    
                        self.validationControl=False

                elif int(listMax) <= int(listMin):
                    self.ui.lbl_validation_message.setText("Maksimum değer alt sınırdan yüksek olmalıdır")
            
                    #self.ui.btn_create.setEnabled(False)
                    self.ButtonsEnableDisable(self.ui.btn_create,False)
                    self.ButtonsEnableDisable(self.ui.btn_start,False)

                    self.ui.MplWidget.canvas.axes.cla()
                    self.ui.MplWidget.canvas.draw()

                    self.validationControl=False

            else:
                #self.ui.btn_create.setEnabled(False)
                self.ButtonsEnableDisable(self.ui.btn_create,False)
                self.ButtonsEnableDisable(self.ui.btn_start,False)

                self.ui.MplWidget.canvas.axes.cla()
                self.ui.MplWidget.canvas.draw()
            
                self.validationControl=False
        



    def ManuelListRemoveItem(self):

        if self.isAnimationReseted:

            self.ButtonsEnableDisable(self.ui.btn_start,False)
            
            self.ui.MplWidget.canvas.axes.cla()
            self.ui.MplWidget.canvas.draw()

            
            #self.ui.frame_manuel_list.layout().removeWidget(self.ui.frame_manuel_list.layout().itemAt(self.ui.frame_manuel_list.layout().count()-1).widget())
            ManuelListLineEditCount=self.ui.frame_manuel_list.layout().count()
            WillDeleteManuelListItemWidget=self.ui.frame_manuel_list.layout().itemAt(ManuelListLineEditCount-1).widget()

            if ManuelListLineEditCount>1:
                WillDeleteManuelListItemWidget.deleteLater()
            
                self.ui.frame_manuel_list.setMinimumWidth((ManuelListLineEditCount*60))
            
                ManuelListLineEditCount=self.ui.frame_manuel_list.layout().count()

                if ManuelListLineEditCount<=2:
                    #self.ui.btn_create.setEnabled(False)
                    self.ButtonsEnableDisable(self.ui.btn_create,False)

            else:
                #self.ui.btn_create.setEnabled(False)
                self.ButtonsEnableDisable(self.ui.btn_create,False)


    def ManuelListRemoveAllItems(self):

        if self.isAnimationReseted:

            ManuelListLineEditCount=self.ui.frame_manuel_list.layout().count()

            for x in range(1,ManuelListLineEditCount):
                self.ui.frame_manuel_list.layout().itemAt(x).widget().deleteLater()
                #self.ui.btn_create.setEnabled(False)
                self.ButtonsEnableDisable(self.ui.btn_create,False)


            self.ui.frame_manuel_list.setMinimumWidth(50)
        
        
            self.ui.lineEdit_manuel_list_0.setText("")







    def ManuelListLineEditPressed(self):
        
        ManuelListLineEditCount=self.ui.frame_manuel_list.layout().count()

        

        self.ManuelListNewLineEdit=QtWidgets.QLineEdit(self)

        self.ManuelListNewLineEdit.installEventFilter(self)

        self.ManuelListNewLineEdit.textChanged.connect(self.ManuelListTextChangedValidation)

        self.ManuelListNewLineEdit.setObjectName(f"lineEdit_manuel_list_{ManuelListLineEditCount-1}")
        self.ManuelListNewLineEdit.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.ManuelListNewLineEdit.setMinimumSize(50,50)
        self.ManuelListNewLineEdit.setMaximumSize(50,50)
        self.ManuelListNewLineEdit.setStyleSheet("border-color:white;")
        self.ManuelListNewLineEdit.setValidator(QIntValidator(-1000,1000,self))

        self.ManuelListNewLineEdit.setAlignment(QtCore.Qt.AlignCenter)

        self.ManuelListNewLineEdit.setFont(self.font3)


        self.ui.frame_manuel_list.setMinimumWidth(50+(ManuelListLineEditCount*60))
        self.ui.frame_manuel_list.layout().addWidget(self.ManuelListNewLineEdit)

        self.ManuelListNewLineEdit.setFocus()
       
        self.ui.scrollArea.horizontalScrollBar().rangeChanged.connect(lambda: self.ui.scrollArea.horizontalScrollBar().setValue(self.ui.scrollArea.horizontalScrollBar().maximum()))
        
        self.ManuelListTextChangedValidation()
        
        
        



    def onClickedRandomListRadio(self):

        if self.isAnimationReseted:
        
            rb= self.sender()

            rb.setChecked(True)

            self.ui.radioButton_manuel_list.setChecked(False)

            self.ui.lbl_validation_message.setText("")

            self.ui.frame_random_list.setEnabled(True)
            self.ui.frame_manuel_list.setEnabled(False)

            self.ManuelListRemoveAllItems()
            self.ui.lineEdit_random_list_max.setText("")
            self.ui.lineEdit_random_list_min.setText("")
            self.ui.lineEdit_random_list_length.setText("")
            #self.ui.btn_create.setEnabled(False)
            self.ButtonsEnableDisable(self.ui.btn_create,False)


            self.ui.frame_random_list.setStyleSheet("background:#1E293B; border-radius:3px; padding:0 3px 3px 3px;")
            self.ui.lineEdit_random_list_min.setStyleSheet("border-color:white;")
            self.ui.lineEdit_random_list_max.setStyleSheet("border-color:white;")
            self.ui.lineEdit_random_list_length.setStyleSheet("border-color:white;")

            self.ui.scrollArea.setStyleSheet("background:#737373; border-radius:3px;")
            self.ui.lineEdit_manuel_list_0.setStyleSheet("border-color:#A8A29E;")


    

    def onClickedManuelListRadio(self):

        if self.isAnimationReseted:

            self.ui.radioButton_random_list.setChecked(False)

            self.ui.lbl_validation_message.setText("")

            rb= self.sender()

        
            rb.setChecked(True)

                
            self.ui.frame_manuel_list.setEnabled(True)
            self.ui.frame_random_list.setEnabled(False)

            self.ui.lineEdit_random_list_max.setText("")
            self.ui.lineEdit_random_list_min.setText("")
            self.ui.lineEdit_random_list_length.setText("")

            self.ui.scrollArea.setStyleSheet("background:#1E293B; border-radius:3px;")
            self.ui.lineEdit_manuel_list_0.setStyleSheet("border-color:white;")

            self.ui.frame_random_list.setStyleSheet("background:#737373; border-radius:3px; padding:0 3px 3px 3px;")
            self.ui.lineEdit_random_list_min.setStyleSheet("border-color:#A8A29E;")
            self.ui.lineEdit_random_list_max.setStyleSheet("border-color:#A8A29E;")
            self.ui.lineEdit_random_list_length.setStyleSheet("border-color:#A8A29E;")

                

            if self.ui.frame_manuel_list.layout().count() <= 1:
                #self.ui.btn_create.setEnabled(False)
                self.ButtonsEnableDisable(self.ui.btn_create,False)

    
    def ButtonsEnableDisable(self,btn,state):

        if state:
            btn.setEnabled(True)
            btn.setStyleSheet("#QPushButton{ background-color:rgb(34,36,44); min-width:100px; border-radius:3px; }")
        else:
            btn.setEnabled(False)
            btn.setStyleSheet("background-color:#737373; min-width:100px; border-radius:3px;")






    def CreateGraph(self):

        self.isAnimationStarted=False
        self.isAnimationResuming=False

        self.ui.btn_reset.setText("Sıfırla")

        try:
            self.t.cancel()

        except:
            print("Zamanlayıcı kapalı")
        

        if self.ui.radioButton_random_list.isChecked():

            self.randomListMax=int(self.ui.lineEdit_random_list_max.text())
            self.randomListMin=int(self.ui.lineEdit_random_list_min.text())
            self.randomListLength=int(self.ui.lineEdit_random_list_length.text())

            self.unsortedVisualArr=np.random.randint(self.randomListMin,self.randomListMax,self.randomListLength)

            

        elif self.ui.radioButton_manuel_list.isChecked():

            self.unsortedVisualArr=[]

            self.manuelListLength=self.ui.frame_manuel_list.layout().count()

            for x in range(0,self.manuelListLength):

                self.unsortedVisualArr.append(int(self.ui.frame_manuel_list.layout().itemAt(x).widget().text()))
            

        self.ui.MplWidget.canvas.axes.cla()

        match self.graphType:
            case 0: self.pathCollection=self.ui.MplWidget.canvas.axes.scatter(np.arange(0,len(self.unsortedVisualArr)),self.unsortedVisualArr,c=self.unsortedColor,edgecolor=self.edgeColor,linewidth=self.linewidth,alpha=self.alpha)
            case 1: self.barContainer=self.ui.MplWidget.canvas.axes.bar(np.arange(0,len(self.unsortedVisualArr)),self.unsortedVisualArr,color=self.unsortedColor,edgecolor=self.edgeColor,linewidth=self.linewidth,alpha=self.alpha)
            case 2: 
                self.stemContainer=self.ui.MplWidget.canvas.axes.stem(np.arange(0,len(self.unsortedVisualArr)),self.unsortedVisualArr,linefmt=self.stemLineFormat,markerfmt=self.stemMarkerFormat)
                
                self.stemContainer.stemlines.set_color(self.stemStemLinesColor)
                self.stemContainer.baseline.set_color(self.stemBaseLineColor)

                self.stemContainer.markerline.set_markerfacecolor(self.stemMarkerFaceColor)
                self.stemContainer.markerline.set_markeredgecolor(self.stemMarkerEdgeColor)
                self.stemContainer.markerline.set_markeredgewidth(self.stemMarkerEdgeWidth)

                



        

       
        self.ui.MplWidget.canvas.axes.set_ylim(top=max(self.unsortedVisualArr)+self.ylimMaxIncreaseAmount)
        
        self.ui.MplWidget.canvas.draw()
        
        #self.ui.btn_start.setEnabled(True)
        self.ButtonsEnableDisable(self.ui.btn_start,True)

        #self.ui.btn_pause_resume.setEnabled(False)
        #self.ui.btn_reset.setEnabled(False)
        self.ButtonsEnableDisable(self.ui.btn_pause_resume,False)
        self.ButtonsEnableDisable(self.ui.btn_reset,False)

        self.ui.btn_pause_resume.setChecked(False)
        self.ui.btn_pause_resume.setText("Durdur")
        self.ui.btn_pause_resume.setIcon(QIcon(":/icons/icons/pause.png"))
        

        
        





    def StartVisualization(self):

        self.comparisonCount=0
        self.comparisonCopyArray.clear()

        self.isAnimationReseted=False

        


        try:
            self.t.cancel()

        except:
            print("Zamanlayıcı kapalı")

        self.ui.lbl_comparison_count.setText("0")


        for x in self.sortingAlgorithmAndGraphTypeList:
            x.setEnabled(False)

         
        self.ui.btn_size_grip.setEnabled(False)
        self.ui.btn_restore_maximize.setEnabled(False)

        self.ui.MplWidget.canvas.axes.cla()

        match self.graphType:
            case 0: self.pathCollection=self.ui.MplWidget.canvas.axes.scatter(np.arange(0,len(self.unsortedVisualArr)),self.unsortedVisualArr,c=self.unsortedColor,edgecolor=self.edgeColor,linewidth=self.linewidth,alpha=self.alpha)
            case 1: self.barContainer=self.ui.MplWidget.canvas.axes.bar(np.arange(0,len(self.unsortedVisualArr)),self.unsortedVisualArr,color=self.unsortedColor,edgecolor=self.edgeColor,linewidth=self.linewidth,alpha=self.alpha)
            case 2: 
                self.stemContainer=self.ui.MplWidget.canvas.axes.stem(np.arange(0,len(self.unsortedVisualArr)),self.unsortedVisualArr,linefmt=self.stemLineFormat,markerfmt=self.stemMarkerFormat)
                
                self.stemContainer.stemlines.set_color(self.stemStemLinesColor)
                self.stemContainer.baseline.set_color(self.stemBaseLineColor)

                self.stemContainer.markerline.set_markerfacecolor(self.stemMarkerFaceColor)
                self.stemContainer.markerline.set_markeredgecolor(self.stemMarkerEdgeColor)
                self.stemContainer.markerline.set_markeredgewidth(self.stemMarkerEdgeWidth)

        self.ui.MplWidget.canvas.axes.set_ylim(top=max(self.unsortedVisualArr)+self.ylimMaxIncreaseAmount)
        self.ui.MplWidget.canvas.draw()
        
        self.visualArrComparisonCount=np.copy(self.unsortedVisualArr)

        self.visualArr = TrackedArray(self.unsortedVisualArr)

        arrLength=len(self.visualArr)

        

        match self.sortingAlgorithmIndex:
            case 0: 
                self.selectionSort(self.visualArr,len(self.visualArr))
                self.selectionSortComparisonCount(self.visualArrComparisonCount,len(self.visualArrComparisonCount))

                self.ui.lbl_best_case.setText(str(round(arrLength**2)))
                self.ui.lbl_average_case.setText(str(round(arrLength**2)))
                self.ui.lbl_worst_case.setText(str(round(arrLength**2)))

            case 1: 
                self.bubbleSort(self.visualArr)
                self.bubbleSortComparisonCount(self.visualArrComparisonCount)

                self.ui.lbl_best_case.setText(str(arrLength))
                self.ui.lbl_average_case.setText(str(round(arrLength**2)))
                self.ui.lbl_worst_case.setText(str(round(arrLength**2)))

            case 2: 
                self.insertionSort(self.visualArr)
                self.insertionSortComparisonCount(self.visualArrComparisonCount)

                self.ui.lbl_best_case.setText(str(arrLength))
                self.ui.lbl_average_case.setText(str(round(arrLength**2)))
                self.ui.lbl_worst_case.setText(str(round(arrLength**2)))

            case 3: 
                self.mergeSort(self.visualArr,0,len(self.visualArr)-1)
                self.mergeSortComparisonCount(self.visualArrComparisonCount,0,len(self.visualArrComparisonCount)-1)

                self.ui.lbl_best_case.setText(str(round(arrLength*math.log2(arrLength))))
                self.ui.lbl_average_case.setText(str(round(arrLength*math.log2(arrLength))))
                self.ui.lbl_worst_case.setText(str(round(arrLength*math.log2(arrLength))))

            case 4: 
                self.quickSort(self.visualArr,0,len(self.visualArr)-1)
                self.quickSortComparisonCount(self.visualArrComparisonCount,0,len(self.visualArrComparisonCount)-1)

                self.ui.lbl_best_case.setText(str(round(arrLength*math.log2(arrLength))))
                self.ui.lbl_average_case.setText(str(round(arrLength*math.log2(arrLength))))
                self.ui.lbl_worst_case.setText(str(round(arrLength**2)))

        
        
        
        

        self.scatterColorListDefault=[]

        self.stemColorListDefault=[]

        for x in range(len(self.unsortedVisualArr)):
            self.scatterColorListDefault.append(self.unsortedColor)
            
            self.stemColorListDefault.append(self.unsortedColor)


        print("Karşılaştırma sayısı")
        print(self.comparisonCount)
            
        
        self.animation = FuncAnimation(self.ui.MplWidget.figure,self.AnimationUpdate,frames=range(len(self.visualArr.full_copies)),blit=True,interval=6000./self.speed,repeat=False)
        
        

        self.isAnimationStarted=True
        self.isAnimationResuming=True

        #self.ui.btn_create.setEnabled(False)
        self.ButtonsEnableDisable(self.ui.btn_create,False)

        #self.ui.btn_start.setEnabled(False)
        self.ButtonsEnableDisable(self.ui.btn_start,False)

        #self.ui.btn_pause_resume.setEnabled(True)
        self.ButtonsEnableDisable(self.ui.btn_pause_resume,True)

        #self.ui.btn_reset.setEnabled(True)
        self.ButtonsEnableDisable(self.ui.btn_reset,True)

        self.ButtonsEnableDisable(self.ui.btn_manuel_list_remove_all_items,False)
        self.ButtonsEnableDisable(self.ui.btn_manuel_list_remove_item,False)

        self.ui.frame_manuel_list.setEnabled(False)
        self.ui.frame_random_list.setEnabled(False)

        self.ui.radioButton_manuel_list.setEnabled(False)
        self.ui.radioButton_random_list.setEnabled(False)

        self.ui.btn_pause_resume.setChecked(False)
        self.ui.btn_pause_resume.setIcon(QIcon(":/icons/icons/pause.png"))

        self.startTimer()



    def PauseResumeAnimation(self,state):

        #print("Durdurma-Devam Etme Butonu State: ",state)

        if state:
            self.animation.event_source.stop()
            self.isAnimationResuming=False
            self.ui.btn_pause_resume.setText("Devam Et")
            #self.ui.btn_create.setEnabled(True)
            #self.ButtonsEnableDisable(self.ui.btn_create,True)
            self.ui.btn_pause_resume.setIcon(QIcon(":/icons/icons/resume.png"))


        else :
        
            self.animation.event_source.start()
            self.isAnimationResuming=True
            
            
            self.ui.btn_pause_resume.setText("Durdur")
            #self.ui.btn_create.setEnabled(False)
            self.ButtonsEnableDisable(self.ui.btn_create,False)
            self.ui.btn_pause_resume.setIcon(QIcon(":/icons/icons/pause.png"))

            for x in self.sortingAlgorithmAndGraphTypeList:
                x.setEnabled(False)



    def ResetGraph(self):

        self.t.cancel()
        self.isAnimationStarted=False

        self.isAnimationReseted=True

        self.ui.frame_manuel_list.setEnabled(True)
        self.ui.frame_random_list.setEnabled(True)
        
        self.ui.radioButton_manuel_list.setEnabled(True)
        self.ui.radioButton_random_list.setEnabled(True)

        self.ui.lbl_comparison_count.setText("-")

        self.ButtonsEnableDisable(self.ui.btn_reset,False)

        self.ButtonsEnableDisable(self.ui.btn_manuel_list_remove_all_items,True)
        self.ButtonsEnableDisable(self.ui.btn_manuel_list_remove_item,True)

        self.ui.MplWidget.canvas.axes.cla()

        for x in self.sortingAlgorithmAndGraphTypeList:
            x.setEnabled(True)
        
        self.animation.event_source=None
        del self.animation

        self.ui.btn_size_grip.setEnabled(True)
        self.ui.btn_restore_maximize.setEnabled(True)

        match self.graphType:
            case 0: self.pathCollection=self.ui.MplWidget.canvas.axes.scatter(np.arange(0,len(self.unsortedVisualArr)),self.unsortedVisualArr,c=self.unsortedColor,edgecolor=self.edgeColor,linewidth=self.linewidth,alpha=self.alpha)
            case 1: self.barContainer=self.ui.MplWidget.canvas.axes.bar(np.arange(0,len(self.unsortedVisualArr)),self.unsortedVisualArr,color=self.unsortedColor,edgecolor=self.edgeColor,linewidth=self.linewidth,alpha=self.alpha)
            case 2: 
                self.stemContainer=self.ui.MplWidget.canvas.axes.stem(np.arange(0,len(self.unsortedVisualArr)),self.unsortedVisualArr,linefmt=self.stemLineFormat,markerfmt=self.stemMarkerFormat)
                
                self.stemContainer.stemlines.set_color(self.stemStemLinesColor)
                self.stemContainer.baseline.set_color(self.stemBaseLineColor)

                self.stemContainer.markerline.set_markerfacecolor(self.stemMarkerFaceColor)
                self.stemContainer.markerline.set_markeredgecolor(self.stemMarkerEdgeColor)
                self.stemContainer.markerline.set_markeredgewidth(self.stemMarkerEdgeWidth)


        self.ui.MplWidget.canvas.axes.set_ylim(top=max(self.unsortedVisualArr)+self.ylimMaxIncreaseAmount)
        self.ui.MplWidget.canvas.draw()


        self.ButtonsEnableDisable(self.ui.btn_create,True)
        self.ButtonsEnableDisable(self.ui.btn_start,True)

        self.ui.btn_pause_resume.setEnabled(False)
        self.ui.btn_pause_resume.setStyleSheet("width:100px; background:#737373; border-radius:3px;")
        self.ui.btn_pause_resume.setText("Durdur")
        self.ui.btn_pause_resume.setIcon(QIcon(":/icons/icons/pause.png"))
        #self.ui.btn_start.setEnabled(True)
        


      

        

        

    def AnimationUpdate(self, frame):

        self.lastFrame=frame

        if self.speedChanged:
            
            self.ui.MplWidget.canvas.axes.cla()
            match self.graphType:
                case 0: self.pathCollection=self.ui.MplWidget.canvas.axes.scatter(np.arange(0,len(self.visualArr.full_copies[self.lastFrame])),self.visualArr.full_copies[self.lastFrame],c=self.unsortedColor,edgecolor=self.edgeColor,linewidth=self.linewidth,alpha=self.alpha)
                case 1: self.barContainer=self.ui.MplWidget.canvas.axes.bar(np.arange(0,len(self.visualArr.full_copies[self.lastFrame])),self.visualArr.full_copies[self.lastFrame],color=self.graphColor,edgecolor=self.edgeColor,linewidth=self.linewidth,alpha=self.alpha)
                case 2: 
                    self.stemContainer=self.ui.MplWidget.canvas.axes.stem(np.arange(0,len(self.visualArr.full_copies[self.lastFrame])),self.visualArr.full_copies[self.lastFrame],linefmt=self.stemLineFormat,markerfmt=self.stemMarkerFormat)
                
                    self.stemContainer.stemlines.set_color(self.stemStemLinesColor)
                    self.stemContainer.baseline.set_color(self.stemBaseLineColor)

                    self.stemContainer.markerline.set_markerfacecolor(self.stemMarkerFaceColor)
                    self.stemContainer.markerline.set_markeredgecolor(self.stemMarkerEdgeColor)
                    self.stemContainer.markerline.set_markeredgewidth(self.stemMarkerEdgeWidth)
        
            
        self.ui.MplWidget.canvas.axes.set_ylim(top=max(self.unsortedVisualArr)+self.ylimMaxIncreaseAmount)
        self.ui.MplWidget.canvas.draw()
        

        self.speedChanged=False

        

        





        index, op = self.visualArr.getActivity(frame)

        


        if frame==(len(self.visualArr.full_copies)-1):
            #self.ui.btn_pause_resume.setEnabled(False)
            self.ButtonsEnableDisable(self.ui.btn_pause_resume,False)
            self.ui.btn_pause_resume.setIcon(QIcon(":/icons/icons/pause.png"))

            #self.ui.btn_reset.setEnabled(True)
            self.ButtonsEnableDisable(self.ui.btn_reset,True)

            #self.ui.btn_start.setEnabled(False)        
            self.ButtonsEnableDisable(self.ui.btn_start,False)

            #self.ui.btn_create.setEnabled(True)        
            #self.ButtonsEnableDisable(self.ui.btn_create,True)

            

            self.isAnimationStarted=False

            self.t.cancel()

            self.ui.lbl_comparison_count.setText(str(self.comparisonCount))

            #self.ui.btn_reset.setText("Yeniden Başlat")
            #self.ui.btn_reset.setStyleSheet("min-width:160px;")


        fullCopiesLength=len(self.visualArr.full_copies)

        ctrl=self.visualArr.full_copies[frame]==self.visualArr.full_copies[fullCopiesLength-1]

        c=np.copy(ctrl)

        for (x,y) in enumerate(ctrl):

            if y:

                for j in range(frame,len(self.visualArr.full_copies)):
                                
                    if self.visualArr.full_copies[frame][x] != self.visualArr.full_copies[j][x]:
                                    
                        c[x]=False
                        break
       


        match self.graphType:

            
            case 0:
                self.pathCollection.set_offsets(list(zip(np.arange(0,len(self.visualArr.full_copies[frame])),self.visualArr.full_copies[frame])))

                self.scatterColorList=[]

                self.scatterColorList=self.scatterColorListDefault.copy()

                if op =="get":
                    self.scatterColorList[index]=self.getOperationColor
        
                elif op == "set":
                    self.scatterColorList[index]=self.setOperationColor
                

                self.pathCollection.set_facecolor(self.scatterColorList)

                for x in range(len(c)):

                    if c[x]:
                        self.scatterColorList[x]=self.sortedColor


                self.pathCollection.set_edgecolor(self.edgeColor)

                self.pathCollection.set_alpha(0.75)
                self.pathCollection.set_linewidth(1)


                if frame==(len(self.visualArr.full_copies)-1):
                    self.scatterColorList[index] =self.sortedColor
                    self.pathCollection.set_facecolor(self.scatterColorList)


                return (self.pathCollection.findobj())
            
            case 1:
                
                
                i=0
                for (rectangle, height) in zip(self.barContainer.patches, self.visualArr.full_copies[frame]):


                    rectangle.set_height(height)

                    
                    if c[i]:
                
                       rectangle.set_color(self.sortedColor)
                        

                    else:
                       rectangle.set_color(self.unsortedColor)
                        
                    i+=1

                    rectangle.set_edgecolor(self.edgeColor)

                
               
                if op =="get":
                    self.barContainer.patches[index].set_color(self.getOperationColor)
                    self.barContainer.patches[index].set_edgecolor(self.edgeColor)
        
                elif op == "set":
                    self.barContainer.patches[index].set_color(self.setOperationColor)
                    self.barContainer.patches[index].set_edgecolor(self.edgeColor)

                if frame==(len(self.visualArr.full_copies)-1):
                    self.barContainer.patches[index].set_color(self.sortedColor)
                    self.barContainer.patches[index].set_edgecolor(self.edgeColor)
                        
       

                return (self.barContainer)
            


            
            case 2:
                
                self.ui.MplWidget.canvas.axes.cla()

      

                self.stemContainer=self.ui.MplWidget.canvas.axes.stem(np.arange(0,len(self.visualArr.full_copies[self.lastFrame])),self.visualArr.full_copies[self.lastFrame],linefmt=self.stemLineFormat,markerfmt=self.stemMarkerFormat)
                
                

                self.ui.MplWidget.canvas.axes.set_ylim(top=max(self.unsortedVisualArr)+self.ylimMaxIncreaseAmount)
                

                markerline,stemlines,baseline=self.stemContainer.markerline,self.stemContainer.stemlines,self.stemContainer.baseline
                
                
                baseline.set_color(self.unsortedColor)
                
                markerline.set_markeredgewidth(self.stemMarkerEdgeWidth)
                markerline.set_markeredgecolor(self.stemMarkerEdgeColor)
                markerline.set_markerfacecolor(self.stemMarkerFaceColor)
                
                
                self.stemColorList=[]

                self.stemColorList=self.stemColorListDefault.copy()

                if op =="get":
                    self.stemColorList[index]=self.getOperationColor
        
                elif op == "set":
                    self.stemColorList[index]=self.setOperationColor
                

                for x in range(len(c)):
                    if c[x]:
                        self.stemColorList[x]=self.sortedColor
              
                stemlines.set_color(self.stemColorList)

                if frame==(len(self.visualArr.full_copies)-1):
                    self.stemColorList[index] =self.sortedColor
                    
                    baseline.set_color(self.sortedColor)
                    markerline.set_markerfacecolor(self.sortedColor)
                    stemlines.set_color(self.stemColorList)

                return (self.stemContainer)


            
            





            

            

        

        





    def ChangeAnimationSpeed(self,speed):
        
        self.speed = float(speed)

        if self.isAnimationStarted:

        
            self.speedChanged=True
        
            self.animation.event_source.stop()

       
            self.animation = FuncAnimation(self.ui.MplWidget.figure,self.AnimationUpdate,frames=range(self.lastFrame,len(self.visualArr.full_copies)),blit=True,interval=6000./self.speed,repeat=False)
       

            if not self.isAnimationResuming:

                self.animation.event_source.stop()


            self.ui.MplWidget.canvas.axes.cla()




            fullCopiesLength=len(self.visualArr.full_copies)

            ctrl=self.visualArr.full_copies[self.lastFrame]==self.visualArr.full_copies[fullCopiesLength-1]

            c=np.copy(ctrl)

            for (x,y) in enumerate(ctrl):

                if y:

                    for j in range(self.lastFrame,len(self.visualArr.full_copies)):
                                
                        if self.visualArr.full_copies[self.lastFrame][x] != self.visualArr.full_copies[j][x]:
                                    
                            c[x]=False
                            break
                            

            
            ctrl=np.copy(c)

            self.graphColor=[self.unsortedColor]*len(self.visualArrComparisonCount)


            for i in range(len(c)):

                if c[i]:

                    self.graphColor[i]=self.sortedColor

                    
                

                


            match self.graphType:
                case 0: self.pathCollection=self.ui.MplWidget.canvas.axes.scatter(np.arange(0,len(self.visualArr.full_copies[self.lastFrame])),self.visualArr.full_copies[self.lastFrame],color=self.graphColor,edgecolor=self.edgeColor,linewidth=self.linewidth,alpha=self.alpha)
                case 1: self.barContainer=self.ui.MplWidget.canvas.axes.bar(np.arange(0,len(self.visualArr.full_copies[self.lastFrame])),self.visualArr.full_copies[self.lastFrame],color=self.graphColor,edgecolor=self.edgeColor,linewidth=self.linewidth,alpha=self.alpha)
                case 2: 
                    self.stemContainer=self.ui.MplWidget.canvas.axes.stem(np.arange(0,len(self.visualArr.full_copies[self.lastFrame])),self.visualArr.full_copies[self.lastFrame],linefmt=self.stemLineFormat,markerfmt=self.stemMarkerFormat)
                
                    self.stemContainer.stemlines.set_color(self.graphColor)

                    if ctrl.all():
                        self.stemContainer.baseline.set_color(self.sortedColor)
                    else:
                        self.stemContainer.baseline.set_color(self.stemBaseLineColor)

                    self.stemContainer.markerline.set_markerfacecolor(self.stemMarkerFaceColor)
                    self.stemContainer.markerline.set_markeredgecolor(self.stemMarkerEdgeColor)
                    self.stemContainer.markerline.set_markeredgewidth(self.stemMarkerEdgeWidth)
            
            
            self.ui.MplWidget.canvas.axes.set_ylim(top=max(self.unsortedVisualArr)+self.ylimMaxIncreaseAmount)

     
      

    

    def comparisonCountInterval(self):

       
        f = self.lastFrame

        print("Karşılaştırma Frame: ")
        print(f)

        self.control=False

        for x in range(f,0,-1):

            for self.compCountIndex in range(len(self.comparisonCopyArray)-1,0,-1):
                
                
                if (self.comparisonCopyArray[self.compCountIndex] == self.visualArr.full_copies[x]).all():
                    print("Karşılaştırma Sayısı")
                    print(self.compCountIndex)
                    self.control=True

                    self.ui.lbl_comparison_count.setText(str(self.compCountIndex+1))
                    break

                self.control=False

            if self.control:

                self.control=False
                break 

        
        

        




    def startTimer(self):
        self.t=threading.Timer(self.interval,self.startTimer)

        self.t.start()

        self.comparisonCountInterval()










    def bubbleSort(self, arr):
        n = len(arr)

        swapped = False

        for i in range(n-1):

            for j in range(0, n-i-1):

                if arr[j] > arr[j + 1]:

                    swapped = True
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

            if not swapped:
                return
            

     

    def selectionSort(self,array, size):
    
        for ind in range(size):
            min_index = ind
 
            for j in range(ind + 1, size):

                if array[j] < array[min_index]:
                    min_index = j
         
            (array[ind], array[min_index]) = (array[min_index], array[ind])


    def insertionSort(self,arr):
     
        if (n := len(arr)) <= 1:
            return
        for i in range(1, n):
         
            key = arr[i]
            
            j = i-1
            while j >=0 and key < arr[j] :
                
                arr[j+1] = arr[j]
                j -= 1
            arr[j+1] = key

    

    def merge(self,arr, l, m, r):
        n1 = m - l + 1
        n2 = r - m
 
        
        L = [0] * (n1)
        R = [0] * (n2)
 
        
        for i in range(0, n1):
            L[i] = arr[l + i]
 
        for j in range(0, n2):
            R[j] = arr[m + 1 + j]
 
        
        i = 0
        j = 0
        k = l 
 
        while i < n1 and j < n2:

            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
 
        
        
        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1
 
        
        
        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1
 
    


    def mergeSort(self,arr, l, r):
        if l < r:
            
            m = l+(r-l)//2
            
            self.mergeSort(arr, l, m)
            self.mergeSort(arr, m+1, r)
            self.merge(arr, l, m, r)
 
    




    
    def partition(self,array, low, high):
 
        pivot = array[high]
 
        i = low - 1
 
        
        for j in range(low, high):

            self.comparisonCount+=1

            if array[j] <= pivot:
 
                i = i + 1
                
                (array[i], array[j]) = (array[j], array[i])
 
        
        (array[i + 1], array[high]) = (array[high], array[i + 1])
 
        return i + 1
 
    
 


 
    def quickSort(self,array, low, high):
        if low < high:
 
            pi = self.partition(array, low, high)
 
            self.quickSort(array, low, pi - 1)
 
            self.quickSort(array, pi + 1, high)








    def bubbleSortComparisonCount(self, arr):
        n = len(arr)

        swapped = False

        for i in range(n-1):

            for j in range(0, n-i-1):

                self.comparisonCount+=1
                self.comparisonCopyArray.append(np.copy(arr))

                if arr[j] > arr[j + 1]:

                    swapped = True
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

            if not swapped:
                return



    def selectionSortComparisonCount(self,array, size):
    
        for ind in range(size):
            min_index = ind
 
            for j in range(ind + 1, size):

                self.comparisonCount+=1
                self.comparisonCopyArray.append(np.copy(array))

                if array[j] < array[min_index]:
                    min_index = j
         
            (array[ind], array[min_index]) = (array[min_index], array[ind])




    def insertionSortComparisonCount(self,arr):
     
        if (n := len(arr)) <= 1:
            return
        for i in range(1, n):
         
            key = arr[i]
 
            j = i-1
            while j >=0 and key < arr[j] :

                self.comparisonCount+=1
                self.comparisonCopyArray.append(np.copy(arr))

                arr[j+1] = arr[j]
                j -= 1
            arr[j+1] = key



    def mergeComparisonCount(self,arr, l, m, r):
        n1 = m - l + 1
        n2 = r - m
 
        
        L = [0] * (n1)
        R = [0] * (n2)
 
        
        for i in range(0, n1):
            L[i] = arr[l + i]
 
        for j in range(0, n2):
            R[j] = arr[m + 1 + j]
 
        
        i = 0
        j = 0
        k = l 
 
        while i < n1 and j < n2:

            self.comparisonCount+=1
            self.comparisonCopyArray.append(np.copy(arr))


            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
 
        
        
        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1
 
        
        
        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1
 
    


    def mergeSortComparisonCount(self,arr, l, r):
        if l < r:
            
            m = l+(r-l)//2
 
            self.mergeSortComparisonCount(arr, l, m)
            self.mergeSortComparisonCount(arr, m+1, r)
            self.mergeComparisonCount(arr, l, m, r)
 






    def partitionComparisonCount(self,array, low, high):
 
        pivot = array[high]
 
        i = low - 1
        
        for j in range(low, high):

            self.comparisonCount+=1
            self.comparisonCopyArray.append(np.copy(array))

            if array[j] <= pivot:
 
                i = i + 1
                
                (array[i], array[j]) = (array[j], array[i])
 
        
        (array[i + 1], array[high]) = (array[high], array[i + 1])
 
        return i + 1
 
    
 


 
    def quickSortComparisonCount(self,array, low, high):
        if low < high:
 
            pi = self.partitionComparisonCount(array, low, high)
 
            self.quickSortComparisonCount(array, low, pi - 1)
 
            self.quickSortComparisonCount(array, pi + 1, high)



def window():

    application = QApplication(sys.argv)

    window = Main()
    window.show()

    sys.exit(application.exec_())


window()
