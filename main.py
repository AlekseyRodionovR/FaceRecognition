import face_recognition
import numpy as np
import sys, os, datetime, cv2, sqlite3
from mydesign import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QFile, QIODevice
from ScreenshotWindow import *
from dialog import Ui_Dialog
from Dialog_python import Ui_Dialog_python

class MyWin(QtWidgets.QMainWindow):

    def __init__ (self, parent=None):
        super().__init__()
        self.ui = Ui_MainWindow() # Обращаемся к Ui_MainWindow (это наш дизайн), прописываем обращение self.ui как обращение к внутренностям формы
        self.ui.setupUi(self)
        self.cancelPressedFN = ''
        self.cancelPressedFN2 = ''
        self.loadData()
        self.sqlDataBase()
        self.setWindowIcon(QtGui.QIcon('./icons/987654.png')) # Иконка на окно

        self.ui.UploadPhoto_Tab1.clicked.connect(self.setImage) # Загрузка картинки в лэйбл на 1 вкладке
        self.ui.UploadPhoto_Tab2.clicked.connect(self.setImage2) # Загрузка картинки в лэйбл на 2 вкладке
        self.ui.OpenWebcam_Tab1.clicked.connect(self.openCamera) # Выполнение функции openCamera
        self.ui.Recognize_Tab1.clicked.connect(self.recognize) # Выполнение функции opoznatKartinku
        self.ui.Recognize_Tab2.clicked.connect(self.recognize2)
        self.ui.AddToDb_Tab1.clicked.connect(self.addInDatabase) # Кнопка для добавления данных в БД
        self.ui.Search_Tab2.textChanged.connect(self.searchInDatabase)
        self.ui.DeleteFromDb_Tab2.clicked.connect(self.deleteRecords)
        self.ui.DeletePhoto_Tab1.clicked.connect(self.deletePhotoBox1)
        self.ui.Table_Tab2.selectionModel().selectionChanged.connect(self.changeSelection)
        self.ui.SaveChanges_Tab2.clicked.connect(self.saveChanges)
        self.ui.DeletePhoto_Tab2.clicked.connect(self.deletePhotoBox2)
        self.ui.Table_Tab2.setColumnHidden(0, True)
        self.ui.About.clicked.connect(self.about)
        self.ui.pushButton_5.clicked.connect(self.press_change_DB)
        self.ui.pushButton_4.clicked.connect(self.press_add_in_DB)
        #self.ui.AboutPython.clicked.connect(self.AboutPythonDef)
        self.ui.StartRecognize.clicked.connect(self.RecognFace)

    def AboutPythonDef(self):
        Dialog_python = QtWidgets.QDialog()
        ui = Ui_Dialog_python()
        ui.setupUi(Dialog_python)
        Dialog_python.show()
        Dialog_python.exec_()

    def about(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()

    def press_change_DB(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.pushButton_5.setDisabled(bool(self))
        self.ui.pushButton_4.setEnabled(bool(self))
    def press_add_in_DB(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.pushButton_4.setDisabled(bool(self))
        self.ui.pushButton_5.setEnabled(bool(self))

    def setImage(self):
        global fileName, name_file #Делаем эту переменную глобальной,чтобы потом запросить из функции распознования
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Select Image', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)') # Открываем диалоговое окно и ставим расширения
        name_file = os.path.basename(fileName)
        print(name_file)
        if fileName == '':
            fileName = self.cancelPressedFN
        else:
            self.ui.Recognize_Tab1.setEnabled(bool(self))
            self.ui.DeletePhoto_Tab1.setEnabled(bool(self))
            self.ui.AddToDb_Tab1.setEnabled(bool(self))
            pass
        pixmapPB1 = QtGui.QPixmap(fileName) # открытому файлу присваиваем значение pixmapPB1
        pixmapPB1 = pixmapPB1.scaled(self.ui.PhotoBox_Tab1.width(), self.ui.PhotoBox_Tab1.height(), QtCore.Qt.KeepAspectRatio) # выравниваем
        self.ui.PhotoBox_Tab1.setPixmap(pixmapPB1) # Запись в imageLbl
        self.ui.PhotoBox_Tab1.setAlignment(QtCore.Qt.AlignCenter) # Выравнивание по центру
        self.show() # Показываем
        self.cancelPressedFN = fileName

    def setImage2(self):
        global fileName2
        fileName2, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Select Image', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
        if fileName2 == '':
            fileName2 = self.cancelPressedFN2
        else:
            pass
        pixmapPB2 = QtGui.QPixmap(fileName2) #открытому файлу присваиваем значение pixmapPB2
        pixmapPB2 = pixmapPB2.scaled(self.ui.PhotoBox_Tab2.width(), self.ui.PhotoBox_Tab2.height(), QtCore.Qt.KeepAspectRatio)
        self.ui.PhotoBox_Tab2.setPixmap(pixmapPB2)
        self.ui.PhotoBox_Tab2.setAlignment(QtCore.Qt.AlignCenter)
        self.show()
        self.cancelPressedFN2 = fileName2
    def recognize(self): #Функция осуществляющая распознование. По сути, на пиксмапе не рисуется квадрат, он рисуется на новом изображении,которое после прорисовки отправляется в пиксмап
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') # Загружаем основу(библиотека распознавания образов и лиц на изображении)
        selImg = fileName #запрашиваем путь до выбранного изображения
        img = cv2.imread(selImg) #читаем изображение с путем selImg
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Конвертируем исходное изображение в серый
        faces = face_cascade.detectMultiScale(gray, 1.1, 4) # Определение лиц на изображении
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Конвертируем серое изображение в RGB
        for (x, y, w, h) in faces: # Прорисовка квадратов для наглядности распознавания
            cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)#Рисуем квадраты которые нашлись в переменной faces(которая использует grayscale img) на рисунке img2(который RGB)
        #Конвертирование imread в Qimage
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qImg =  QtGui.QPixmap.fromImage(QtGui.QImage(img2.data, width, height, bytesPerLine, QImage.Format_RGB888))
        #Делаем норм скейл в Qt и отправляем в pixmap
        qImg = qImg.scaled(self.ui.PhotoBox_Tab1.width(), self.ui.PhotoBox_Tab1.height(), QtCore.Qt.KeepAspectRatio)
        self.ui.PhotoBox_Tab1.setPixmap(qImg)
        self.ui.PhotoBox_Tab1.setAlignment(QtCore.Qt.AlignCenter)

    def recognize2(self):
            db = sqlite3.connect('./DataBase/OurDataBase.db')
            cursor = db.cursor()
            try:
                lbl = self.ui.PhotoBox_Tab2
                face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') # Загружаем основу(библиотека распознавания образов и лиц на изображении)
                selImg = fileName2 #запрашиваем путь до выбранного изображения
                img = cv2.imread(selImg) #читаем изображение с путем selImg
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Конвертируем исходное изображение в серый
                faces = face_cascade.detectMultiScale(gray, 1.1, 4) # Определение лиц на изображении
                img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Конвертируем серое изображение в RGB
                for (x, y, w, h) in faces: # Прорисовка квадратов для наглядности распознавания
                    cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 3)#Рисуем квадраты которые нашлись в переменной faces(которая использует grayscale img) на рисунке img2(который RGB)
                #Конвертирование imread в Qimage
                height, width, channel = img.shape
                bytesPerLine = 3 * width
                qImg =  QtGui.QPixmap.fromImage(QtGui.QImage(img2.data, width, height, bytesPerLine, QImage.Format_RGB888))
                #Делаем норм скейл в Qt и отправляем в pixmap
                qImg = qImg.scaled(lbl.width(), lbl.height(), QtCore.Qt.KeepAspectRatio)
                lbl.setPixmap(qImg)
                lbl.setAlignment(QtCore.Qt.AlignCenter)
            except (NameError, FileNotFoundError) as error:
                indices = self.ui.Table_Tab2.selectionModel().selectedRows()
                for index in sorted(indices):
                    idInDb = index.sibling(index.row(),0).data()
                    [name], = cursor.execute('SELECT Picture FROM tableOne Where ID = ?',(idInDb,))
                    qimg = QtGui.QImage.fromData(name)# преобразование в qimg
                    pixmap = QtGui.QPixmap.fromImage(qimg)
                    QFile2 = QFile("./TEMPFILES/temp.png")
                    QFile2.open(QIODevice.WriteOnly)
                    pixmap.save(QFile2, "PNG")
                    lbl = self.ui.PhotoBox_Tab2
                    pixmapch = QPixmap("./TEMPFILES/temp.png").scaled(lbl.width(), lbl.height(), QtCore.Qt.KeepAspectRatio)
                    lbl.setPixmap(pixmapch)
                    lbl.setAlignment(QtCore.Qt.AlignCenter) # Выравнивание по центру
                    fileName = ("./TEMPFILES/temp.png")
                    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') # Загружаем основу(библиотека распознавания образов и лиц на изображении)
                    selImg = fileName #запрашиваем путь до выбранного изображения
                    img = cv2.imread(selImg) #читаем изображение с путем selImg
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Конвертируем исходное изображение в серый
                    faces = face_cascade.detectMultiScale(gray, 1.1, 4) # Определение лиц на изображении
                    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Конвертируем серое изображение в RGB
                    for (x, y, w, h) in faces: # Прорисовка квадратов для наглядности распознавания
                        cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 3)#Рисуем квадраты которые нашлись в переменной faces(которая использует grayscale img) на рисунке img2(который RGB)
                    #Конвертирование imread в Qimage
                    height, width, channel = img.shape
                    bytesPerLine = 3 * width
                    qImg =  QtGui.QPixmap.fromImage(QtGui.QImage(img2.data, width, height, bytesPerLine, QImage.Format_RGB888))
                    #Делаем норм скейл в Qt и отправляем в pixmap
                    qImg = qImg.scaled(lbl.width(), lbl.height(), QtCore.Qt.KeepAspectRatio)
                    lbl.setPixmap(qImg)
                    lbl.setAlignment(QtCore.Qt.AlignCenter)
                  #os.remove('./TEMPFILES/temp.png')
            cursor.close()
            db.close()

    def sqlDataBase(self): #Создаем таблицу
        db = sqlite3.connect('./DataBase/OurDataBase.db') #Соединяемся с бд, если она не существует - создается эта бд
        cur = db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS tableOne(ID INTEGER PRIMARY KEY,Surname TEXT,Name TEXT,Midname TEXT,DateOfBirth REAL, Institute TEXT, Function TEXT, Picture BLOB)') #, ID INTEGER #Создаем таблицу data,если она не существует, добавляем названия столбцов
        cur.close()

    def loadData(self):
        connection = sqlite3.connect('./DataBase/OurDataBase.db')
        query = "SELECT * FROM tableOne"
        result = connection.execute(query)
        self.ui.Table_Tab2.setRowCount(0)
        for row_number , row_data in enumerate(result):
            self.ui.Table_Tab2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.ui.Table_Tab2.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        connection.close()
        self.ui.Table_Tab2.resizeColumnsToContents()

    def addInDatabase(self):
        db = sqlite3.connect('./DataBase/OurDataBase.db')#Коннект к бд
        cur = db.cursor()#Открываем курсор

        def image(filename): #Функция для чтения открытого изображения
            img = open(filename,'rb') #Переводим изображение в биты
            fin = img.read() #Читаем
            return fin #Возвращаем
        try:
            imgData = image(fileName) #Записываем функцию с путем файла в переменную
        except NameError:
            imgData = image('./icons/no_image.png')
        except TypeError:
            imgData = image('./icons/no_image.png')
        binImg = sqlite3.Binary(imgData) #Извлекаем изобржение из бинарной системы,нужно чтобы добавить файл как BLOB

        listToAdd =( #Создаем список со значениями,последнее значение - BLOB, тип данных который принимает исходное значение без его конвертирования(единственное что подойдет для фото)
                      self.ui.Surname_Tab1.text(),
                      self.ui.Name_Tab1.text(),
                      self.ui.Midname_Tab1.text(),
                      self.ui.Date_Tab1.text(),
                      self.ui.Institute_Tab1.currentText(),
                      self.ui.Post_Tab1.currentText(),
                      binImg
                    )
        listToAdd2=self.ui.Name_Tab1.text()+"_"+self.ui.Surname_Tab1.text()
        Myfile = open('./FaceRecognition/SurnameName.txt','a')
        Myfile.write("\n")
        global name_file
        datawithdouplepoint=[]
        datawithdouplepoint=list({listToAdd2+" : "+name_file})
        datawithdouplepoint_end=datawithdouplepoint[0]
        Myfile.write(datawithdouplepoint_end)
        Myfile.close()
        cur.execute('INSERT INTO tableOne VALUES(NULL,?,?,?,?,?,?,?)',listToAdd) #Вставляем значения в бд
        db.commit() # Сохраняем изменения
        cur.close() # Удаляем курсор
        db.close() # Разрываем соединение с базой
        self.loadData()

    def deletePhotoBox1(self): #Удалить изображение 1ая вкладка
        self.ui.Recognize_Tab1.setDisabled(bool(self))
        self.ui.DeletePhoto_Tab1.setDisabled(bool(self))
        self.ui.AddToDb_Tab1.setDisabled(bool(self))
        global fileName
        fileName = None
        self.ui.PhotoBox_Tab1.clear()

    def deletePhotoBox2(self):
        global fileName2
        self.ui.PhotoBox_Tab2.clear()
        fileName2 = './icons/no_image.png'
        indices = self.ui.Table_Tab2.selectionModel().selectedRows()
        for index in sorted(indices):
            qimg = QtGui.QImage('./icons/no_image.png')
            pixmap = QtGui.QPixmap.fromImage(qimg).scaled(self.ui.PhotoBox_Tab2.width(), self.ui.PhotoBox_Tab2.height(), QtCore.Qt.KeepAspectRatio)
            self.ui.PhotoBox_Tab2.setPixmap(pixmap)
            self.ui.PhotoBox_Tab2.setAlignment(QtCore.Qt.AlignCenter)

    def searchInDatabase(self): #Поиск
        connection = sqlite3.connect('./DataBase/OurDataBase.db')
        query = """SELECT * FROM tableOne WHERE ? IN (
        Surname,Name,Midname,
        Surname || ' ' || Name || ' ' || Midname, /*ФИО*/
        Surname || ' ' || Midname || ' ' || Name, /*ФОИ*/
        Surname || ' ' || Name, /*ФИ*/
        Surname || ' ' || Midname, /*ФО*/
        Name || ' ' || Midname || ' ' || Surname, /*ИОФ*/
        Name || ' ' || Surname || ' ' || Midname, /*ИФО*/
        Name || ' ' || Midname, /*ИО*/
        Name || ' ' || Surname, /*ИФ*/
        Midname || ' ' || Surname || ' ' || Name, /*ОФИ*/
        Midname || ' ' || Name || ' ' || Surname, /*ОИФ*/
        Midname || ' ' || Surname, /*ОФ*/
        Midname || ' ' || Name /*ОИ*/
        )
        """
        if self.ui.Search_Tab2.text() == '':
            self.loadData()
        else:
            result = connection.execute(query,(self.ui.Search_Tab2.text(),))
            self.ui.Table_Tab2.setRowCount(0)
            for row_number , row_data in enumerate(result):
                self.ui.Table_Tab2.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.ui.Table_Tab2.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        connection.close()

    def deleteRecords(self):#Удаление
        connection = sqlite3.connect('./DataBase/OurDataBase.db')
        cursor = connection.cursor()
        indices = self.ui.Table_Tab2.selectionModel().selectedRows()
        QModelIndex = self.ui.Table_Tab2.selectionModel().currentIndex().row()
        for index in sorted(indices):
            idInDb = index.sibling(index.row(),0).data()
            self.ui.Table_Tab2.removeRow(index.row())
            self.ui.Table_Tab2.selectionModel().clearCurrentIndex()
            self.ui.Table_Tab2.selectionModel().clearSelection()
            delete_row_from_db = cursor.execute('DELETE FROM tableOne Where ID = ?',(idInDb,))
            connection.commit()
        self.ui.Surname_Tab2.clear()
        self.ui.Name_Tab2.clear()
        self.ui.Midname_Tab2.clear()
        self.ui.Date_Tab2.clear()
        self.ui.Institute_Tab2.setCurrentIndex(0)
        self.ui.Post_Tab2.setCurrentIndex(0)
        self.ui.PhotoBox_Tab2.clear()
        cursor.close()
        connection.close()

    def changeSelection(self):
        self.ui.DeleteFromDb_Tab2.setEnabled(bool(self))
        self.ui.DeletePhoto_Tab2.setEnabled(bool(self))
        self.ui.UploadPhoto_Tab2.setEnabled(bool(self))
        self.ui.Recognize_Tab2.setEnabled(bool(self))
        self.ui.SaveChanges_Tab2.setEnabled(bool(self))
        global fileName2
        connection = sqlite3.connect('./DataBase/OurDataBase.db')
        cursor = connection.cursor()
        indices = self.ui.Table_Tab2.selectionModel().selectedRows()
        for index in sorted(indices):
            idInDb = index.sibling(index.row(),0).data()
            getFromDb = cursor.execute('SELECT * FROM tableOne Where ID = ?',(idInDb,))
            listOfVars = getFromDb.fetchall()
            self.ui.Surname_Tab2.setText(listOfVars[0][1])
            self.ui.Name_Tab2.setText(listOfVars[0][2])
            self.ui.Midname_Tab2.setText(listOfVars[0][3])
            self.ui.Date_Tab2.setDate(QDate.fromString(listOfVars[0][4],"dd.MM.yyyy"))
            self.ui.Institute_Tab2.setCurrentText(listOfVars[0][5])
            self.ui.Post_Tab2.setCurrentText(listOfVars[0][6])
            qimg = QtGui.QImage.fromData(listOfVars[0][7])
            pixmap = QtGui.QPixmap.fromImage(qimg).scaled(self.ui.PhotoBox_Tab2.width(), self.ui.PhotoBox_Tab2.height(), QtCore.Qt.KeepAspectRatio)
            self.ui.PhotoBox_Tab2.setPixmap(pixmap)
            self.ui.PhotoBox_Tab2.setAlignment(QtCore.Qt.AlignCenter)
        if (len(self.ui.Table_Tab2.selectionModel().selectedRows()) <= 0):
            self.ui.Surname_Tab2.clear()
            self.ui.Name_Tab2.clear()
            self.ui.Midname_Tab2.clear()
            self.ui.Date_Tab2.clear()
            self.ui.Institute_Tab2.setCurrentIndex(0)
            self.ui.Post_Tab2.setCurrentIndex(0)
            self.ui.PhotoBox_Tab2.clear()
        cursor.close()
        connection.close()
        try:
            del fileName2
        except NameError:
            pass

    def saveChanges(self): #Сохранить изменения
        global fileName2
        connection = sqlite3.connect('./DataBase/OurDataBase.db')
        cursor = connection.cursor()
        indices = self.ui.Table_Tab2.selectionModel().selectedRows()
        for index in sorted(indices):
            idInDb = index.sibling(index.row(),0).data()
            selectedRow = self.ui.Table_Tab2.currentRow()
            getFromDb = cursor.execute('SELECT * FROM tableOne Where ID = ?',(idInDb,))
            listOfVars = getFromDb.fetchall()
        def image(filename):
                img = open(filename,'rb') 
                fin = img.read()
                return fin
        try:
            imgData = image(fileName2)
        except (NameError, FileNotFoundError) as error:
            qimg = QtGui.QImage.fromData(listOfVars[0][7])
            pixmap = QtGui.QPixmap.fromImage(qimg)
            SaveNewChangesFile = QFile("./TEMPFILES/tempSaveChanges.png")
            SaveNewChangesFile.open(QIODevice.WriteOnly)
            pixmap.save(SaveNewChangesFile, "PNG")
            fileName2 = "./TEMPFILES/tempSaveChanges.png"
            imgData = image(fileName2)
        binImg = sqlite3.Binary(imgData)
        listToAdd =(
                      self.ui.Surname_Tab2.text(),
                      self.ui.Name_Tab2.text(),
                      self.ui.Midname_Tab2.text(),
                      self.ui.Date_Tab2.text(),
                      self.ui.Institute_Tab2.currentText(),
                      self.ui.Post_Tab2.currentText(),
                      binImg,
                      idInDb
        )
        cursor.execute('UPDATE tableOne SET Surname = ?, Name = ?, Midname = ?, DateOfBirth = ?, Institute = ?, Function = ?, Picture = ? WHERE ID = ?',listToAdd)
        connection.commit() 
        cursor.close()
        connection.close()
        self.loadData()
        self.ui.Table_Tab2.selectRow(selectedRow)

    #def cameraWindow(self):
        #self.window = ScreenWin(self)
        #self.window.show()
    def RecognFace(self):
        video_capture = cv2.VideoCapture(0)
        directory = "./FaceRecognition"
        files = os.listdir(directory)
        images = list(filter(lambda x: x.endswith('.jpg'), files))
        spisok=len(images)
        img_recognition=[]
        lineList = list()
        for i in range(1,spisok+1):
            my_filename="./FaceRecognition/"+str(i)+".jpg"
            img = face_recognition.load_image_file(my_filename)
            img_recognition.append(face_recognition.face_encodings(img)[0])        
        with open("./FaceRecognition/SurnameName.txt") as f:
            for line in f:
                lineList.append(line)
        known_face_encodings = img_recognition
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        while True:
            ret, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = lineList[best_match_index]

                    face_names.append(name)

            process_this_frame = not process_this_frame


            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        video_capture.release()
        cv2.destroyAllWindows()
    def closeEvent(self,event):
        app.closeAllWindows()
    def openCamera(self):

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        cam = cv2.VideoCapture(0)
        while True:
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 10)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow("FaceDetection + Screenshot", img) # Отображение полученного с камеры изображения

            #Функция для возврата ТЕКУЩЕГО системного времени
            def currentTime():
                now = datetime.datetime.now()
                return str(now.hour)+("_")+str(now.minute)+("_")+str(now.second)+("_")+str(now.year)+("_")+str(now.month)+("_")+str(now.day)

            ch = cv2.waitKey(30) & 0xff
            if ch == 27:
                break
            if ch == ord('+'): #Вызов функции по событию нажатия кнопки "+"
                cv2.imshow("screenshot", cam.read()[1]) # Отображени сделанного скриншота
                cv2.imwrite('./PhotosForDataBase/'+ currentTime() + '.png',cam.read()[1]) # Запись на диск
                direc = "./FaceRecognition"
                fil = os.listdir(direc)
                imag = list(filter(lambda x: x.endswith('.jpg'), fil))
                sp = len(imag)+1
                cv2.imwrite('./FaceRecognition/'+ str(sp) + '.jpg',cam.read()[1]) # Запись на диск
        cv2.destroyAllWindows()
        cam.release()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
