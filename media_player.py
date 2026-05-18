import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QSlider, QLabel, QListWidget, QListWidgetItem,
    QFileDialog, QDialog, QLineEdit, QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QFont, QColor, QIcon
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import json
from pathlib import Path


class SettingsDialog(QDialog):
    """Password protected settings dialog"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 400, 200)
        self.secret_unlocked = False
        self.init_ui()
        self.apply_material3_theme()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Password prompt
        pwd_layout = QHBoxLayout()
        pwd_label = QLabel("Enter Password:")
        pwd_label.setFont(QFont("Segoe UI", 11))
        self.pwd_input = QLineEdit()
        self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pwd_input.setFont(QFont("Segoe UI", 11))
        self.pwd_input.returnPressed.connect(self.check_password)
        pwd_layout.addWidget(pwd_label)
        pwd_layout.addWidget(self.pwd_input)
        layout.addLayout(pwd_layout)
        
        # Submit button
        submit_btn = QPushButton("Unlock Settings")
        submit_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        submit_btn.clicked.connect(self.check_password)
        layout.addWidget(submit_btn)
        
        self.setLayout(layout)
        
    def check_password(self):
        """Check if password is correct - secret is 'purple bananas'"""
        password = self.pwd_input.text().strip().lower()
        
        if password == "purple bananas":
            self.secret_unlocked = True
            QMessageBox.information(self, "Success", "🔓 Secret menu unlocked!\n\nAccess Movies & Games from the menu.")
            self.accept()
        else:
            QMessageBox.warning(self, "Access Denied", "❌ Incorrect password.\n\nSettings locked.")
            self.pwd_input.clear()
            
    def apply_material3_theme(self):
        """Apply Material 3 theme"""
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFBFE;
            }
            QLineEdit {
                background-color: #F5EFF7;
                border: 2px solid #E0D7E8;
                border-radius: 8px;
                padding: 8px;
                color: #1C1B1F;
                selection-background-color: #6750A4;
            }
            QPushButton {
                background-color: #6750A4;
                color: white;
                border: none;
                border-radius: 100px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5A4B8E;
            }
            QPushButton:pressed {
                background-color: #4F4178;
            }
            QLabel {
                color: #1C1B1F;
            }
        """)


class SecretMenuDialog(QDialog):
    """Secret menu with Movies and Games - separate folders"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔐 Secret Menu")
        self.setGeometry(100, 100, 900, 600)
        self.init_ui()
        self.apply_material3_theme()
        
    def init_ui(self):
        layout = QHBoxLayout()
        
        # Movies section (left)
        movies_layout = QVBoxLayout()
        movies_title = QLabel("🎬 MOVIES")
        movies_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        movies_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        movies_layout.addWidget(movies_title)
        
        self.movies_list = QListWidget()
        self.movies_list.setFont(QFont("Segoe UI", 11))
        movies = [
            "The Matrix (1999)",
            "Inception (2010)",
            "Interstellar (2014)",
            "The Dark Knight (2008)",
            "Pulp Fiction (1994)",
            "Forrest Gump (1994)",
            "The Shawshank Redemption (1994)",
            "Gladiator (2000)"
        ]
        for movie in movies:
            self.movies_list.addItem(movie)
        movies_layout.addWidget(self.movies_list)
        layout.addLayout(movies_layout, 1)
        
        # Games section (right)
        games_layout = QVBoxLayout()
        games_title = QLabel("🎮 GAMES")
        games_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        games_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        games_layout.addWidget(games_title)
        
        self.games_list = QListWidget()
        self.games_list.setFont(QFont("Segoe UI", 11))
        games = [
            "Elden Ring",
            "Cyberpunk 2077",
            "The Witcher 3",
            "Baldur's Gate 3",
            "Starfield",
            "Hogwarts Legacy",
            "Palworld",
            "Final Fantasy VII Remake"
        ]
        for game in games:
            self.games_list.addItem(game)
        games_layout.addWidget(self.games_list)
        layout.addLayout(games_layout, 1)
        
        self.setLayout(layout)
        
    def apply_material3_theme(self):
        """Apply Material 3 theme"""
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFBFE;
            }
            QLabel {
                color: #1C1B1F;
            }
            QListWidget {
                background-color: #F5EFF7;
                border: 2px solid #E0D7E8;
                border-radius: 8px;
                color: #1C1B1F;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #6750A4;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #EADDFF;
            }
        """)


