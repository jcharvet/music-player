# video_player.py
class VideoPlayer:
    def __init__(self, player):
        self.player = player
        # Initialize video player components
        self.is_playing = False

    def play_video(self):
        # Code to play video
        print("Video playback started")
        self.is_playing = True

    def stop_video(self):
        # Code to stop video
        print("Video playback stopped")
        self.is_playing = False
