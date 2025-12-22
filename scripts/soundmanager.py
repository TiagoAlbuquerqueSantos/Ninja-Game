import pygame
from pygame.mixer import Sound, Channel
from pathlib import Path
from typing import Dict, Optional


class SoundManager:
    def __init__(self, sounds_dir: str = "assets/sounds") -> None:
        self.sounds_dir = Path(sounds_dir)
        self.sounds: Dict[str, Sound] = {}
        self.channels: Dict[str, Channel] = {}
        self.music_channel: Optional[Channel] = None

        self._load_all_sounds()

    def _load_all_sounds(self) -> None:
        """Carrega todos os arquivos de som do diretório."""
        # Estrutura esperada: assets/sounds/sfx/ e assets/sounds/music/
        sfx_dir = self.sounds_dir / "sfx"
        music_dir = self.sounds_dir / "music"

        if sfx_dir.exists():
            for sound_file in sfx_dir.glob("*.wav"):
                self.sounds[sound_file.stem] = Sound(str(sound_file))

        if music_dir.exists():
            for music_file in music_dir.glob("*.wav"):
                self.sounds[music_file.stem] = Sound(str(music_file))

    def play_sfx(self, sfx_name: str, volume: float = 1.0) -> None:
        """Reproduz um efeito sonoro."""
        if sfx_name in self.sounds:
            sound = self.sounds[sfx_name]
            sound.set_volume(volume)
            sound.play()

    def play_music(self, music_name: str, loops: int = -1) -> None:
        """Reproduz música em loop."""
        if music_name in self.sounds:
            sound = self.sounds[music_name]
            sound.play(loops=loops)

    def stop_music(self) -> None:
        """Para a música atual."""
        pygame.mixer.stop()

    def set_volume(self, sound_name: str, volume: float) -> None:
        """Ajusta volume de um som específico."""
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(max(0, min(1, volume)))
