import sys
from PyQt5.QtWidgets import QApplication, QWidget,QPushButton, QLineEdit,QLabel,QTabWidget,QVBoxLayout,QMainWindow,QTableWidget,QTableWidgetItem,QFileDialog,QMessageBox
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import pyqtSlot
from functools import partial
from operations import InformationExtractor
import pefile,ctypes
import numpy
from classifier_Model import classifier_model
from EventHandlers import NktSpyMgrEvents
import win32com.client

class Button_Handlers:
    
    def Back_button_function(self,winshow,winhide):
        winshow.show()
        winhide.hide()

    def Get_FilePath(self,textbox,mainwindow):
     fileName, _ = QFileDialog.getOpenFileName(mainwindow, "Open File", "", "All Files (*);;executable Files (*.exe)")
     if '.exe' not in fileName and  '.EXE' not in fileName:
         message_box = QMessageBox()

         buttonReply = QMessageBox.question(message_box, 'Malware Hunter ',
                                            "Please make sure you entered .exe file", QMessageBox.Ok)

         if buttonReply == QMessageBox.Ok:
             message_box.close()
     elif fileName =='':
         message_box = QMessageBox()

         buttonReply = QMessageBox.question(message_box, 'Malware Hunter ',
                                            "you entered an empty path Enter you file again", QMessageBox.Ok)

         if buttonReply == QMessageBox.Ok:
             message_box.close()
     else:
      textbox.setText(fileName)
         

    def ScanFunction(self,vertextbox,md5_hash_textbox,class_textbox,pathtextbox,table,windtoshow,windtohide,dtable):
        path = pathtextbox.text()
        extractor = InformationExtractor()
        vertextbox.setText(str(extractor.exe_version(path)))
        md5_hash_textbox.setText(str(extractor.md5_hashing(path)))
        section_list= extractor.Get_file_sections(path)
        table.horizontalHeader().setDefaultSectionSize(230);
        table.setHorizontalHeaderLabels(["size in memory", "size in disk", "MD5 Hash","",""])
        table.setRowCount(len(section_list)+4)
        table.setColumnCount(4)
        vertical = []
        vertical.append("Sections names")
        for i in range(0,len(section_list)):
         vertical.append(section_list[i][0])
         for j in range(1,4):
          table.setItem(i+1,j-1, QTableWidgetItem(str(section_list[i][j])))
        vertical.append("")
        vertical.append("")
        vertical.append("")
        table.setVerticalHeaderLabels(vertical)

        win32com.client.pythoncom.CoInitialize()
        spyManager = win32com.client.DispatchWithEvents("DeviareCOM.NktSpyMgr", NktSpyMgrEvents)
        result = spyManager.Initialize()
        process=extractor.HookProcess(spyManager,path)
        message_box = QMessageBox()

        buttonReply = QMessageBox.question(message_box, 'Malware Hunter ', "Do you want to stop scanning to see the results? ", QMessageBox.Yes)
        
        if buttonReply == QMessageBox.Yes:
            windtoshow.show()                     
            process.Terminate(0)
            print('Yes clicked.')
            fun_numbers = 0
            path_str = str(pathtextbox.text())
            elements = path_str.split("/")
            file_name = elements[len(elements)-1]
            file_name =file_name.split('.')[0]+'.txt'
            print(file_name)
            log_file = open(file_name,"r")
            function_list = []
            function_list.append("Functions Names")                             
            functAndParm = []
            for i in log_file:
             fun_numbers+=1
             functAndParm.append(i.replace('\n',''))
             function = i.split(',')[0]
             function_list.append(function)                            
            dtable.setRowCount(fun_numbers+4)
            dtable.setColumnCount(10)
            function_list.append("")
            function_list.append("")
            function_list.append("")
            dtable.setHorizontalHeaderLabels(["parameter (1)", "parameter (2)", "parameter (3)","parameter (4)","parameter (5)","parameter (6)","parameter (7)","parameter (8)","parameter (9)","parameter (10)"]) 
            dtable.setVerticalHeaderLabels(function_list) 
            for i in range(0,len(functAndParm)):
                params = functAndParm[i].split(',')
                for j in range(1,len(params)):
                 dtable.setItem(i+1,j-1, QTableWidgetItem(str(params[j])))

            windtohide.hide()
            classifier=classifier_model()
            model=classifier.LoadModel('model.h5')
            log_file_seq_list=extractor.get_api_sequence_num(file_name)
            log_file_seq_array=numpy.array(log_file_seq_list)
            indicator=classifier.Predict(log_file_seq_array,model)
            if indicator==0:
              class_textbox.setText(" Safe File") 
            elif indicator==1:
              class_textbox.setText(" Malware File") 
                    
            windtoshow.show()                     
            
            
            
        

    
