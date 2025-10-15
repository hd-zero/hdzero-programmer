import pathlib
import sys
from pathlib import Path

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QMainWindow,
    QFrame,
    QPushButton,
    QStackedWidget,
    QFileDialog,
    QTableView,
    QTextBrowser,
)
from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon
from app.core.custom_logger import setup_logger
from app.core.CoreInterface import CoreInterface

logger = setup_logger()


class MainWindow(QMainWindow):
    """
    Main window class for connected widgets and controls.
    """

    def __init__(self):
        """
        Load window and connect widgets.
        """
        super().__init__()
        loader = QUiLoader()
        if getattr(sys, "frozen", False):
            ui_file = Path(__file__).parent.parent.parent / "lib" / "ui" / "main_window.ui"
        else:
            ui_file = Path(__file__).parent.parent / "ui" / "main_window.ui"
        logger.info(f"Loading {ui_file}")
        self.ui = loader.load(ui_file)
        self.setCentralWidget(self.ui)

        # load core
        self.core = CoreInterface()

        # load style sheet
        self.setStyleSheet(self.load_style_from_file())

        # setup title and icon
        self.setWindowTitle("HDZero Programmer v2")
        icon_pth = pathlib.Path(__file__).parent.parent / "src" / "icons" / "HDZeroIcon.ico"
        self.setWindowIcon(QIcon(str(icon_pth)))

        # assign widgets objet with variables
        self.left_sidebar_frame = self.ui.findChild(QFrame, "left_sidebar_frame")
        self.btn_toggle_menu = self.ui.findChild(QPushButton, "btn_toggle_menu")
        self.stacked_widget = self.ui.findChild(QStackedWidget, "stackedWidget")
        self.btn_sidebar_home = self.ui.findChild(QPushButton, "btn_sidebar_home")
        self.btn_sidebar_vtx = self.ui.findChild(QPushButton, "btn_sidebar_vtx")
        self.btn_sidebar_eventVrx = self.ui.findChild(QPushButton, "btn_sidebar_eventVrx")
        self.btn_sidebar_info = self.ui.findChild(QPushButton, "btn_sidebar_info")
        self.btn_sidebar_settings = self.ui.findChild(QPushButton, "btn_sidebar_settings")
        self.btn_load_fw_local_vtx = self.ui.findChild(QPushButton, "btn_load_fw_local_vtx")
        self.tb_vtx = self.ui.findChild(QTextBrowser, "tb_vtx")
        self.tb_vtx.setReadOnly(True)

        # VTX page stackedWidget
        self.btn_vtx_connect = self.ui.findChild(QPushButton, "btn_vtx_connect")

        # left sidebar run settings
        self.is_container_expanded = True
        self.expanded_width_on_start = 200

        # pre-setup startup page
        self.stacked_widget.setCurrentIndex(0)

        # connect widgets with func
        self.btn_toggle_menu.clicked.connect(self.toggle_left_sidebar_frame_width)
        self.btn_sidebar_home.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_sidebar_vtx.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_sidebar_info.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.btn_sidebar_settings.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.btn_sidebar_eventVrx.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.btn_load_fw_local_vtx.clicked.connect(self.on_load_fw_local_vtx)
        self.btn_close_app.clicked.connect(self.close_app)

        # connect VTX buttons with func
        self.btn_vtx_connect.clicked.connect(self.vtx_connect_function)

    def toggle_left_sidebar_frame_width(self) -> None:
        """Animation sidebar"""
        start_width = self.left_sidebar_frame.width()

        # setup animate properties
        if self.is_container_expanded:
            end_width = 65
        else:
            end_width = self.expanded_width_on_start

        # create animation properties
        self.animation = QPropertyAnimation(self.left_sidebar_frame, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(start_width)
        self.animation.setEndValue(end_width)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        self.animation.start()

        self.is_container_expanded = not self.is_container_expanded

    @staticmethod
    def load_style_from_file():
        """Load window style from the file."""
        style_path = pathlib.Path(__file__).parent.parent / "src" / "styles" / "styles.qss"
        with open(style_path, "r") as f:
            style_sheet = f.read()
            return style_sheet

    def select_file(self) -> tuple[str, str]:
        """Select a path using the os window"""
        return QFileDialog.getOpenFileName(self, "Choose file", "", "Bin(*.bin);;All Files (*)")

    def on_load_fw_local_vtx(self) -> None:
        """Choose a file to flash for vtx"""
        path_to_file = self.select_file()
        if len(path_to_file[0]) > 0:
            _f = self.core.file_path = path_to_file[0]
        else:
            _f = "Error!! -> Wrong file selected"
        self.tb_vtx.setText(f"Bin File: {_f}")

    def vtx_connect_function(self) -> None:
        """Function for connect action with button @connect in vtx page"""
        ...

    def vtx_disconnect_function(self) -> None:
        """Function for connect action with button @disconnect in vtx page"""
        ...

    def vtx_backup_function(self) -> None:
        """Function for connect action with button @backup in vtx page"""
        ...

    def vtx_flash_function(self) -> None:
        """Function for connect action with button @flash in vtx page"""
        ...

    def close_app_function(self) -> None:
        """Function for connect action with button @close_app"""
        ...
