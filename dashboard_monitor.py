import sys
import socket
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QMessageBox, QTabWidget, QGroupBox, QComboBox, QGridLayout)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont

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
            # Temporarily increase timeout for long-running commands like flight reports
            if "generate" in cmd:
                self.sock.settimeout(600.0) 
            else:
                self.sock.settimeout(2.0)
                
            self.sock.sendall((cmd + '\n').encode('utf-8'))
            response = self.sock.recv(1024).decode('utf-8').strip()
            self.sock.settimeout(2.0) # Reset timeout
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
        self.setWindowTitle("Universal Robots Dashboard Controller")
        self.setMinimumSize(700, 500)
        self.client = DashboardClient("192.168.56.6") 
        
        # Polling timer (1 Hz)
        self.timer = QTimer()
        self.timer.timeout.connect(self.poll_state)
        
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        # --- Top Bar: Connection ---
        conn_layout = QHBoxLayout()
        self.ip_input = QLineEdit("192.168.56.6")
        self.btn_connect = QPushButton("Connect")
        self.btn_connect.clicked.connect(self.toggle_connection)
        conn_layout.addWidget(QLabel("Robot IP:"))
        conn_layout.addWidget(self.ip_input)
        conn_layout.addWidget(self.btn_connect)
        main_layout.addLayout(conn_layout)

        # --- Middle: Live Status & Tabs ---
        content_layout = QHBoxLayout()
        
        # Left Panel: Live Status
        status_group = QGroupBox("Live Status (Polled)")
        status_layout = QVBoxLayout()
        self.lbl_mode = QLabel("Robot Mode: Disconnected")
        self.lbl_safety = QLabel("Safety Status: Disconnected")
        self.lbl_program = QLabel("Program State: Disconnected")
        self.lbl_loaded = QLabel("Loaded: None")
        self.lbl_remote = QLabel("Remote Control: Unknown")
        self.lbl_op_mode = QLabel("Op Mode: Unknown")
        
        # Bold the labels for readability
        bold_font = QFont()
        bold_font.setBold(True)
        for lbl in [self.lbl_mode, self.lbl_safety, self.lbl_program, self.lbl_loaded, self.lbl_remote, self.lbl_op_mode]:
            lbl.setFont(bold_font)
            status_layout.addWidget(lbl)
            
        status_layout.addStretch()
        status_group.setLayout(status_layout)
        content_layout.addWidget(status_group, 1)

        # Right Panel: Control Tabs
        self.tabs = QTabWidget()
        
        # Tab 1: Core & Safety
        tab_core = QWidget()
        core_layout = QVBoxLayout()
        core_layout.addWidget(self.create_btn("Power On", "power on", "#4CAF50"))
        core_layout.addWidget(self.create_btn("Power Off", "power off", "#F44336"))
        core_layout.addWidget(self.create_btn("Brake Release", "brake release"))
        core_layout.addWidget(self.create_btn("Unlock Protective Stop", "unlock protective stop", "#FF9800"))
        core_layout.addWidget(self.create_btn("Close Safety Popup", "close safety popup"))
        core_layout.addWidget(self.create_btn("Restart Safety", "restart safety", "#FF5722"))
        core_layout.addWidget(self.create_btn("Shutdown Controller", "shutdown", "#000000", "white"))
        core_layout.addStretch()
        tab_core.setLayout(core_layout)
        self.tabs.addTab(tab_core, "Core & Safety")

        # Tab 2: Execution
        tab_exec = QWidget()
        exec_layout = QVBoxLayout()
        
        play_ctrls = QHBoxLayout()
        play_ctrls.addWidget(self.create_btn("Play", "play", "#4CAF50"))
        play_ctrls.addWidget(self.create_btn("Pause", "pause", "#FFC107", "black"))
        play_ctrls.addWidget(self.create_btn("Stop", "stop", "#F44336"))
        exec_layout.addLayout(play_ctrls)
        
        # Load Program
        load_prog_layout = QHBoxLayout()
        self.input_prog = QLineEdit("my_program.urp")
        btn_load_prog = QPushButton("Load Program")
        btn_load_prog.clicked.connect(lambda: self.run_cmd(f"load {self.input_prog.text()}"))
        load_prog_layout.addWidget(self.input_prog)
        load_prog_layout.addWidget(btn_load_prog)
        exec_layout.addLayout(load_prog_layout)

        # Load Installation
        load_inst_layout = QHBoxLayout()
        self.input_inst = QLineEdit("default.installation")
        btn_load_inst = QPushButton("Load Installation")
        btn_load_inst.clicked.connect(lambda: self.run_cmd(f"load installation {self.input_inst.text()}"))
        load_inst_layout.addWidget(self.input_inst)
        load_inst_layout.addWidget(btn_load_inst)
        exec_layout.addLayout(load_inst_layout)
        
        exec_layout.addStretch()
        tab_exec.setLayout(exec_layout)
        self.tabs.addTab(tab_exec, "Execution")

        # Tab 3: System Info & Reports
        tab_sys = QWidget()
        sys_layout = QVBoxLayout()
        
        info_grid = QGridLayout()
        info_grid.addWidget(self.create_btn("Get Serial", "get serial number"), 0, 0)
        info_grid.addWidget(self.create_btn("Get Model", "get robot model"), 0, 1)
        info_grid.addWidget(self.create_btn("PolyScope Version", "PolyscopeVersion"), 1, 0)
        info_grid.addWidget(self.create_btn("Software Version", "version"), 1, 1)
        sys_layout.addLayout(info_grid)
        
        sys_layout.addWidget(QLabel("\nWarning: Reports can take several minutes and will freeze the UI while generating."))
        
        # Flight Report
        fr_layout = QHBoxLayout()
        self.combo_fr = QComboBox()
        self.combo_fr.addItems(["system", "controller", "software"])
        btn_fr = QPushButton("Generate Flight Report")
        btn_fr.clicked.connect(lambda: self.run_cmd(f"generate flight report {self.combo_fr.currentText()}"))
        fr_layout.addWidget(self.combo_fr)
        fr_layout.addWidget(btn_fr)
        sys_layout.addLayout(fr_layout)
        
        # Support File
        sf_layout = QHBoxLayout()
        self.input_sf = QLineEdit("usbdisk")
        btn_sf = QPushButton("Generate Support File (to dir)")
        btn_sf.clicked.connect(lambda: self.run_cmd(f"generate support file {self.input_sf.text()}"))
        sf_layout.addWidget(self.input_sf)
        sf_layout.addWidget(btn_sf)
        sys_layout.addLayout(sf_layout)
        
        sys_layout.addStretch()
        tab_sys.setLayout(sys_layout)
        self.tabs.addTab(tab_sys, "System & Reports")

        # Tab 4: Tools & Logs
        tab_tools = QWidget()
        tools_layout = QVBoxLayout()
        
        popup_layout = QHBoxLayout()
        self.input_popup = QLineEdit("Hello World")
        btn_popup = QPushButton("Show Popup")
        btn_popup.clicked.connect(lambda: self.run_cmd(f"popup {self.input_popup.text()}"))
        popup_layout.addWidget(self.input_popup)
        popup_layout.addWidget(btn_popup)
        tools_layout.addLayout(popup_layout)
        tools_layout.addWidget(self.create_btn("Close Popup", "close popup"))
        
        log_layout = QHBoxLayout()
        self.input_log = QLineEdit("Custom log entry")
        btn_log = QPushButton("Add to UR Log")
        btn_log.clicked.connect(lambda: self.run_cmd(f"addToLog {self.input_log.text()}"))
        log_layout.addWidget(self.input_log)
        log_layout.addWidget(btn_log)
        tools_layout.addLayout(log_layout)
        
        op_layout = QHBoxLayout()
        self.combo_op = QComboBox()
        self.combo_op.addItems(["manual", "automatic", "brake release"])
        btn_op = QPushButton("Set Op Mode")
        btn_op.clicked.connect(lambda: self.run_cmd(f"set operational mode {self.combo_op.currentText()}"))
        op_layout.addWidget(self.combo_op)
        op_layout.addWidget(btn_op)
        tools_layout.addLayout(op_layout)
        tools_layout.addWidget(self.create_btn("Clear Operational Mode", "clear operational mode"))
        
        tools_layout.addStretch()
        tab_tools.setLayout(tools_layout)
        self.tabs.addTab(tab_tools, "Tools & Logs")

        content_layout.addWidget(self.tabs, 2)
        main_layout.addLayout(content_layout)

        # --- Bottom: Terminal Output ---
        self.lbl_terminal = QLabel("Ready.")
        self.lbl_terminal.setStyleSheet("background-color: #222; color: #0F0; padding: 5px;")
        main_layout.addWidget(self.lbl_terminal)

        central_widget.setLayout(main_layout)

    def create_btn(self, label, cmd, bg_color=None, text_color="white"):
        btn = QPushButton(label)
        if bg_color:
            btn.setStyleSheet(f"background-color: {bg_color}; color: {text_color}; font-weight: bold;")
        btn.clicked.connect(lambda: self.run_cmd(cmd))
        return btn

    def toggle_connection(self):
        if self.client.sock is None:
            self.client.ip = self.ip_input.text()
            try:
                response = self.client.connect()
                self.btn_connect.setText("Disconnect")
                self.lbl_terminal.setText(f"Connected: {response.strip()}")
                self.timer.start(1000) # Poll every 1s
            except Exception as e:
                QMessageBox.critical(self, "Connection Error", str(e))
        else:
            self.timer.stop()
            self.client.disconnect()
            self.btn_connect.setText("Connect")
            self.lbl_terminal.setText("Disconnected.")
            self.lbl_mode.setText("Robot Mode: Disconnected")
            self.lbl_safety.setText("Safety Status: Disconnected")
            self.lbl_program.setText("Program State: Disconnected")
            self.lbl_loaded.setText("Loaded: None")
            self.lbl_remote.setText("Remote Control: Unknown")
            self.lbl_op_mode.setText("Op Mode: Unknown")

    def run_cmd(self, cmd):
        self.lbl_terminal.setText(f"Sending: {cmd} ...")
        QApplication.processEvents() # Force UI update before blocking socket
        response = self.client.send_command(cmd)
        self.lbl_terminal.setText(f"Response: {response}")

    def poll_state(self):
        try:
            # Poll status quietly without updating the terminal window
            mode = self.client.send_command("robotmode").replace("Robotmode: ", "")
            safety = self.client.send_command("safetystatus").replace("Safetystatus: ", "")
            prog_state = self.client.send_command("programState")
            loaded = self.client.send_command("get loaded program").replace("Loaded program: ", "")
            remote = self.client.send_command("is in remote control")
            op_mode = self.client.send_command("get operational mode")
            
            self.lbl_mode.setText(f"Robot Mode: {mode}")
            self.lbl_safety.setText(f"Safety Status: {safety}")
            self.lbl_program.setText(f"Program State: {prog_state}")
            self.lbl_loaded.setText(f"Loaded: {loaded}")
            self.lbl_remote.setText(f"Remote Control: {remote}")
            self.lbl_op_mode.setText(f"Op Mode: {op_mode}")
        except Exception:
            pass # Ignore polling errors during longer commands

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())