class MediaPlayer(QMainWindow):
    """Main Media Player Application with Material 3 Design"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎵 Universal Media Player")
        self.setGeometry(100, 100, 900, 700)
        
        # Media player setup
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)
        
        # State variables
        self.is_playing = False
        self.playlist = []
        self.current_index = 0
        self.secret_unlocked = False
        
        self.init_ui()
        self.apply_material3_theme()
        
    def init_ui(self):
        """Initialize the UI"""
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Top bar with title and settings
        top_layout = QHBoxLayout()
        title = QLabel("🎵 Media Player")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_layout.addWidget(title)
        
        # Settings button (top right)
        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        settings_btn.setFixedWidth(120)
        settings_btn.clicked.connect(self.open_settings)
        top_layout.addStretch()
        top_layout.addWidget(settings_btn)
        
        main_layout.addLayout(top_layout)
        
        # Current playing info
        self.info_label = QLabel("Select a file to play")
        self.info_label.setFont(QFont("Segoe UI", 11))
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.info_label)
        
        # Playlist widget
        playlist_label = QLabel("📂 Playlist")
        playlist_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        main_layout.addWidget(playlist_label)
        
        self.playlist_widget = QListWidget()
        self.playlist_widget.setFont(QFont("Segoe UI", 10))
        self.playlist_widget.itemDoubleClicked.connect(self.play_from_list)
        main_layout.addWidget(self.playlist_widget)
        
        # Load button
        load_btn = QPushButton("+ Load Files")
        load_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        load_btn.clicked.connect(self.load_files)
        main_layout.addWidget(load_btn)
        
        # Progress bar
        progress_layout = QHBoxLayout()
        self.time_label = QLabel("00:00")
        self.time_label.setFont(QFont("Segoe UI", 9))
        progress_layout.addWidget(self.time_label)
        
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setSliderPosition(0)
        self.progress_slider.sliderMoved.connect(self.set_position)
        progress_layout.addWidget(self.progress_slider)
        
        self.duration_label = QLabel("00:00")
        self.duration_label.setFont(QFont("Segoe UI", 9))
        progress_layout.addWidget(self.duration_label)
        
        main_layout.addLayout(progress_layout)
        
        # Control buttons
        controls_layout = QHBoxLayout()
        
        play_btn = QPushButton("▶️ Play")
        play_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        play_btn.clicked.connect(self.play)
        controls_layout.addWidget(play_btn)
        
        pause_btn = QPushButton("⏸ Pause")
        pause_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        pause_btn.clicked.connect(self.pause)
        controls_layout.addWidget(pause_btn)
        
        stop_btn = QPushButton("⏹ Stop")
        stop_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        stop_btn.clicked.connect(self.stop)
        controls_layout.addWidget(stop_btn)
        
        prev_btn = QPushButton("⏮ Previous")
        prev_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        prev_btn.clicked.connect(self.previous)
        controls_layout.addWidget(prev_btn)
        
        next_btn = QPushButton("⏭ Next")
        next_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        next_btn.clicked.connect(self.next)
        controls_layout.addWidget(next_btn)
        
        main_layout.addLayout(controls_layout)
        
        # Volume control
        volume_layout = QHBoxLayout()
        volume_label = QLabel("🔊 Volume:")
        volume_label.setFont(QFont("Segoe UI", 10))
        volume_layout.addWidget(volume_label)
        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.setMaximumWidth(200)
        self.volume_slider.sliderMoved.connect(self.set_volume)
        self.volume_slider.setValue(70)
        volume_layout.addWidget(self.volume_slider)
        
        volume_layout.addStretch()
        main_layout.addLayout(volume_layout)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
    def open_settings(self):
        """Open password protected settings"""
        settings_dialog = SettingsDialog(self)
        if settings_dialog.exec() == QDialog.DialogCode.Accepted:
            if settings_dialog.secret_unlocked:
                self.secret_unlocked = True
                self.show_secret_menu()
    
    def show_secret_menu(self):
        """Show the secret menu with Movies and Games"""
        secret_menu = SecretMenuDialog(self)
        secret_menu.exec()
        
    def load_files(self):
        """Load audio files into playlist"""
        files, _ = QFileDialog.getOpenFileNames(
            self, 
            "Select Audio Files", 
            "",
            "Audio Files (*.mp3 *.flac *.wav *.ogg *.m4b *.aac);;All Files (*)"
        )
        
        for file in files:
            self.playlist.append(file)
            filename = os.path.basename(file)
            self.playlist_widget.addItem(filename)
            
    def play_from_list(self, item):
        """Play selected item from playlist"""
        self.current_index = self.playlist_widget.row(item)
        self.play()
        
    def play(self):
        """Play current or selected file"""
        if self.current_index < len(self.playlist):
            file_path = self.playlist[self.current_index]
            self.player.setSource(QUrl.fromLocalFile(file_path))
            self.player.play()
            self.is_playing = True
            filename = os.path.basename(file_path)
            self.info_label.setText(f"Now Playing: {filename}")
            self.playlist_widget.setCurrentRow(self.current_index)
            
    def pause(self):
        """Pause playback"""
        if self.is_playing:
            self.player.pause()
            self.is_playing = False
            self.info_label.setText("Paused")
            
    def stop(self):
        """Stop playback"""
        self.player.stop()
        self.is_playing = False
        self.info_label.setText("Stopped")
        self.progress_slider.setValue(0)
        
    def next(self):
        """Play next track"""
        if self.current_index < len(self.playlist) - 1:
            self.current_index += 1
            self.play()
        else:
            self.stop()
            
    def previous(self):
        """Play previous track"""
        if self.current_index > 0:
            self.current_index -= 1
            self.play()
            
    def set_position(self, position):
        """Set playback position"""
        self.player.setPosition(position)
        
    def update_position(self, position):
        """Update progress slider"""
        self.progress_slider.blockSignals(True)
        self.progress_slider.setValue(position)
        self.progress_slider.blockSignals(False)
        
        # Update time label
        minutes = position // 60000
        seconds = (position % 60000) // 1000
        self.time_label.setText(f"{minutes:02d}:{seconds:02d}")
        
    def update_duration(self, duration):
        """Update duration label"""
        self.progress_slider.setRange(0, duration)
        minutes = duration // 60000
        seconds = (duration % 60000) // 1000
        self.duration_label.setText(f"{minutes:02d}:{seconds:02d}")
        
    def set_volume(self, value):
        """Set volume level"""
        self.audio_output.setVolume(value / 100.0)
        
    def on_media_status_changed(self, status):
        """Handle media status changes"""
        from PyQt6.QtMultimedia import QMediaPlayer
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.next()
            
    def apply_material3_theme(self):
        """Apply Material 3 adaptive design theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFBFE;
            }
            QWidget {
                background-color: #FFFBFE;
                color: #1C1B1F;
            }
            QLabel {
                color: #1C1B1F;
            }
            QPushButton {
                background-color: #6750A4;
                color: white;
                border: none;
                border-radius: 100px;
                padding: 8px 16px;
                font-weight: bold;
                margin: 4px;
            }
            QPushButton:hover {
                background-color: #5A4B8E;
            }
            QPushButton:pressed {
                background-color: #4F4178;
            }
            QSlider::groove:horizontal {
                background-color: #E0D7E8;
                height: 4px;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background-color: #6750A4;
                width: 18px;
                margin: -7px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background-color: #5A4B8E;
            }
            QListWidget {
                background-color: #F5EFF7;
                border: 2px solid #E0D7E8;
                border-radius: 8px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 6px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #6750A4;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #EADDFF;
            }
        """)


def main():
    app = QApplication(sys.argv)
    player = MediaPlayer()
    player.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
