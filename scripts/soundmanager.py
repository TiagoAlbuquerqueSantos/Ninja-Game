import pygame

from scripts.constants import VOLUME_AUDIO
from pygame.mixer import Sound
from pathlib import Path
from typing import Dict


class SoundManager:
    def __init__(self, sounds_dir: str = "assets/sounds") -> None:
        self.sounds_dir = Path(sounds_dir)
        self.sounds: Dict[str, Sound] = {}

        self._load_all_sounds()

    def _load_all_sounds(self) -> None:
        sfx_dir = self.sounds_dir / "sfx"
        music_dir = self.sounds_dir / "music"

        if sfx_dir.exists():
            for sound_file in sfx_dir.glob("*.wav"):
                self.sounds[sound_file.stem] = Sound(str(sound_file))

        if music_dir.exists():
            for music_file in music_dir.glob("*.wav"):
                self.sounds[music_file.stem] = Sound(str(music_file))

        for sound_name, volume in VOLUME_AUDIO.items():
            self.set_volume(sound_name, volume)

    def play_sfx(self, sfx_name: str) -> None:
        if sfx_name in self.sounds:
            self.sounds[sfx_name].play()

    def play_music(self, music_name: str, loops: int = -1) -> None:
        if music_name in self.sounds:
           self.sounds[music_name].play(loops=loops)

    @staticmethod
    def stop_music() -> None:
        pygame.mixer.stop()

    def set_volume(self, sound_name, volume) -> None:
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(max(0, min(1, volume)))
