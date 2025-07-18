import sys
import os
import json
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy,
    QPushButton, QScrollArea, QGridLayout, QMessageBox, QLineEdit
)
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QCursor, QFontDatabase, QFont
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve


def colorize_icon(path, color=QColor("#A259F7")):
    pixmap = QPixmap(path)
    if pixmap.isNull():
        print(f"Failed to load icon: {path}")
        return QIcon()

    tinted = QPixmap(pixmap.size())
    tinted.fill(Qt.transparent)

    painter = QPainter(tinted)
    painter.setCompositionMode(QPainter.CompositionMode_Source)
    painter.drawPixmap(0, 0, pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(tinted.rect(), color)
    painter.end()

    return QIcon(tinted)


class HoverButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hover_anim = QPropertyAnimation(self, b"geometry")
        self.hover_anim.setDuration(150)
        self.hover_anim.setEasingCurve(QEasingCurve.OutQuad)
        self._original_rect = None

        self.click_anim = QPropertyAnimation(self, b"geometry")
        self.click_anim.setDuration(100)
        self.click_anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.click_anim.finished.connect(self._on_click_anim_finished)

    def enterEvent(self, event):
        if not self._original_rect:
            self._original_rect = self.geometry()

        new_rect = self._original_rect.adjusted(
            -self._original_rect.width() * 0.05,
            -self._original_rect.height() * 0.05,
            self._original_rect.width() * 0.05,
            self._original_rect.height() * 0.05,
        )
        self.hover_anim.stop()
        self.hover_anim.setStartValue(self.geometry())
        self.hover_anim.setEndValue(new_rect)
        self.hover_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hover_anim.stop()
        self.hover_anim.setStartValue(self.geometry())
        self.hover_anim.setEndValue(self._original_rect)
        self.hover_anim.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if not self._original_rect:
            self._original_rect = self.geometry()

        smaller_rect = self._original_rect.adjusted(
            self._original_rect.width() * 0.05,
            self._original_rect.height() * 0.05,
            -self._original_rect.width() * 0.05,
            -self._original_rect.height() * 0.05,
        )
        self.click_anim.stop()
        self.click_anim.setStartValue(self.geometry())
        self.click_anim.setEndValue(smaller_rect)
        self.click_anim.start()
        super().mousePressEvent(event)

    def _on_click_anim_finished(self):
        cursor_inside = self.rect().contains(self.mapFromGlobal(QCursor.pos()))
        if cursor_inside and self._original_rect:
            target_rect = self._original_rect.adjusted(
                -self._original_rect.width() * 0.05,
                -self._original_rect.height() * 0.05,
                self._original_rect.width() * 0.05,
                self._original_rect.height() * 0.05,
            )
        else:
            target_rect = self._original_rect

        self.click_anim.setStartValue(self.geometry())
        self.click_anim.setEndValue(target_rect)
        self.click_anim.start()


class ProjectCard(QWidget):
    def __init__(self, project_data: dict, click_callback=None):
        super().__init__()
        self.project_data = project_data
        self.click_callback = click_callback
        self.setFixedSize(260, 140)
        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet("""
            background-color: #2D033B;
            border-radius: 12px;
            color: #fff;
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Project name at the top
        name_label = QLabel(project_data.get("name", "Unnamed Project"))
        name_label.setStyleSheet("color: #A259F7; font-size: 18px; font-weight: bold; padding: 12px 16px 6px 16px;")
        layout.addWidget(name_label)

        # Info rows (Created, Updated, Engine)
        info_rows = [
            ("#A259F7", "\U0001F4C5", f"Created: {project_data.get('created', '')[:19]}"),
            ("#A259F7", "\U0001F6E0", f"Updated: {project_data.get('updated', '')[:19]}"),
            ("#F75990", "\U0001F9E0", f"Engine: {project_data.get('engine', {}).get('type', '2D')} {project_data.get('engine', {}).get('version', '0.0.0-0')}")
        ]
        for i, (bg_color, icon, text) in enumerate(info_rows):
            info_widget = QWidget()
            info_layout = QHBoxLayout(info_widget)
            info_layout.setContentsMargins(16, 0 if i > 0 else 6, 16, 0)
            info_layout.setSpacing(8)
            info_widget.setStyleSheet(f"background: {bg_color}; border-radius: 0px;" + ("border-bottom-left-radius: 12px; border-bottom-right-radius: 12px;" if i == len(info_rows)-1 else ""))
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 15px; color: #fff;")
            info_layout.addWidget(icon_label)
            text_label = QLabel(text)
            text_label.setStyleSheet("color: #fff; font-size: 14px;")
            info_layout.addWidget(text_label)
            info_layout.addStretch(1)
            layout.addWidget(info_widget)

    def mousePressEvent(self, event):
        if self.click_callback:
            self.click_callback(self.project_data.get("name", "Unknown"))
        super().mousePressEvent(event)


class Sidebar(QWidget):
    def __init__(self, icon_data, button_callbacks):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)

        self.buttons = {}

        for icon_name, tooltip, callback_key in icon_data:
            icon_path = os.path.abspath(os.path.join("Resources", "Icons", icon_name))
            print(f"Loading icon from: {icon_path}")

            if not os.path.exists(icon_path):
                print(f"Warning: Icon file not found: {icon_path}")

            icon = colorize_icon(icon_path, QColor("#A259F7"))

            btn = HoverButton()
            btn.setIcon(icon)
            btn.setIconSize(QSize(32, 32))
            btn.setFixedSize(56, 56)
            btn.setStyleSheet("""
                QPushButton {
                    background: #232136;
                    border: 1px solid #2B2840;
                    border-radius: 18px;
                }
            """)
            btn.setToolTip(tooltip)

            if callback_key in button_callbacks:
                btn.clicked.connect(button_callbacks[callback_key])

            layout.addWidget(btn)
            self.buttons[callback_key] = btn

        layout.addStretch(1)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        logo_path = os.path.abspath(os.path.join("Resources", "Logo.png"))
        self.setWindowIcon(QIcon(logo_path))

        self.setWindowTitle("Vortex - Home")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QWidget {
                background: #181824;
                color: #fff;
            }
            QLineEdit {
                background: #232136;
                border: 1px solid #2B2840;
                border-radius: 6px;
                padding: 6px 10px;
                color: #A259F7;
                font-size: 16px;
            }
        """)

        main_layout = QHBoxLayout(self)
        self.main_layout = main_layout

        icon_data = [
            ("house-solid.png", "Home", "home"),
            ("plus-solid.png", "Add Project", "add"),
        ]

        callbacks = {
            "home": self.show_welcome,
            "add": self.show_create_project,
        }

        sidebar = Sidebar(icon_data, callbacks)
        sidebar.setStyleSheet("""
            background: #2D033B;
            border-top-left-radius: 16px;
            border-bottom-left-radius: 16px;
        """)
        main_layout.addWidget(sidebar)

        self.content_widget = None
        self.logo_path = logo_path
        self.projects_dir = os.path.abspath("projects")

        self.show_welcome()

    def clear_content(self):
        if self.content_widget is not None:
            self.main_layout.removeWidget(self.content_widget)
            self.content_widget.deleteLater()
            self.content_widget = None

    def open_project(self, project_name):
        QMessageBox.information(self, "Project Clicked", f"You clicked project:\n{project_name}")

    def show_welcome(self):
        self.clear_content()

        try:
            username = os.getlogin()
        except Exception:
            username = os.environ.get('USERNAME', 'User')

        container = QWidget()
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(20, 20, 20, 20)
        vbox.setSpacing(25)

        # Welcome Section
        welcome_widget = QWidget()
        welcome_layout = QHBoxLayout(welcome_widget)
        welcome_layout.setContentsMargins(0, 0, 0, 0)
        welcome_layout.setSpacing(20)

        pixmap = QPixmap(self.logo_path)
        pixmap = pixmap.scaled(96, 96, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pic_label = QLabel()
        pic_label.setPixmap(pixmap)
        pic_label.setAlignment(Qt.AlignCenter)

        welcome_text = QLabel(f"Welcome back, {username}!")
        welcome_text.setStyleSheet("color: #A259F7; font-size: 32px; font-weight: bold;")
        welcome_text.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        welcome_layout.addWidget(pic_label)
        welcome_layout.addWidget(welcome_text)
        welcome_layout.addStretch()

        vbox.addWidget(welcome_widget)

        # Projects Section Title (with icon and subtitle)
        projects_header = QWidget()
        projects_header_layout = QHBoxLayout(projects_header)
        projects_header_layout.setContentsMargins(0, 0, 0, 0)
        projects_header_layout.setSpacing(12)
        projects_title = QLabel("Your Projects")
        projects_title.setStyleSheet("color: #A259F7; font-size: 24px; font-weight: bold;")
        projects_header_layout.addWidget(projects_title)
        subtitle = QLabel("Manage and open your recent projects below.")
        subtitle.setStyleSheet("color: #CCCCCC; font-size: 14px;")
        projects_header_layout.addWidget(subtitle)
        projects_header_layout.addStretch()
        vbox.addWidget(projects_header)

        # Scroll area for projects
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")

        projects_container = QWidget()
        projects_layout = QGridLayout(projects_container)
        projects_layout.setContentsMargins(0, 0, 0, 0)
        projects_layout.setSpacing(24)

        # Load projects from folder
        # Load project data from .vortexproject file
        projects = []
        if os.path.exists(self.projects_dir):
            for folder in sorted(os.listdir(self.projects_dir)):
                project_path = os.path.join(self.projects_dir, folder)
                metadata_path = os.path.join(project_path, ".vortexproject")
                if os.path.isdir(project_path) and os.path.isfile(metadata_path):
                    try:
                        with open(metadata_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            projects.append(data)
                    except Exception as e:
                        print(f"Failed to load project {folder}: {e}")
        else:
            print(f"Projects folder not found at {self.projects_dir}")

        if not projects:
            # Improved empty state
            empty_widget = QWidget()
            empty_layout = QVBoxLayout(empty_widget)
            empty_layout.setAlignment(Qt.AlignCenter)
            empty_icon = QLabel()
            empty_icon.setPixmap(QPixmap(os.path.join("Resources", "Icons", "plus-solid.png")).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            empty_icon.setAlignment(Qt.AlignCenter)
            empty_layout.addWidget(empty_icon)
            no_proj_label = QLabel("No projects found. Start by creating a new project!")
            no_proj_label.setStyleSheet("color: #A259F7; font-size: 20px; font-style: italic;")
            no_proj_label.setAlignment(Qt.AlignCenter)
            empty_layout.addWidget(no_proj_label)
            create_btn = HoverButton("Create New Project")
            create_btn.setFixedWidth(200)
            create_btn.setStyleSheet("""
                QPushButton {
                    background: #A259F7;
                    border: none;
                    border-radius: 10px;
                    color: white;
                    font-size: 18px;
                    font-weight: bold;
                    padding: 10px 0;
                }
                QPushButton:hover {
                    background: #8e44ad;
                }
            """)
            create_btn.clicked.connect(self.show_create_project)
            empty_layout.addWidget(create_btn)
            vbox.addWidget(empty_widget)
        else:
            columns = 2
            row = 0
            col = 0
            # Add a 'New Project' card at the start
            new_proj_card = HoverButton()
            new_proj_card.setFixedSize(260, 160)
            new_proj_card.setStyleSheet("""
                QPushButton {
                    background: #232136;
                    border: 2px dashed #A259F7;
                    border-radius: 12px;
                    color: #A259F7;
                    font-size: 18px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #2D033B;
                }
            """)
            new_proj_card.setText("+ New Project")
            new_proj_card.clicked.connect(self.show_create_project)
            projects_layout.addWidget(new_proj_card, row, col)
            col += 1
            for project_data in projects:
                card = ProjectCard(project_data, click_callback=self.open_project)
                projects_layout.addWidget(card, row, col)
                col += 1
                if col >= columns:
                    col = 0
                    row += 1

            scroll.setWidget(projects_container)
            scroll.setFixedHeight(400)
            vbox.addWidget(scroll)


        self.content_widget = container
        self.main_layout.addWidget(self.content_widget, 1)

    def show_create_project(self):
        self.clear_content()

        container = QWidget()
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(40, 40, 40, 40)
        vbox.setSpacing(25)

        title = QLabel("Create a New Project")
        title.setStyleSheet("color: #A259F7; font-size: 28px; font-weight: bold;")
        vbox.addWidget(title)

        self.project_name_input = QLineEdit()
        self.project_name_input.setPlaceholderText("Enter project name...")
        vbox.addWidget(self.project_name_input)

        create_btn = HoverButton("Create")
        create_btn.setFixedWidth(150)
        create_btn.setStyleSheet("""
            QPushButton {
                background: #A259F7;
                border: none;
                border-radius: 10px;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 10px 0;
            }
            QPushButton:hover {
                background: #8e44ad;
            }
        """)
        create_btn.clicked.connect(self.create_project)
        vbox.addWidget(create_btn)

        self.content_widget = container
        self.main_layout.addWidget(self.content_widget, 1)

    def create_project(self):
        project_name = self.project_name_input.text().strip()
        if not project_name:
            QMessageBox.warning(self, "Error", "Project name cannot be empty.")
            return

        if any(c in project_name for c in r'<>:"/\\|?*'):
            QMessageBox.warning(self, "Error", "Project name contains invalid characters.")
            return

        project_path = os.path.join(self.projects_dir, project_name)

        try:
            if not os.path.exists(self.projects_dir):
                os.makedirs(self.projects_dir)

            if os.path.exists(project_path):
                QMessageBox.warning(self, "Error", "A project with this name already exists.")
                return

            os.makedirs(project_path)

            # Create project.json metadata file
            now = datetime.now().isoformat()
            metadata = {
                "name": project_name,
                "created": now,
                "updated": now,
                "engine": {
                    "version": "0.0.0-0",
                    "type": "2D"
                }
            }
            metadata_path = os.path.join(project_path, ".vortexproject")
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)

            QMessageBox.information(self, "Success", f"Project '{project_name}' created successfully!")
            self.show_welcome()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create project:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load Inter font from Resources/Inter.ttc
    font_path = os.path.abspath(os.path.join("Resources", "Inter.ttc"))
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print("Failed to load Inter font.")
    else:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(font_family))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
