from PyQt5.QtWidgets import QWidget,QPushButton,QLineEdit,QLabel,QTabWidget,QTableWidget,QApplication
from PyQt5.QtGui import QPixmap
from functools import partial
import Button_Handlers
from Button_Handlers import Button_Handlers
import sys

class pair :

  def __init__(self,widg,text):
    self.widget =QWidget()
    self.widget_text="" 
    self. widgeti = widg
    self.widget_text=text

  def set(self,widg,text):
    self.widgeti = widg
    self.widget_text=text

  def get_widget(self):
    return self.widgeti

  def get_widget_text(self):
    return self.widget_text
        

class Gui :
    def Create_Widget(self,window_name,xposition,yposition,xresize,yresize,cssline):
     new_window = QWidget()
     new_window.resize(xresize, yresize)
     new_window.move(xposition, yposition)
     new_window.setWindowTitle(window_name)
     new_window.setStyleSheet(cssline)
     return new_window 


    def Create_Button(self,button_name,xposition,yposition,xresize,yresize,cssline,parentwindow):
      new_button = QPushButton(button_name,parentwindow)
      new_button.move(xposition,yposition)
      new_button.resize(xresize, yresize)
      new_button.setStyleSheet(cssline)
      return new_button


    def Create_Textbox(self,xposition,yposition,xresize,yresize,cssline,parentwindow):
     new_textbox = QLineEdit(parentwindow)
     new_textbox.move(xposition,yposition)
     new_textbox.resize(xresize,yresize)
     new_textbox.setStyleSheet(cssline)
     new_textbox.setReadOnly(True)
     return new_textbox



    def Create_Label(self,label_text,xposition,yposition,xresize,yresize,cssline,parentwindow ):
      new_label = QLabel(label_text,parentwindow)
      new_label.move(xposition,yposition)
      new_label.resize(xresize,yresize)
      new_label.setStyleSheet(cssline)
      return new_label
     

    def Create_LabelImage(self,path,xposition,yposition,xresize,yresize,parentwindow):
     new_label_img = QLabel(parentwindow)
     img = QPixmap(path)
     new_label_img.setPixmap(img)
     new_label_img.resize(xresize,yresize)
     new_label_img.move(xposition,yposition)
     return new_label_img
    


    def Create_Tabs(self,collection,xposition,yposition,xresize,yresize,cssline,parentwindow):
     tabs = QTabWidget(parentwindow)
     tabs.resize(xresize,yresize)
     for i in range(0,len(collection)):

       tabs.addTab(collection[i].get_widget(),collection[i].get_widget_text())    

     tabs.move(xposition,yposition)
     
     tabs.setStyleSheet(cssline)
     return tabs 





    def Create_DataTable(self,rcount,ccount,xposition,yposition,xresize,yresize,cssline,parentwindow):
     newtableWidget = QTableWidget(parentwindow)
     newtableWidget.setRowCount(rcount)
     newtableWidget.setColumnCount(ccount)
     newtableWidget.move(xposition,yposition)
     newtableWidget.resize(xresize,yresize)
     newtableWidget.setStyleSheet(cssline)
     newtableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
     return newtableWidget


    def App_Intializer(self):
        app = QApplication(sys.argv)
        gui_manager = Gui()

        main_widget = gui_manager.Create_Widget("Malware Hunter", 300, 300, 500, 600, "background-color:rgb(17,17,17)")
        second_widget = gui_manager.Create_Widget("Malware Hunter", 300, 300, 500, 600,
                                                  "background-color:rgb(17,17,17)")

        widget_collection = []
        static_analysis = QWidget()
        dynamic_analysis = QWidget()

        browse_button = gui_manager.Create_Button("Browse", 400, 300, 90, 30,
                                                  "background-color:rgb(45,45,50);color: rgb(255, 255, 255)",
                                                  main_widget)
        scan_button = gui_manager.Create_Button("Scan", 180, 400, 120, 30,
                                                "background-color:rgb(45,45,50);color: rgb(255, 255, 255)", main_widget)


        path_textbox = gui_manager.Create_Textbox(87, 305, 290, 20, "background-color:rgb(255,255,255)", main_widget)
        path_label = gui_manager.Create_Label("  Exe Path ", 5, 305, 75, 20,
                                              "background-color:rgb(17,17,17); color: rgb(255, 255, 255); font: 11pt Comic Sans MS ",
                                              main_widget)
        image_label = gui_manager.Create_LabelImage("backgound_image_logo.png", 150, 50, 200, 200, main_widget)

        widget_collection.append(pair(static_analysis, "Static Analaysis"))
        widget_collection.append(pair(dynamic_analysis, "Dynamic Analaysis"))
        tabs = gui_manager.Create_Tabs(widget_collection, 0, 0, 500, 600,
                                       "QTabBar::tab {background-color:rgb(45,45,50); color: rgb(255, 255, 255);} QTabWidget::pane {border: 0px }  QTabBar::tab:selected {  background:  grey; }",
                                       second_widget)

        exe_version_label = gui_manager.Create_Label("Exe Version ", 20, 50, 100, 20,
                                                     "background-color:rgb(17,17,17); color: rgb(255, 255, 255); font: 10pt Comic Sans MS ",
                                                     static_analysis)
        md5_hash_label = gui_manager.Create_Label("MD5 Hash ", 20, 70, 100, 70,
                                                  "background-color:rgb(17,17,17); color: rgb(255, 255, 255); font: 10pt Comic Sans MS ",
                                                  static_analysis)

        exe_version_textbox = gui_manager.Create_Textbox(100, 50, 50, 20, "background-color:rgb(255,255,255)",
                                                         static_analysis)

        label32_64 = gui_manager.Create_Label("Bits ", 160, 50, 100, 20,
                                                     "background-color:rgb(17,17,17); color: rgb(255, 255, 255); font: 10pt Comic Sans MS ",
                                                     static_analysis)


        md5_hash_textbox = gui_manager.Create_Textbox(100, 95, 205, 20, "background-color:rgb(255,255,255)",
                                                      static_analysis)

        table_staticinfo = gui_manager.Create_DataTable(9, 5, 0, 200, 485, 300, "background-color:rgb(255,255,255)",
                                                        static_analysis)
        backButton = gui_manager.Create_Button("Back", 5, 515, 90, 30,
                                               "background-color:rgb(45,45,50);color: rgb(255, 255, 255)",
                                               static_analysis)

        class_label = gui_manager.Create_Label("file classification ", 20, 70, 130, 70,
                                               "background-color:rgb(17,17,17); color: rgb(255, 255, 255); font: 10pt Comic Sans MS ",
                                               dynamic_analysis)
        class_textbox = gui_manager.Create_Textbox(135, 96, 150, 20, "background-color:rgb(255,255,255)",
                                                   dynamic_analysis)
        table_dynamicinfo = gui_manager.Create_DataTable(9, 10, 0, 185, 500, 300, "background-color:rgb(255,255,255)",
                                                         dynamic_analysis)
        backButton2 = gui_manager.Create_Button("Back", 5, 515, 90, 30,
                                                "background-color:rgb(45,45,50);color: rgb(255, 255, 255)",
                                                dynamic_analysis)

        Buttons_manager = Button_Handlers()

        backButton.clicked.connect(partial(Buttons_manager.Back_button_function, main_widget, second_widget))
        backButton2.clicked.connect(partial(Buttons_manager.Back_button_function, main_widget, second_widget))

        browse_button.clicked.connect(partial(Buttons_manager.Get_FilePath, path_textbox, main_widget))
        scan_button.clicked.connect(
            partial(Buttons_manager.ScanFunction, exe_version_textbox, md5_hash_textbox, class_textbox,path_textbox, table_staticinfo,
                    second_widget, main_widget, table_dynamicinfo))

        main_widget.show()
        sys.exit(app.exec_())







    

   

