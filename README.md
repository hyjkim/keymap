# Keymap Visualizer

This is a visualizer for keymaps, similar to [`keymap`](https://github.com/callum-oakley/keymap) that it is forked from.

## Differences from original
- Support custom-sized layouts
    - Non-split layout support in the future
- Read layout and keymap definitions from yaml files
- Support for hold-tap keys
- Support for combos
    - Only two non-thumb neighboring positions for now
    - Defined by ZMK-like index positions
- Layer labels
- Slightly different styling

For expected input schema, please see examples in [keymaps] folder.

## Example layout
Below is an example layout generated with `python draw.py keymaps/3x5+2.formal.yaml >keymap.svg`:

![3x5+2 "formal" layout](svg/3x5+2.formal.svg)
