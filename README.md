# MinesweeperBot

A Python bot that plays Minesweeper automatically using computer vision and screen capture. It locates the game window, reads the board state by pixel color, and applies constraint-based logic to flag mines and safely open tiles.

## Features

- Automatically detects and locates the Minesweeper window on screen
- Reads board state using PIL screen capture and pixel color matching
- Constraint-based solver: flags certain mines, opens safe tiles
- Falls back to a random guess when no deterministic move exists
- Organic (Bézier-curved) mouse movement to simulate human play

## Requirements

- Python 3.8+
- pyautogui
- Pillow
- pynput
- A running instance of [Minesweeper by Easybrain](https://apps.microsoft.com/detail/9msq6hgp5hbn) (Windows) visible on screen

## Installation

```bash
git clone https://github.com/chrisguzun/MinesweeperBot.git
cd MinesweeperBot
pip install -r requirements.txt
```

## Usage

1. Open Minesweeper and start a game so the board is visible on screen.
2. Run the bot:

```bash
python minesweeperBot.py
```

The bot will locate the board, start solving, and loop automatically after each game ends. Press **Ctrl+Shift** to stop.

> **Note:** The bot is calibrated for a specific screen resolution and Minesweeper window size. You may need to adjust pixel offsets and color thresholds in `minesweeperBot.py` if your setup differs.
