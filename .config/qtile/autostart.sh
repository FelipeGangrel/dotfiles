#!/bin/sh

wal -i "$(< "${HOME}/.cache/wal/wal")" -q &
lxsession &
# setxkbmap -model abnt2 -layout br -variant abnt2 &
setxkbmap -model intl -layout us -variant intl &
picom --experimental-backends &
nitrogen --restore &
volumeicon &
