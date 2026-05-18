import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QSlider, QLabel, QListWidget, QListWidgetItem,
    QFileDialog, QDialog, QLineEdit, QMessageBox, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer, QUrl, QRect, QSize
from PyQt6.QtGui import QFont, QColor, QIcon, QPixmap, QPainter, QImage
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import json
from pathlib import Path


class PixelArtCat:
    """Generate pixel art cat animations"""
    
    # Pixel art cat frames (8x8 grid)
    FRAMES = {
        'idle_blink': [
            # Frame 1: Normal
            [
                "  NN  NN ",
                " NPPPPPPN",
                "NPPPPPPPPN",
                "NPPNNNNPPN",
                "NPNNNNNNNPN",
                "NPNNNNNNPN",
                "NPPNNNNPPN",
                " NPPPPPPPN"
            ],
            # Frame 2: Blinking
            [
                "  NN  NN ",
                " NPPPPPPN",
                "NPPPPPPPPN",
                "NPPPPPPPPN",
                "NPNNNNNNNPN",
                "NPNNNNNNPN",
                "NPPNNNNPPN",
                " NPPPPPPPN"
            ]
        ],
        'idle_tail': [
            # Frame 1: Tail down
            [
                "  NN  NN ",
                " NPPPPPPN",
                "NPPPPPPPPN",
                "NPPNNNNPPN",
                "NPNNNNNNNPN",
                "NPNNNNNNPN",
                "NPPNNNNPPN",
                " NPPPPPPPN"
            ],
            # Frame 2: Tail up
            [
                "  NNNNNN ",
                " NPPPPPPN",
                "NPPPPPPPPN",
                "NPPNNNNPPN",
                "NPNNNNNNNPN",
                "NPNNNNNNPN",
                "NPPNNNNPPN",
                " NPPPPPPPN"
            ]
        ],
        'idle_headtilt': [
            # Frame 1: Head normal
            [
                "  NN  NN ",
                " NPPPPPPN",
                "NPPPPPPPPN",
                "NPPNNNNPPN",
                "NPNNNNNNNPN",
                "NPNNNNNNPN",
                "NPPNNNNPPN",
                " NPPPPPPPN"
            ],
            # Frame 2: Head tilted
            [
                "   NN NN  ",
                "  NPPPPPPN",
                " NPPPPPPPPN",
                " NPPNNNNPPN",
                " NPNNNNNNNPN",
                " NPNNNNNNPN",
                " NPPNNNNPPN",
                "  NPPPPPPPN"
            ]
        ]
    }
    
    COLORS = {
        'N': '#2D3748',  # Dark gray (outline)
        'P': '#F5A962',  # Orange (cat body)
        ' ': '#1A1A2E'   # Background
    }
    
    @staticmethod
    def render_frame(frame_data, size=256):
        """Render pixel art frame to QPixmap"""
        pixmap = QPixmap(size, size)
        pixmap.fill(QColor('#1A1A2E'))
        
        painter = QPainter(pixmap)
        pixel_size = size // 8
        
        for y, row in enumerate(frame_data):
            for x, char in enumerate(row):
                color = QColor(PixelArtCat.COLORS.get(char, '#1A1A2E'))
                painter.fillRect(x * pixel_size, y * pixel_size, pixel_size, pixel_size, color)
                # Add subtle border to pixels
                painter.drawRect(x * pixel_size, y * pixel_size, pixel_size, pixel_size)
        
        painter.end()
        return pixmap


