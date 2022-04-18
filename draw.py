#!/usr/bin/env python3

import sys
import yaml
from dataclasses import dataclass
from enum import Enum
from typing import Optional


KEY_W = 55
KEY_H = 45
KEY_RX = 6
KEY_RY = 6
INNER_PAD_W = 2
INNER_PAD_H = 2
OUTER_PAD_W = KEY_W / 2
OUTER_PAD_H = KEY_H / 2
KEYSPACE_W = KEY_W + 2 * INNER_PAD_W
KEYSPACE_H = KEY_H + 2 * INNER_PAD_H
LINE_SPACING = 18

STYLE = """
    svg {
        font-family: SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace;
        font-size: 14px;
        font-kerning: normal;
        text-rendering: optimizeLegibility;
        fill: #24292e;
    }

    rect {
        fill: #f6f8fa;
    }

    .held {
        fill: #fdd;
    }
"""


class KeyType(Enum):
    NORMAL = ""
    HELD = "held"


@dataclass
class Key:
    tap: str
    hold: Optional[str] = None
    type: KeyType = KeyType.NORMAL


class Keymap:
    def __init__(self, split, rows, columns, thumbs, layers):
        self.split = split
        self.rows = rows
        self.columns = columns
        self.thumbs = thumbs
        self.layers = layers

        assert self.split

        self.hand_w = self.columns * KEYSPACE_W
        self.hand_h = (self.rows + (1 if self.thumbs else 0)) * KEYSPACE_H
        self.layer_w = 2 * self.hand_w + OUTER_PAD_W
        self.layer_h = self.hand_h
        self.board_w = self.layer_w + 2 * OUTER_PAD_W
        self.board_h = len(layers) * self.layer_h + (len(layers) + 1) * OUTER_PAD_H

    def print_key(self, x, y, key):
        key_class = ""
        if isinstance(key, dict):
            key_class = key.get("type", "")
            key = key["key"]
        print(
            f'<rect rx="{KEY_RX}" ry="{KEY_RY}" x="{x + INNER_PAD_W}" y="{y + INNER_PAD_H}" width="{KEY_W}" height="{KEY_H}" class="{key_class}" />'
        )
        words = key.split()
        y += (KEYSPACE_H - (len(words) - 1) * LINE_SPACING) / 2
        for word in words:
            print(
                f'<text text-anchor="middle" dominant-baseline="middle" x="{x + KEYSPACE_W / 2}" y="{y}">{word}</text>'
            )
            y += LINE_SPACING

    def print_row(self, x, y, row):
        for key in row:
            self.print_key(x, y, key)
            x += KEYSPACE_W

    def print_block(self, x, y, block):
        for row in block:
            self.print_row(x, y, row)
            y += KEYSPACE_H

    def print_layer(self, x, y, name, layer):
        self.print_block(x, y, layer["left"])
        self.print_block(
            x + self.hand_w + OUTER_PAD_W,
            y,
            layer["right"],
        )
        self.print_row(
            x + 3 * KEYSPACE_W,
            y + 3 * KEYSPACE_H,
            layer["thumbs"]["left"],
        )
        self.print_row(
            x + self.hand_w + OUTER_PAD_W,
            y + 3 * KEYSPACE_H,
            layer["thumbs"]["right"],
        )

    def print_board(self):
        print(
            f'<svg width="{self.board_w}" height="{self.board_h}" viewBox="0 0 {self.board_w} {self.board_h}" xmlns="http://www.w3.org/2000/svg">'
        )
        print(f"<style>{STYLE}</style>")

        x, y = OUTER_PAD_W, 0
        for name, layer in self.layers.items():
            y += OUTER_PAD_H
            self.print_layer(x, y, name, layer)
            y += self.layer_h

        print("</svg>")


def main():
    data = yaml.safe_load(open(sys.argv[1]))
    km = Keymap(**data['layout'], layers=data['layers'])
    km.print_board()


if __name__ == "__main__":
    main()
