#! /bin/sh

# wal -i "$(< "${HOME}/.cache/wal/wal")" -q &
lxsession &
picom --experimental-backends &
nitrogen --restore &