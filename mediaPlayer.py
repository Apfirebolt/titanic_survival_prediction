import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QSlider,
    QMessageBox,
    QLabel,
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, Qt, QFileInfo


class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Player")
        self.setGeometry(300, 50, 900, 700)

        self.isMuted = False  # Initialize the mute state

        self.init_ui()

    def init_ui(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videowidget = QVideoWidget()

        openBtn = QPushButton("Open Video")
        openBtn.clicked.connect(self.open_file)

        playBtn = QPushButton("Play")
        playBtn.clicked.connect(self.play_video)

        pauseBtn = QPushButton("Pause")
        pauseBtn.clicked.connect(self.pause_video)

        infoBtn = QPushButton("Info")
        infoBtn.clicked.connect(self.info_video)

        fileInfoBtn = QPushButton("File Info")
        fileInfoBtn.clicked.connect(self.show_file_info)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.volumeSlider.sliderMoved.connect(self.control_volume)

        hboxLayout = QHBoxLayout()
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(playBtn)
        hboxLayout.addWidget(pauseBtn)
        hboxLayout.addWidget(infoBtn)
        hboxLayout.addWidget(fileInfoBtn)

        vboxLayout = QVBoxLayout()
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(videowidget)

        sliderLayout = QHBoxLayout()
        self.durationLabel = QLabel("00:00")
        self.durationLabel.setStyleSheet("font-size: 14px; padding: 5px;")
        self.durationLabel.setAlignment(Qt.AlignCenter)

        sliderLayout.addWidget(self.durationLabel)
        sliderLayout.addWidget(self.slider)

        vboxLayout.addLayout(sliderLayout)
        volumeLayout = QHBoxLayout()
        volumeLabel = QLabel("Volume")
        volumeLabel.setAlignment(Qt.AlignCenter)
        volumeLabel.setStyleSheet("font-size: 14px; padding: 5px;")
        volumeLayout.addWidget(volumeLabel)
        volumeLayout.addWidget(self.volumeSlider)

        self.muteBtn = QPushButton("Mute")
        self.muteBtn.clicked.connect(self.mute_video)
        volumeLayout.addWidget(self.muteBtn)

        vboxLayout.addLayout(volumeLayout)

        self.setLayout(vboxLayout)

        self.mediaPlayer.setVideoOutput(videowidget)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.mediaPlayer.positionChanged.connect(self.update_duration_label)

    def open_file(self):
        while True:
            filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
            if filename != "":
                if not filename.endswith(".mp4"):
                    error_dialog = QMessageBox()
                    error_dialog.setIcon(QMessageBox.Critical)
                    error_dialog.setText(
                        "Unsupported file format. Please select an mp4 file."
                    )
                    error_dialog.setWindowTitle("Error")
                    error_dialog.exec_()
                else:
                    self.mediaPlayer.setMedia(
                        QMediaContent(QUrl.fromLocalFile(filename))
                    )
                    self.mediaPlayer.play()
                    break

    def play_video(self):
        self.mediaPlayer.play()

    def pause_video(self):
        self.mediaPlayer.pause()

    def info_video(self):
        info_dialog = QMessageBox()
        info_dialog.setIcon(QMessageBox.Information)
        info_dialog.setText("This is a simple video player made using PyQt5.")
        info_dialog.setWindowTitle("Info")
        info_dialog.exec_()

    def control_volume(self, value):
        self.mediaPlayer.setVolume(value)

    def mute_video(self):
        self.isMuted = not self.isMuted
        self.mediaPlayer.setMuted(self.isMuted)
        self.muteBtn.setText("Unmute" if self.isMuted else "Mute")

    def show_file_info(self):
        media_content = self.mediaPlayer.media()
        if not media_content.isNull():
            file_url = media_content.canonicalUrl().toLocalFile()
            file_info = QFileInfo(file_url)
            file_name = file_info.fileName()
            file_size = file_info.size() / (1024 * 1024)  # Convert to MB

            duration = self.mediaPlayer.duration() / 1000  # Convert to seconds
            minutes, seconds = divmod(duration, 60)

            info_dialog = QMessageBox()
            info_dialog.setIcon(QMessageBox.Information)
            info_dialog.setText(
                f"File Name: {file_name}\nFile Size: {file_size:.2f} MB\nDuration: {int(minutes)}:{int(seconds):02d}"
            )
            info_dialog.setWindowTitle("File Info")
            info_dialog.exec_()

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def update_duration_label(self, position):
        duration = position / 1000  # Convert to seconds
        minutes, seconds = divmod(duration, 60)
        self.durationLabel.setText(f"{int(minutes):02d}:{int(seconds):02d}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoPlayer()
    window.show()
    sys.exit(app.exec_())
