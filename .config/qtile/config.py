import os
import subprocess

from typing import List  # noqa: F401

from libqtile import bar, hook, layout, widget
from libqtile.config import Click, Drag, DropDown, Group, Key, Match, ScratchPad, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = "alacritty"

keys = [
    # Essentials
    Key([mod, "control"], "r",
        lazy.restart(),
        desc="Restart Qtile"),
    Key([mod, "control"], "q",
        lazy.shutdown(),
        desc="Shutdown Qtile"),
    Key([mod], "r",
        lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
    Key([mod], "w",
        lazy.window.kill(),
        desc="Kill focused window"),
    Key([mod], "Tab",
        lazy.next_layout(),
        desc="Toggle between layouts"),

    # Launchers
    Key([mod], "Return",
        lazy.spawn(terminal),
        desc="Launch terminal"),
    Key([mod, "shift"], "Return",
        lazy.spawn("rofi -show drun -show-icons"),
        desc="Spawn Rofi menu"),
    Key([mod, "shift"], "e",
        lazy.spawn("rofi -show emoji -modi-emoji"),
        desc="Spawn Rofi menu"),
    Key([mod], "F12",
        lazy.group['scratchpad'].dropdown_toggle('term'),
        desc="Toggle my scratchpad"),
    Key([mod], "Print",
	lazy.spawn("flameshot gui"),
        desc="Launch Flameshot for taking screenshots"),
	
    # Treetab controls
    Key([mod, "control"], "k",
        lazy.layout.section_up(),
        desc='Move up a section in treetab'),
    Key([mod, "control"], "j",
        lazy.layout.section_down(),
        desc='Move down a section in treetab'),

    # Window controls
    Key([mod], "j",
        lazy.layout.down(),
        desc='Move focus down in current stack pane'),
    Key([mod], "k",
        lazy.layout.up(),
        desc='Move focus up in current stack pane'),
    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        desc='Move windows down in current stack'),
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        desc='Move windows up in current stack'),
    Key([mod], "h",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
        desc='Shrink window (MonadTall), decrease number in master pane (Tile)'),
    Key([mod], "l",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
        desc='Expand window (MonadTall), increase number in master pane (Tile)'),
    Key([mod], "n",
        lazy.layout.normalize(),
        desc='normalize window size ratios'),
    Key([mod], "m",
        lazy.layout.maximize(),
        desc='toggle window between minimum and maximum sizes'),
    Key([mod, "shift"], "f",
        lazy.window.toggle_floating(),
        desc='toggle floating'),
    Key([mod, "shift"], "m",
        lazy.window.toggle_fullscreen(),
        desc='toggle fullscreen'),

    # Stack controls
    Key([mod, "shift"], "space",
        lazy.layout.rotate(),
        lazy.layout.flip(),
        desc='Switch which side main pane occupies (XmonadTall)'),
    Key([mod], "space",
        lazy.layout.next(),
        desc='Switch window focus to other pane(s) of stack'),
    Key([mod, "control"], "Return",
        lazy.layout.toggle_split(),
        desc='Toggle between split and unsplit sides of stack'),

]

group_names = [
    ("1", {'layout': 'monadtall'}),
    ("2", {'layout': 'monadtall'}),
    ("3", {'layout': 'monadtall'}),
    ("4", {'layout': 'monadtall'}),
    ("5", {'layout': 'monadtall'}),
    ("6", {'layout': 'monadtall'}),
    ("7", {'layout': 'monadtall'}),
    ("8", {'layout': 'monadtall'}),
    ("9", {'layout': 'columns'})
]


groups = [Group(name, **kwargs) for name, kwargs in group_names] + [
    ScratchPad("scratchpad", [
        DropDown(
            "term", terminal,
            opacity=0.96,
            width=0.4,
            height=0.4,
            x=0.3,
            y=0.3,
        ),
    ]),
]

for i, (name, kwargs) in enumerate(group_names, 1):
    # Switch to another group
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))
    # Send current window to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))


# palette

bg_color = "#2c2440"
fg_color = "#ffffff"
ac_color = "#12F2DC"

