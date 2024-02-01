
from PySide6.QtCore import Slot, QSize, Signal, QObject, Qt
from PySide6.QtGui import QCloseEvent, QIcon, QPixmap, QImage
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QFrame, QPushButton,
    QVBoxLayout, QLabel, QHBoxLayout, QFileDialog
)

import os
from glob import glob
import numpy as np
import cv2
from tqdm import tqdm
from pathlib import Path

class Signals(QObject):
    wheel_controller = Signal(int)
    current_file_info = Signal(dict)
    
signal = Signals()



class ImageLabel(QLabel):
    def __init__(self, obj_name: str):
        super().__init__()
        self.setFixedSize(640, 640)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setText("\n\n Drop Image Here \n\n")
        self.setStyleSheet(
            """
            QLabel{
                border: 3px dashed #aaa
            }
        """
        )
        # all_signals.image_size.emit("")
        self.setObjectName(obj_name)

    def setPixmap(self, image):
        super().setPixmap(image)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.preprocess(file_path)
            event.accept()
        else:
            event.ignore()
            
    def wheelEvent(self, event):
        signal.wheel_controller.emit(event.angleDelta().y())
        
    def preprocess(self, file_path: str):
        root_path = '/'.join(os.path.dirname(__file__).split('\\')[:-1])
        method = ""
        if "train" in file_path:
            new_file_path = file_path.split("train/")[-1]
            method = "train_jpg"
        else:
            new_file_path = file_path.split("valid/")[-1]
            method = "valid_jpg"
        plane = new_file_path.split("/")[0]
        file_name = new_file_path.split("/")[-1].replace('.npy', '')
        save_path = os.path.join(root_path, method, plane, file_name)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
            np_img = np.load(file_path)
            for idx in range(np_img.shape[0]):
                img = np_img[idx, :, :]
                img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                cv2.imwrite(os.path.join(save_path, f'{idx}.jpg'), img)
                
            _info =  {
                "plane": plane,
                "save_path": save_path,
                "file_name": file_name,
                "method": method,
                "length": np_img.shape[0]
            }
            signal.current_file_info.emit(_info)
        else:
            print("Already exist")


class MainWindow(QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        self.initial_window()
        
    def initial_window(self) -> None:
        self.setFixedSize(QSize(720, 800))
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        self.title_label = QLabel("")
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)
        
        img_frame = QFrame()
        img_layout = QHBoxLayout()
        self.original_label = ImageLabel("label")
        img_layout.addWidget(self.original_label)
        img_frame.setLayout(img_layout)
        main_layout.addWidget(img_frame)
        
        btn_frame = QFrame()
        btn_layout = QHBoxLayout()
        formal_btn = QPushButton("<")
        next_btn = QPushButton(">")
        btn_layout.addWidget(formal_btn)
        btn_layout.addWidget(next_btn)
        btn_frame.setLayout(btn_layout)
        main_layout.addWidget(btn_frame)    
        main_widget.setLayout(main_layout)           
        self.setCentralWidget(main_widget)   
        
        formal_btn.clicked.connect(self.formal_img)
        next_btn.clicked.connect(self.next_img)
        signal.wheel_controller.connect(self.change_idx)
        signal.current_file_info.connect(self.set_current_img_folder)
        
    @Slot(dict)
    def set_current_img_folder(self, folder_name: dict):
        self.file_name = folder_name["file_name"]
        self.plane = folder_name["plane"]
        self.save_path = folder_name["save_path"]
        self.length = folder_name["length"]
        self.current_idx = 0
        self.set_img()

    def set_img(self):
        _file_name = os.path.join(self.save_path, f'{self.current_idx}.jpg')
        self.title_label.setText(
            "Plane: {}, File Name: {}, Length: {}, Index: {}" \
                .format(self.plane, self.file_name, self.length, self.current_idx)
        )
        self.original_label.setPixmap(QPixmap(QImage(_file_name).scaled(640, 640)))

    def next_img(self):
        if self.current_idx < self.length-1:
            self.current_idx += 1
            self.set_img()
        
    def formal_img(self):
        if self.current_idx > 0:
            self.current_idx -= 1
            self.set_img()
            
    @Slot(int)    
    def change_idx(self, value: int):
        if value > 0:
            self.next_img()
        else:
            self.formal_img()