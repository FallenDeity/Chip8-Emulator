from src.emulator import Window

if __name__ == "__main__":
    window = Window(rom_path=r"roms\Pong [Paul Vervalin, 1990].ch8")
    window.run()