class SettingsDialog(QDialog):
    """Password protected settings dialog"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚙️ Settings")
        self.setGeometry(100, 100, 450, 220)
        self.secret_unlocked = False
        self.init_ui()
        self.apply_dark_theme()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Settings")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Password prompt
        pwd_layout = QHBoxLayout()
        pwd_label = QLabel("🔐 Password:")
        pwd_label.setFont(QFont("Segoe UI", 11))
        self.pwd_input = QLineEdit()
        self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pwd_input.setFont(QFont("Segoe UI", 11))
        self.pwd_input.setPlaceholderText("Enter password...")
        self.pwd_input.returnPressed.connect(self.check_password)
        pwd_layout.addWidget(pwd_label)
        pwd_layout.addWidget(self.pwd_input)
        layout.addLayout(pwd_layout)
        
        # Submit button
        submit_btn = QPushButton("🔓 Unlock Settings")
        submit_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        submit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        submit_btn.clicked.connect(self.check_password)
        layout.addWidget(submit_btn)
        
        layout.addStretch()
        self.setLayout(layout)
        
    def check_password(self):
        """Check if password is correct - secret is 'purple bananas'"""
        password = self.pwd_input.text().strip().lower()
        
        if password == "purple bananas":
            self.secret_unlocked = True
            QMessageBox.information(self, "✅ Success", "🔓 Secret menu unlocked!\n\nAccess Movies & Games from the menu.")
            self.accept()
        else:
            QMessageBox.warning(self, "❌ Access Denied", "Incorrect password.\n\nSettings locked.")
            self.pwd_input.clear()
            
    def apply_dark_theme(self):
        """Apply dark mode with rounded corners"""
        self.setStyleSheet("""
            QDialog {
                background-color: #1A1A2E;
            }
            QLineEdit {
                background-color: #2D3748;
                border: 2px solid #4A5568;
                border-radius: 8px;
                padding: 8px 12px;
                color: #E2E8F0;
                selection-background-color: #7C3AED;
            }
            QLineEdit:focus {
                border: 2px solid #7C3AED;
            }
            QPushButton {
                background-color: #7C3AED;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6D28D9;
            }
            QPushButton:pressed {
                background-color: #5B21B6;
            }
            QLabel {
                color: #E2E8F0;
            }
        """)


class SecretMenuDialog(QDialog):
    """Secret menu with Movies and Games - separate folders"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔐 Secret Menu")
        self.setGeometry(100, 100, 1000, 650)
        self.init_ui()
        self.apply_dark_theme()
        
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
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
        
    def apply_dark_theme(self):
        """Apply dark mode"""
        self.setStyleSheet("""
            QDialog {
                background-color: #1A1A2E;
            }
            QLabel {
                color: #E2E8F0;
            }
            QListWidget {
                background-color: #2D3748;
                border: 2px solid #4A5568;
                border-radius: 12px;
                color: #E2E8F0;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #7C3AED;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #4A5568;
            }
        """)


