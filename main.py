
import sys
from os.path import expanduser
from popplerqt4 import Poppler
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_gui import Ui_MainWindow


class MainGui(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainGui, self).__init__(parent)
        self.setupUi(self)
        w = QWidget(self)
        w.setLayout(self.main_layout)
        self.setCentralWidget(w)
        # <--------------------------- Menu tweaks --------------------------->
        lb_spacer = QLabel("")
        lb_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.tool_bar.addWidget(lb_spacer)
        self.check_autosave = QCheckBox("auto save")
        self.check_autosave.setCheckState(Qt.Checked)
        self.check_autosave.setEnabled(False)
        self.check_autosave.toggled.connect(self.change_autosave)
        self.tool_bar.addWidget(self.check_autosave)
        self.spin_time = QSpinBox()
        self.spin_time.setMinimum(1)
        self.spin_time.setMaximum(60)
        self.spin_time.setEnabled(False)
        # todo: reinitialize timer as value is changed
        self.spin_time.setValue(5)
        self.spin_time.setSuffix("min")
        self.tool_bar.addWidget(self.spin_time)
        self.tool_bar.addSeparator()
        action_help = QAction("Help", self.tool_bar)
        action_help.triggered.connect(self.show_help)
        self.tool_bar.addAction(action_help)
        self.tool_bar.addSeparator()
        action_exit = QAction("Exit", self.tool_bar)
        action_exit.triggered.connect(self.close)
        self.tool_bar.addAction(action_exit)
        # <---------------------------- Attributes --------------------------->
        self.actual_dir = expanduser("~")
        self.source_file = None
        self.source_num_pages = 0
        self.source_current_page = 0        # pdf standard is zero-index based
        self.target_num_pages = 0
        self.target_current_page = 0
        self.temp_number = 1
        self.autosave = self.check_autosave.isChecked()
        self.target_changed = False
        # <----------------------------- SIGNALS ----------------------------->
        self.bt_load_source.clicked.connect(self.open_file)
        self.spin_time.valueChanged.connect(self.set_timer_interval)
        self.timer_autosave = QTimer()
        self.timer_autosave.timeout.connect(self.save_temp_file)
        self.timer_autosave.start(6e5)      # Auto timer 5 minutes
        self.bt_first_source_page.clicked.connect(self.go_first_source_page)
        self.bt_last_source_page.clicked.connect(self.go_last_source_page)
        self.bt_next_source_page.clicked.connect(self.go_next_source_page)
        self.bt_prev_source_page.clicked.connect(self.go_prev_source_page)

    def change_autosave(self):
        self.autosave = self.check_autosave.isChecked()
        self.spin_time.setEnabled(self.autosave)
        if self.autosave:
            minutes = self.spin_time.value()
            self.timer_autosave.start(minutes*60000)
        else:
            self.timer_autosave.stop()

    def closeEvent(self, event):
        print "verify target changes"
        if self.target_changed:
            pass

    def go_first_source_page(self):
        self.source_current_page = 0
        self.show_source_page()

    def go_last_source_page(self):
        self.source_current_page = self.source_num_pages - 1
        self.show_source_page()

    def go_next_source_page(self):
        self.source_current_page += 1
        if self.source_current_page == self.source_num_pages:
            self.source_current_page -= 1
        self.show_source_page()

    def go_prev_source_page(self):
        self.source_current_page -= 1
        if self.source_current_page <0:
            self.source_current_page = 0
        self.show_source_page()

    def open_file(self):
        file_path = QFileDialog.getOpenFileName(self, "Open source file", self.actual_dir,
                                                      "PDF files (*.pdf);;All files (*.*)")
        if len(file_path) > 0:
            self.source_file = Poppler.Document.load(file_path)
            self.source_num_pages = self.source_file.numPages()
            self.show_source_page()
            # todo: Adaptar la longitud del texto a la caja
            self.tx_source_path.setText(file_path)

    def save_temp_file(self):
        print "save temp file"
        if self.target_changed:
            pass

    def set_timer_interval(self, minutes):
        self.timer_autosave.setInterval(minutes*60000)

    def show_help(self):
        pass

    def show_source_page(self):
        # todo: Si algo no va bien mostrar un mensaje (y una carita triste)
        # todo: Implementar la vista en rejilla
        # todo: En el destino implementar un arbol
        print "show {} source page".format(self.source_current_page)
        im1 = self.source_file.page(self.source_current_page).renderToImage()
        pixmap = QPixmap.fromImage(im1).scaled(self.label_source.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label_source.setPixmap(pixmap)


# Autolaucher
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(
        "QToolButton::disabled{border-style: solid; border-width: 1px; border-color: rgb(170, 170, 170);"
        " border-top-right-radius: 10px; border-bottom-left-radius: 10px;"
        " border-bottom-right-radius: 10px; padding-top: 3px; padding-right: 1px;"
        " padding-bottom: 3px; padding-left: 1px; margin: 2px;}"
        "QToolButton::enabled{border-style: solid; border-width: 1px;"
        " border-color: rgb(170, 170, 170); border-top-right-radius: 10px;"
        " border-bottom-left-radius: 10px; background-color: qlineargradient(spread:pad,"
        " x1:0, y1:0, x2:0, y2:0.5, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(192, 255, 192, 255));"
        " border-bottom-right-radius: 10px; padding-top: 3px; padding-right: 1px;"
        " padding-bottom: 3px; padding-left: 1px; margin: 2px;}"
        "QToolButton::hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,"
        " stop:0 rgba(255, 255, 255, 255), stop:1 rgba(192, 255, 192, 255));}"
        "QToolButton::pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,"
        " stop:0 rgba(128, 170, 128, 255), stop:1 rgba(192, 255, 192, 255));}"
        "QToolButton::checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,"
        " stop:0 rgba(128, 170, 128, 255), stop:1 rgba(192, 255, 192, 255));}"
        "QPushButton::disabled{border-style: solid; border-width: 1px; border-color: rgb(170, 170, 170);"
        " border-top-right-radius: 10px; border-bottom-left-radius: 10px;"
        " border-bottom-right-radius: 10px; padding-top: 3px; padding-right: 1px;"
        " padding-bottom: 3px; padding-left: 1px; margin: 2px;}"
        "QPushButton::enabled{border-style: solid; border-width: 1px;"
        " border-color: rgb(170, 170, 170); border-top-right-radius: 10px;"
        " border-bottom-left-radius: 10px; background-color: qlineargradient(spread:pad,"
        " x1:0, y1:0, x2:0, y2:0.5, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(192, 255, 192, 255));"
        " border-bottom-right-radius: 10px; padding-top: 3px; padding-right: 1px;"
        " padding-bottom: 3px; padding-left: 1px; margin: 2px;}"
        "QPushButton::hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,"
        " stop:0 rgba(255, 255, 255, 255), stop:1 rgba(192, 255, 192, 255));}"
        "QPushButton::pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,"
        " stop:0 rgba(128, 170, 128, 255), stop:1 rgba(192, 255, 192, 255));}"
        "QPushButton::checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,"
        " stop:0 rgba(128, 170, 128, 255), stop:1 rgba(192, 255, 192, 255));}"
        )
    gui = MainGui()
    active_screen = app.desktop().screenNumber(app.desktop().cursor().pos())
    gui.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, gui.size(),
                                       app.desktop().screenGeometry(active_screen)))
    gui.show()
    app.exec_()