#!/bin/sh

wal -i "$(< "${HOME}/.cache/wal/wal")" -q &
lxsession &
setxkbmap -model abnt2 -layout br -variant abnt2 &
picom --experimental-backends &
nitrogen --restore &
volumeicon &