class MediaPlayer(QMainWindow):
    """Main Media Player Application with Material 3 Design & Pixel Art Cat"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎵 Universal Media Player")
        self.setGeometry(100, 100, 1100, 850)
        
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
        
        # Pixel art cat animation
        self.cat_frame = 0
        self.cat_animation_index = 0
        self.cat_timer = QTimer()
        self.cat_timer.timeout.connect(self.update_cat_animation)
        self.cat_timer.start(500)  # Update every 500ms
        
        self.init_ui()
        self.apply_dark_theme()
        
    def init_ui(self):
        """Initialize the UI"""
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Top bar with title and settings
        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)
        
        title = QLabel("🎵 Media Player")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_layout.addWidget(title)
        
        # Pixel art cat display
        self.cat_label = QLabel()
        self.cat_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cat_label.setFixedSize(180, 180)
        self.update_cat_display()
        top_layout.addWidget(self.cat_label)
        
        # Settings button (top right)
        settings_btn = QPushButton("⚙️")
        settings_btn.setFont(QFont("Segoe UI", 14))
        settings_btn.setFixedSize(50, 50)
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_btn.clicked.connect(self.open_settings)
        top_layout.addStretch()
        top_layout.addWidget(settings_btn)
        
        main_layout.addLayout(top_layout)
        
        # Current playing info
        self.info_label = QLabel("▶️ Select a file to play")
        self.info_label.setFont(QFont("Segoe UI", 12))
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.info_label)
        
        # Playlist widget
        playlist_label = QLabel("📂 Playlist")
        playlist_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        main_layout.addWidget(playlist_label)
        
        self.playlist_widget = QListWidget()
        self.playlist_widget.setFont(QFont("Segoe UI", 10))
        self.playlist_widget.itemDoubleClicked.connect(self.play_from_list)
        self.playlist_widget.setMaximumHeight(180)
        main_layout.addWidget(self.playlist_widget)
        
        # Load button
        load_btn = QPushButton("+ Load Files")
        load_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        load_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        load_btn.setFixedHeight(40)
        load_btn.clicked.connect(self.load_files)
        main_layout.addWidget(load_btn)
        
        # Progress bar
        progress_layout = QHBoxLayout()
        progress_layout.setSpacing(10)
        
        self.time_label = QLabel("00:00")
        self.time_label.setFont(QFont("Segoe UI", 10))
        self.time_label.setFixedWidth(50)
        progress_layout.addWidget(self.time_label)
        
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setSliderPosition(0)
        self.progress_slider.sliderMoved.connect(self.set_position)
        progress_layout.addWidget(self.progress_slider)
        
        self.duration_label = QLabel("00:00")
        self.duration_label.setFont(QFont("Segoe UI", 10))
        self.duration_label.setFixedWidth(50)
        progress_layout.addWidget(self.duration_label)
        
        main_layout.addLayout(progress_layout)
        
        # Control buttons
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        buttons = [
            ("⏮", self.previous),
            ("⏸", self.pause),
            ("▶️", self.play),
            ("⏹", self.stop),
            ("⏭", self.next),
        ]
        
        for emoji, func in buttons:
            btn = QPushButton(emoji)
            btn.setFont(QFont("Segoe UI", 12))
            btn.setFixedHeight(45)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(func)
            controls_layout.addWidget(btn)
        
        main_layout.addLayout(controls_layout)
        
        # Volume control
        volume_layout = QHBoxLayout()
        volume_layout.setSpacing(10)
        
        volume_label = QLabel("🔊")
        volume_label.setFont(QFont("Segoe UI", 12))
        volume_layout.addWidget(volume_label)
        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.setMaximumWidth(250)
        self.volume_slider.sliderMoved.connect(self.set_volume)
        self.volume_slider.setValue(70)
        volume_layout.addWidget(self.volume_slider)
        
        volume_value = QLabel("70%")
        volume_value.setFont(QFont("Segoe UI", 10))
        volume_value.setFixedWidth(40)
        self.volume_slider.valueChanged.connect(lambda v: volume_value.setText(f"{v}%"))
        volume_layout.addWidget(volume_value)
        
        volume_layout.addStretch()
        main_layout.addLayout(volume_layout)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
    def update_cat_animation(self):
        """Update pixel art cat animation"""
        animations = ['idle_blink', 'idle_tail', 'idle_headtilt']
        current_anim = animations[self.cat_animation_index % len(animations)]
        
        frames = PixelArtCat.FRAMES[current_anim]
        self.cat_frame = (self.cat_frame + 1) % len(frames)
        
        # Change animation every 3 frames
        if self.cat_frame == 0:
            self.cat_animation_index += 1
        
        self.update_cat_display()
        
    def update_cat_display(self):
        """Display current cat frame"""
        animations = ['idle_blink', 'idle_tail', 'idle_headtilt']
        current_anim = animations[self.cat_animation_index % len(animations)]
        frames = PixelArtCat.FRAMES[current_anim]
        frame_data = frames[self.cat_frame % len(frames)]
        pixmap = PixelArtCat.render_frame(frame_data, 160)
        self.cat_label.setPixmap(pixmap)
        
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
            self.info_label.setText(f"▶️ Now Playing: {filename}")
            self.playlist_widget.setCurrentRow(self.current_index)
            
    def pause(self):
        """Pause playback"""
        if self.is_playing:
            self.player.pause()
            self.is_playing = False
            self.info_label.setText("⏸ Paused")
            
    def stop(self):
        """Stop playback"""
        self.player.stop()
        self.is_playing = False
        self.info_label.setText("⏹ Stopped")
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
            
    def apply_dark_theme(self):
        """Apply dark mode with rounded corners"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1A1A2E;
            }
            QWidget {
                background-color: #1A1A2E;
                color: #E2E8F0;
            }
            QLabel {
                color: #E2E8F0;
            }
            QPushButton {
                background-color: #7C3AED;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6D28D9;
            }
            QPushButton:pressed {
                background-color: #5B21B6;
            }
            QSlider::groove:horizontal {
                background-color: #2D3748;
                height: 6px;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background-color: #7C3AED;
                width: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background-color: #6D28D9;
            }
            QListWidget {
                background-color: #2D3748;
                border: 2px solid #4A5568;
                border-radius: 12px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #7C3AED;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #4A5568;
            }
            QScrollBar:vertical {
                background-color: #2D3748;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #7C3AED;
                border-radius: 6px;
            }
        """)


def main():
    app = QApplication(sys.argv)
    player = MediaPlayer()
    player.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
