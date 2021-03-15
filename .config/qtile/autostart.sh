#! /bin/sh

wal -i "$(< "${HOME}/.cache/wal/wal")" -q &
nitrogen --restore &
picom --experimental-backends &