color1 = "#FD5D78"
color2 = "#8B4E80"
color3 = "#3599A9"


layout_defaults = {
    "border_width": 2,
    "margin": 4,
    "border_focus": ac_color,
    "border_normal": bg_color
}


layouts = [
    # Try more layouts by unleashing below layouts.
    layout.MonadTall(ratio=0.65, **layout_defaults),
    # layout.Tile(**layout_defaults),
    # layout.TreeTab(
    #     **layout_defaults
    # ),
    layout.Max(**layout_defaults),
    layout.Floating(),
    # layout.Bsp(**layout_defaults),
    layout.Columns(border_focus_stack=ac_color, **layout_defaults),
    # layout.Stack(num_stacks=2),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.VerticalTile(),
    # layout.Zoomy(**layout_defaults),
]

widget_defaults = dict(
    font='FiraCode Nerd Font',
    fontsize=12,
    padding=0,
    background=bg_color,
    foreground=fg_color,
)

extension_defaults = widget_defaults.copy()

# Glyphs to cpy and paste
#    

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    background=color2
                ),
                widget.GroupBox(
                    font="FiraCode Nerd Font Bold",
                    fontsize=11,
                    margin_y=4,
                    borderwidth=2,
                    padding=4,
                    background=color2,
                    active=fg_color,
                    inactive=bg_color,
                    highlight_color=[color2, color2],
                    highlight_method="line",
                    block_highlight_text_color=fg_color,
                    this_screen_border=ac_color,
                    this_current_screen_border=ac_color,
                    rounded=False,
                    markup=False,
                ),
                widget.TextBox(
                    text="",
                    fontsize=20,
                    padding=0,
                    foreground=color2,
                    background=bg_color
                ),
                widget.Sep(
                    linewidth=0,
                    padding=8
                ),
                widget.Prompt(),
                widget.WindowName(max_chars=140),
                widget.TextBox(
                    text="",
                    fontsize=20,
                    padding=0,
                    foreground=color1,
                    background=bg_color
                ),
                widget.CurrentLayoutIcon(
                    custom_icon_paths=[os.path.expanduser(
                        "~/.config/qtile/icons")],
                    padding=0,
                    scale=0.5,
                    background=color1,
                ),
                widget.CurrentLayout(
                    background=color1,
                ),
                widget.Sep(
                    linewidth=0,
                    padding=8,
                    background=color1
                ),
                widget.TextBox(
                    text="",
                    fontsize=20,
                    padding=0,
                    foreground=color3,
                    background=color1
                ),
                widget.CheckUpdates(
                    no_update_string="No updates",
                    background=color3
                ),
                widget.Sep(
                    linewidth=0,
                    padding=8,
                    background=color3
                ),
                widget.TextBox(
                    text="",
                    fontsize=20,
                    padding=0,
                    foreground=color1,
                    background=color3
                ),
                widget.CPU(
                    background=color1,
                    format='CPU {freq_current}GHz {load_percent}%'
                ),
                widget.Sep(
                    linewidth=0,
                    padding=8,
                    background=color1
                ),
                widget.ThermalSensor(
                    background=color1,
                ),
                widget.Sep(
                    linewidth=0,
                    padding=8,
                    background=color1
                ),
                widget.TextBox(
                    text="",
                    fontsize=20,
                    padding=0,
                    foreground=color3,
                    background=color1
                ),
                widget.Clock(
                    format='%a, %d/%m %H:%M',
                    background=color3,
                ),
                widget.Sep(
                    linewidth=0,
                    padding=8,
                    background=color3
                ),
                widget.TextBox(
                    text="",
                    fontsize=20,
                    padding=0,
                    foreground=bg_color,
                    background=color3
                ),
                widget.Systray(
                    background=bg_color,
                    padding=8
                ),
                widget.Sep(
                    linewidth=0,
                    padding=20,
                    background=bg_color
                )
            ],
            20,
            opacity=0.92,
            margin=[4, 4, 0, 4]
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='pavucontrol'),
], border_focus="#12F2DC", border_normal="#5C5F88")
auto_fullscreen = True
focus_on_window_activation = "smart"


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
