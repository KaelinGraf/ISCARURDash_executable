import sys
import os
import socket
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QMessageBox, QTabWidget, QGroupBox, QComboBox, 
                             QGridLayout, QFrame, QSizePolicy, QSpacerItem)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QPixmap, QColor, QPalette, QIcon

# ── PolyScope-inspired colour palette ──────────────────────────────
UR_BLUE        = "#0092D2"      # Signature UR header blue
UR_BLUE_DARK   = "#006FA0"      # Darker accent / hover
UR_BLUE_LIGHT  = "#33B5E5"      # Light accent
DARK_BG        = "#1E1E1E"      # Main background
PANEL_BG       = "#2A2A2A"      # Sidebar / card panels
CARD_BG        = "#323232"      # Card surface
CARD_BORDER    = "#3E3E3E"      # Subtle card border
TEXT_PRIMARY    = "#EAEAEA"      # Primary text
TEXT_SECONDARY  = "#A0A0A0"     # Secondary / muted text
TEXT_ON_BLUE   = "#FFFFFF"      # Text on blue surfaces
GREEN          = "#4CAF50"      # Power on / play
GREEN_HOVER    = "#66BB6A"
RED            = "#E53935"      # Power off / stop / danger
RED_HOVER      = "#EF5350"
YELLOW         = "#FFB300"      # Warning / pause
YELLOW_HOVER   = "#FFCA28"
ORANGE         = "#FB8C00"      # Caution actions
NEUTRAL_BTN    = "#404040"      # Default button
NEUTRAL_HOVER  = "#505050"
TERMINAL_BG    = "#151515"      # Terminal strip
STATUS_GREEN   = "#00C853"      # Live status indicator
STATUS_RED     = "#FF1744"      # Disconnected indicator

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller bundle."""
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


# ── Global Stylesheet ──────────────────────────────────────────────
STYLESHEET = f"""
    /* ── Base ─────────────────────────────────── */
    QMainWindow {{
        background-color: {DARK_BG};
    }}
    QWidget {{
        color: {TEXT_PRIMARY};
        font-family: "Segoe UI", "Roboto", "Helvetica Neue", sans-serif;
        font-size: 13px;
    }}

    /* ── Group Boxes (cards) ──────────────────── */
    QGroupBox {{
        background-color: {CARD_BG};
        border: 1px solid {CARD_BORDER};
        border-radius: 8px;
        margin-top: 14px;
        padding: 16px 12px 12px 12px;
        font-weight: bold;
        font-size: 13px;
        color: {UR_BLUE_LIGHT};
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 2px 10px;
        color: {UR_BLUE_LIGHT};
    }}

    /* ── Tab Widget ───────────────────────────── */
    QTabWidget::pane {{
        background-color: {CARD_BG};
        border: 1px solid {CARD_BORDER};
        border-radius: 0 0 8px 8px;
        top: -1px;
    }}
    QTabBar::tab {{
        background-color: {PANEL_BG};
        color: {TEXT_SECONDARY};
        border: 1px solid {CARD_BORDER};
        border-bottom: none;
        padding: 8px 18px;
        margin-right: 2px;
        border-radius: 6px 6px 0 0;
        font-weight: bold;
        font-size: 12px;
    }}
    QTabBar::tab:selected {{
        background-color: {CARD_BG};
        color: {UR_BLUE_LIGHT};
        border-bottom: 2px solid {UR_BLUE};
    }}
    QTabBar::tab:hover:!selected {{
        background-color: {NEUTRAL_BTN};
        color: {TEXT_PRIMARY};
    }}

    /* ── Buttons (default / neutral) ──────────── */
    QPushButton {{
        background-color: {NEUTRAL_BTN};
        color: {TEXT_PRIMARY};
        border: none;
        border-radius: 6px;
        padding: 10px 18px;
        font-weight: bold;
        font-size: 13px;
        min-height: 18px;
    }}
    QPushButton:hover {{
        background-color: {NEUTRAL_HOVER};
    }}
    QPushButton:pressed {{
        background-color: {UR_BLUE_DARK};
    }}

    /* ── Line Edits ───────────────────────────── */
    QLineEdit {{
        background-color: {PANEL_BG};
        color: {TEXT_PRIMARY};
        border: 1px solid {CARD_BORDER};
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 13px;
        selection-background-color: {UR_BLUE};
    }}
    QLineEdit:focus {{
        border: 1px solid {UR_BLUE};
    }}

    /* ── Combo Boxes ──────────────────────────── */
    QComboBox {{
        background-color: {PANEL_BG};
        color: {TEXT_PRIMARY};
        border: 1px solid {CARD_BORDER};
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 13px;
        min-height: 18px;
    }}
    QComboBox:focus {{
        border: 1px solid {UR_BLUE};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 24px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {PANEL_BG};
        color: {TEXT_PRIMARY};
        selection-background-color: {UR_BLUE};
        border: 1px solid {CARD_BORDER};
    }}

    /* ── Labels ───────────────────────────────── */
    QLabel {{
        color: {TEXT_PRIMARY};
    }}

    /* ── Message Box (error / info dialogs) ──── */
    QMessageBox {{
        background-color: {CARD_BG};
        min-width: 350px;
        min-height: 120px;
    }}
    QMessageBox QLabel {{
        color: {TEXT_PRIMARY};
        font-size: 13px;
        min-width: 300px;
        padding: 8px;
    }}
    QMessageBox QPushButton {{
        background-color: {UR_BLUE};
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 24px;
        font-weight: bold;
        min-width: 80px;
    }}
    QMessageBox QPushButton:hover {{
        background-color: {UR_BLUE_LIGHT};
    }}

    /* ── Scrollbar styling ────────────────────── */
    QScrollBar:vertical {{
        background: {PANEL_BG};
        width: 8px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical {{
        background: {NEUTRAL_BTN};
        border-radius: 4px;
        min-height: 30px;
    }}
"""


class DashboardClient:
    def __init__(self, ip, port=29999):
        self.ip = ip
        self.port = port
        self.sock = None

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(2.0)
            self.sock.connect((self.ip, self.port))
            return self.sock.recv(1024).decode('utf-8')
        except Exception as e:
            self.sock = None
            raise e

    def send_command(self, cmd):
        if not self.sock:
            return "Not connected"
        try:
            if "generate" in cmd:
                self.sock.settimeout(600.0) 
            else:
                self.sock.settimeout(2.0)
            self.sock.sendall((cmd + '\n').encode('utf-8'))
            response = self.sock.recv(1024).decode('utf-8').strip()
            self.sock.settimeout(2.0)
            return response
        except Exception as e:
            return f"Error: {str(e)}"

    def disconnect(self):
        if self.sock:
            self.sock.close()
            self.sock = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UR Dashboard Monitor")
        self.setMinimumSize(820, 580)
        self.client = DashboardClient("192.168.56.6")
        self.connected = False

        # Polling timer (1 Hz)
        self.timer = QTimer()
        self.timer.timeout.connect(self.poll_state)

        self.initUI()

    # ── Helper: styled button ──────────────────────────────────────
    def create_styled_btn(self, label, cmd, bg=None, bg_hover=None, fg="white"):
        btn = QPushButton(label)
        if bg:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg};
                    color: {fg};
                    border: none;
                    border-radius: 6px;
                    padding: 10px 18px;
                    font-weight: bold;
                    font-size: 13px;
                }}
                QPushButton:hover {{
                    background-color: {bg_hover or bg};
                }}
                QPushButton:pressed {{
                    background-color: {UR_BLUE_DARK};
                }}
            """)
        btn.clicked.connect(lambda: self.run_cmd(cmd))
        btn.setCursor(Qt.PointingHandCursor)
        return btn

    # ── Separator line ─────────────────────────────────────────────
    @staticmethod
    def h_line():
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {CARD_BORDER};")
        line.setFixedHeight(1)
        return line

    # ── Build UI ───────────────────────────────────────────────────
    def initUI(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout()
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── HEADER BAR (UR Blue) ──────────────────────────────────
        header = QFrame()
        header.setFixedHeight(64)
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {UR_BLUE_DARK}, stop:1 {UR_BLUE}
                );
                border: none;
            }}
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 16, 0)

        # ISCAR logo
        logo_label = QLabel()
        pix = QPixmap(resource_path("iscar_logo.jpeg"))
        if not pix.isNull():
            logo_label.setPixmap(pix.scaledToHeight(40, Qt.SmoothTransformation))
        header_layout.addWidget(logo_label)
        header_layout.addSpacing(12)

        # Title
        title = QLabel("UR Dashboard Monitor")
        title.setStyleSheet(f"color: {TEXT_ON_BLUE}; font-size: 18px; font-weight: bold;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        # Connection indicator dot
        self.conn_dot = QLabel("●")
        self.conn_dot.setStyleSheet(f"color: {STATUS_RED}; font-size: 22px;")
        header_layout.addWidget(self.conn_dot)
        self.conn_status_lbl = QLabel("Disconnected")
        self.conn_status_lbl.setStyleSheet(f"color: {TEXT_ON_BLUE}; font-size: 12px;")
        header_layout.addWidget(self.conn_status_lbl)

        root.addWidget(header)

        # ── BODY ──────────────────────────────────────────────────
        body = QWidget()
        body.setStyleSheet(f"background-color: {DARK_BG};")
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(16, 12, 16, 8)
        body_layout.setSpacing(10)

        # ── Connection bar ────────────────────────────────────────
        conn_frame = QFrame()
        conn_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {CARD_BG};
                border: 1px solid {CARD_BORDER};
                border-radius: 8px;
            }}
        """)
        conn_inner = QHBoxLayout(conn_frame)
        conn_inner.setContentsMargins(12, 8, 12, 8)

        ip_label = QLabel("Robot IP:")
        ip_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-weight: bold; border: none;")
        conn_inner.addWidget(ip_label)

        self.ip_input = QLineEdit("192.168.56.6")
        self.ip_input.setFixedWidth(180)
        self.ip_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {PANEL_BG};
                color: {TEXT_PRIMARY};
                border: 1px solid {CARD_BORDER};
                border-radius: 6px;
                padding: 6px 10px;
            }}
            QLineEdit:focus {{ border: 1px solid {UR_BLUE}; }}
        """)
        conn_inner.addWidget(self.ip_input)

        self.btn_connect = QPushButton("Connect")
        self.btn_connect.setCursor(Qt.PointingHandCursor)
        self.btn_connect.setStyleSheet(f"""
            QPushButton {{
                background-color: {UR_BLUE};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 28px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{ background-color: {UR_BLUE_LIGHT}; }}
        """)
        self.btn_connect.clicked.connect(self.toggle_connection)
        conn_inner.addWidget(self.btn_connect)
        conn_inner.addStretch()
        body_layout.addWidget(conn_frame)

        # ── Main content: Status panel + Tabs ─────────────────────
        content = QHBoxLayout()
        content.setSpacing(10)

        # LEFT: Live Status Panel
        status_group = QGroupBox("  LIVE STATUS")
        status_layout = QVBoxLayout()
        status_layout.setSpacing(6)

        self.status_labels = {}
        status_items = [
            ("Robot Mode",    "lbl_mode",    "Disconnected"),
            ("Safety Status", "lbl_safety",  "Disconnected"),
            ("Program State", "lbl_program", "Disconnected"),
            ("Loaded",        "lbl_loaded",  "None"),
            ("Remote Ctrl",   "lbl_remote",  "Unknown"),
            ("Op Mode",       "lbl_op_mode", "Unknown"),
        ]
        for label_text, attr, default in status_items:
            row = QHBoxLayout()
            key_lbl = QLabel(label_text)
            key_lbl.setFixedWidth(105)
            key_lbl.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 12px;")
            val_lbl = QLabel(default)
            val_lbl.setStyleSheet(f"color: {TEXT_PRIMARY}; font-weight: bold; font-size: 13px;")
            row.addWidget(key_lbl)
            row.addWidget(val_lbl, 1)
            status_layout.addLayout(row)
            setattr(self, attr, val_lbl)

        status_layout.addStretch()
        status_group.setLayout(status_layout)
        status_group.setMinimumWidth(250)
        content.addWidget(status_group, 1)

        # RIGHT: Tabbed Controls
        self.tabs = QTabWidget()

        # ── Tab 1: Core & Safety ──────────────────────────────────
        tab_core = QWidget()
        core_layout = QVBoxLayout()
        core_layout.setSpacing(8)

        core_layout.addWidget(QLabel("Power & Brakes"))
        power_row = QHBoxLayout()
        power_row.addWidget(self.create_styled_btn("⏻  Power On",  "power on",  GREEN, GREEN_HOVER))
        power_row.addWidget(self.create_styled_btn("⏻  Power Off", "power off", RED,   RED_HOVER))
        core_layout.addLayout(power_row)
        core_layout.addWidget(self.create_styled_btn("🔓  Brake Release", "brake release", UR_BLUE, UR_BLUE_LIGHT))

        core_layout.addWidget(self.h_line())
        core_layout.addWidget(QLabel("Safety"))
        safety_row = QHBoxLayout()
        safety_row.addWidget(self.create_styled_btn("Unlock Protective Stop", "unlock protective stop", ORANGE, YELLOW_HOVER, "black"))
        safety_row.addWidget(self.create_styled_btn("Close Safety Popup",     "close safety popup"))
        core_layout.addLayout(safety_row)
        core_layout.addWidget(self.create_styled_btn("⚠  Restart Safety", "restart safety", RED, RED_HOVER))

        core_layout.addWidget(self.h_line())
        core_layout.addWidget(self.create_styled_btn("⏼  Shutdown Controller", "shutdown", "#37474F", "#455A64"))

        core_layout.addStretch()
        tab_core.setLayout(core_layout)
        self.tabs.addTab(tab_core, "⚡  Core && Safety")

        # ── Tab 2: Execution ──────────────────────────────────────
        tab_exec = QWidget()
        exec_layout = QVBoxLayout()
        exec_layout.setSpacing(8)

        exec_layout.addWidget(QLabel("Program Control"))
        play_row = QHBoxLayout()
        play_row.addWidget(self.create_styled_btn("▶  Play",  "play",  GREEN,  GREEN_HOVER))
        play_row.addWidget(self.create_styled_btn("⏸  Pause", "pause", YELLOW, YELLOW_HOVER, "black"))
        play_row.addWidget(self.create_styled_btn("⏹  Stop",  "stop",  RED,    RED_HOVER))
        exec_layout.addLayout(play_row)

        exec_layout.addWidget(self.h_line())
        exec_layout.addWidget(QLabel("Load Program"))
        lp_row = QHBoxLayout()
        self.input_prog = QLineEdit("my_program.urp")
        lp_row.addWidget(self.input_prog)
        btn_lp = QPushButton("Load")
        btn_lp.setStyleSheet(f"""
            QPushButton {{ background-color: {UR_BLUE}; color: white; border: none; border-radius: 6px; padding: 8px 20px; font-weight: bold; }}
            QPushButton:hover {{ background-color: {UR_BLUE_LIGHT}; }}
        """)
        btn_lp.setCursor(Qt.PointingHandCursor)
        btn_lp.clicked.connect(lambda: self.run_cmd(f"load {self.input_prog.text()}"))
        lp_row.addWidget(btn_lp)
        exec_layout.addLayout(lp_row)

        exec_layout.addWidget(QLabel("Load Installation"))
        li_row = QHBoxLayout()
        self.input_inst = QLineEdit("default.installation")
        li_row.addWidget(self.input_inst)
        btn_li = QPushButton("Load")
        btn_li.setStyleSheet(f"""
            QPushButton {{ background-color: {UR_BLUE}; color: white; border: none; border-radius: 6px; padding: 8px 20px; font-weight: bold; }}
            QPushButton:hover {{ background-color: {UR_BLUE_LIGHT}; }}
        """)
        btn_li.setCursor(Qt.PointingHandCursor)
        btn_li.clicked.connect(lambda: self.run_cmd(f"load installation {self.input_inst.text()}"))
        li_row.addWidget(btn_li)
        exec_layout.addLayout(li_row)

        exec_layout.addStretch()
        tab_exec.setLayout(exec_layout)
        self.tabs.addTab(tab_exec, "▶  Execution")

        # ── Tab 3: System & Reports ───────────────────────────────
        tab_sys = QWidget()
        sys_layout = QVBoxLayout()
        sys_layout.setSpacing(8)

        sys_layout.addWidget(QLabel("Robot Information"))
        info_grid = QGridLayout()
        info_grid.setSpacing(6)
        info_grid.addWidget(self.create_styled_btn("Serial Number",     "get serial number",  UR_BLUE, UR_BLUE_LIGHT), 0, 0)
        info_grid.addWidget(self.create_styled_btn("Robot Model",       "get robot model",    UR_BLUE, UR_BLUE_LIGHT), 0, 1)
        info_grid.addWidget(self.create_styled_btn("PolyScope Version", "PolyscopeVersion",   UR_BLUE, UR_BLUE_LIGHT), 1, 0)
        info_grid.addWidget(self.create_styled_btn("Software Version",  "version",            UR_BLUE, UR_BLUE_LIGHT), 1, 1)
        sys_layout.addLayout(info_grid)

        sys_layout.addWidget(self.h_line())
        warn = QLabel("⚠  Reports can take several minutes.")
        warn.setStyleSheet(f"color: {YELLOW}; font-size: 12px;")
        sys_layout.addWidget(warn)

        fr_row = QHBoxLayout()
        self.combo_fr = QComboBox()
        self.combo_fr.addItems(["system", "controller", "software"])
        fr_row.addWidget(self.combo_fr)
        btn_fr = QPushButton("Generate Flight Report")
        btn_fr.setCursor(Qt.PointingHandCursor)
        btn_fr.clicked.connect(lambda: self.run_cmd(f"generate flight report {self.combo_fr.currentText()}"))
        fr_row.addWidget(btn_fr)
        sys_layout.addLayout(fr_row)

        sf_row = QHBoxLayout()
        self.input_sf = QLineEdit("usbdisk")
        sf_row.addWidget(self.input_sf)
        btn_sf = QPushButton("Generate Support File")
        btn_sf.setCursor(Qt.PointingHandCursor)
        btn_sf.clicked.connect(lambda: self.run_cmd(f"generate support file {self.input_sf.text()}"))
        sf_row.addWidget(btn_sf)
        sys_layout.addLayout(sf_row)

        sys_layout.addStretch()
        tab_sys.setLayout(sys_layout)
        self.tabs.addTab(tab_sys, "📊  System && Reports")

        # ── Tab 4: Tools & Logs ───────────────────────────────────
        tab_tools = QWidget()
        tools_layout = QVBoxLayout()
        tools_layout.setSpacing(8)

        tools_layout.addWidget(QLabel("Popup Message"))
        pop_row = QHBoxLayout()
        self.input_popup = QLineEdit("Hello World")
        pop_row.addWidget(self.input_popup)
        btn_pop = QPushButton("Show Popup")
        btn_pop.setCursor(Qt.PointingHandCursor)
        btn_pop.clicked.connect(lambda: self.run_cmd(f"popup {self.input_popup.text()}"))
        pop_row.addWidget(btn_pop)
        tools_layout.addLayout(pop_row)
        tools_layout.addWidget(self.create_styled_btn("Close Popup", "close popup"))

        tools_layout.addWidget(self.h_line())
        tools_layout.addWidget(QLabel("UR Log"))
        log_row = QHBoxLayout()
        self.input_log = QLineEdit("Custom log entry")
        log_row.addWidget(self.input_log)
        btn_log = QPushButton("Add to Log")
        btn_log.setCursor(Qt.PointingHandCursor)
        btn_log.clicked.connect(lambda: self.run_cmd(f"addToLog {self.input_log.text()}"))
        log_row.addWidget(btn_log)
        tools_layout.addLayout(log_row)

        tools_layout.addWidget(self.h_line())
        tools_layout.addWidget(QLabel("Operational Mode"))
        op_row = QHBoxLayout()
        self.combo_op = QComboBox()
        self.combo_op.addItems(["manual", "automatic", "brake release"])
        op_row.addWidget(self.combo_op)
        btn_op = QPushButton("Set Op Mode")
        btn_op.setCursor(Qt.PointingHandCursor)
        btn_op.clicked.connect(lambda: self.run_cmd(f"set operational mode {self.combo_op.currentText()}"))
        op_row.addWidget(btn_op)
        tools_layout.addLayout(op_row)
        tools_layout.addWidget(self.create_styled_btn("Clear Op Mode", "clear operational mode"))

        tools_layout.addStretch()
        tab_tools.setLayout(tools_layout)
        self.tabs.addTab(tab_tools, "🔧  Tools && Logs")

        content.addWidget(self.tabs, 2)
        body_layout.addLayout(content)

        root.addWidget(body, 1)

        # ── TERMINAL / STATUS BAR ─────────────────────────────────
        terminal = QFrame()
        terminal.setFixedHeight(36)
        terminal.setStyleSheet(f"""
            QFrame {{
                background-color: {TERMINAL_BG};
                border-top: 1px solid {CARD_BORDER};
            }}
        """)
        term_layout = QHBoxLayout(terminal)
        term_layout.setContentsMargins(16, 0, 16, 0)
        term_icon = QLabel("❯")
        term_icon.setStyleSheet(f"color: {UR_BLUE_LIGHT}; font-size: 14px; font-weight: bold; border: none;")
        term_layout.addWidget(term_icon)
        self.lbl_terminal = QLabel("Ready.")
        self.lbl_terminal.setStyleSheet(f"color: {STATUS_GREEN}; font-family: 'Consolas', 'Courier New', monospace; font-size: 12px; border: none;")
        term_layout.addWidget(self.lbl_terminal, 1)
        root.addWidget(terminal)

        central.setLayout(root)

    # ── Connection toggle ──────────────────────────────────────────
    def toggle_connection(self):
        if self.client.sock is None:
            self.client.ip = self.ip_input.text()
            try:
                response = self.client.connect()
                self.connected = True
                self.btn_connect.setText("Disconnect")
                self.btn_connect.setStyleSheet(f"""
                    QPushButton {{ background-color: {RED}; color: white; border: none; border-radius: 6px; padding: 8px 28px; font-weight: bold; }}
                    QPushButton:hover {{ background-color: {RED_HOVER}; }}
                """)
                self.conn_dot.setStyleSheet(f"color: {STATUS_GREEN}; font-size: 22px;")
                self.conn_status_lbl.setText("Connected")
                self.lbl_terminal.setText(f"Connected: {response.strip()}")
                self.lbl_terminal.setStyleSheet(f"color: {STATUS_GREEN}; font-family: 'Consolas', 'Courier New', monospace; font-size: 12px; border: none;")
                self.timer.start(1000)
            except Exception as e:
                QMessageBox.critical(self, "Connection Error", str(e))
        else:
            self.timer.stop()
            self.client.disconnect()
            self.connected = False
            self.btn_connect.setText("Connect")
            self.btn_connect.setStyleSheet(f"""
                QPushButton {{ background-color: {UR_BLUE}; color: white; border: none; border-radius: 6px; padding: 8px 28px; font-weight: bold; }}
                QPushButton:hover {{ background-color: {UR_BLUE_LIGHT}; }}
            """)
            self.conn_dot.setStyleSheet(f"color: {STATUS_RED}; font-size: 22px;")
            self.conn_status_lbl.setText("Disconnected")
            self.lbl_terminal.setText("Disconnected.")
            self.lbl_terminal.setStyleSheet(f"color: {TEXT_SECONDARY}; font-family: 'Consolas', 'Courier New', monospace; font-size: 12px; border: none;")
            self.lbl_mode.setText("Disconnected")
            self.lbl_safety.setText("Disconnected")
            self.lbl_program.setText("Disconnected")
            self.lbl_loaded.setText("None")
            self.lbl_remote.setText("Unknown")
            self.lbl_op_mode.setText("Unknown")

    # ── Run command ────────────────────────────────────────────────
    def run_cmd(self, cmd):
        self.lbl_terminal.setText(f"» {cmd} …")
        self.lbl_terminal.setStyleSheet(f"color: {YELLOW}; font-family: 'Consolas', 'Courier New', monospace; font-size: 12px; border: none;")
        QApplication.processEvents()
        response = self.client.send_command(cmd)
        self.lbl_terminal.setText(f"← {response}")
        self.lbl_terminal.setStyleSheet(f"color: {STATUS_GREEN}; font-family: 'Consolas', 'Courier New', monospace; font-size: 12px; border: none;")

    # ── Polling ────────────────────────────────────────────────────
    def poll_state(self):
        try:
            mode      = self.client.send_command("robotmode").replace("Robotmode: ", "")
            safety    = self.client.send_command("safetystatus").replace("Safetystatus: ", "")
            prog      = self.client.send_command("programState")
            loaded    = self.client.send_command("get loaded program").replace("Loaded program: ", "")
            remote    = self.client.send_command("is in remote control")
            op_mode   = self.client.send_command("get operational mode")

            self.lbl_mode.setText(mode)
            self.lbl_safety.setText(safety)
            self.lbl_program.setText(prog)
            self.lbl_loaded.setText(loaded)
            self.lbl_remote.setText(remote)
            self.lbl_op_mode.setText(op_mode)
        except Exception:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())