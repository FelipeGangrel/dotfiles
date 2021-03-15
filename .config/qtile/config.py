import os
import subprocess

from typing import List  # noqa: F401

from libqtile import bar, hook, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
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
        lazy.spawn("rofi -show run"),
        desc="Spawn Rofi menu"),

    # Treetab controls
    Key([mod, "control"], "k",
        lazy.layout.section_up(),
        desc='Move up a section in treetab'),
    Key([mod, "control"], "j",
        lazy.layout.section_down(),
        desc='Move down a section in treetab'),

    # Window controls
    Key([mod], "k",
        lazy.layout.down(),
        desc='Move focus down in current stack pane'),
    Key([mod], "j",
        lazy.layout.up(),
        desc='Move focus up in current stack pane'),
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_down(),
        desc='Move windows down in current stack'),
    Key([mod, "shift"], "j",
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
    ("9", {'layout': 'floating'})
]


groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    # Switch to another group
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))
    # Send current window to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))


main_palette = dict(
    bar_background="#0B0C0E",
    dark1="#383c4a",
    dark2="#4b5162",
    light1="#E6E9F3",
    light2="#F7F8FB",
    red1="#bf616a",
    red2="#bf616a",
    blue1="#3A6E97",
    blue2="#417BA8",
)


def init_layout_theme():
    colors = main_palette.copy()
    return dict(
        border_width=2,
        margin=8,
        border_focus=colors.get('red2'),
        border_normal=colors.get('dark2')
    )


layout_defaults = init_layout_theme()


layouts = [
    # Try more layouts by unleashing below layouts.
    layout.MonadTall(ratio=0.65, **layout_defaults),
    layout.TreeTab(
        sections=['Code', 'Other'],
        active_bg=main_palette.get('dark1'),
        bg_color=main_palette.get('bar_background'),
        ** layout_defaults
    ),
    layout.Max(**layout_defaults),
    layout.Floating(),
    # layout.Bsp(**theme_defaults),
    # layout.Columns(border_focus_stack='#d75f5f'),
    # layout.Stack(num_stacks=2),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Fira Code Regular',
    fontsize=12,
    padding=8,
    background=main_palette.get('bar_background'),
    foreground=main_palette.get('light1')
)

extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    font="Fira Code Bold",
                    fontsize=12,
                    borderwidth=0,
                    padding=8,
                    active=main_palette.get('light1'),
                    inactive=main_palette.get('dark2'),
                    rounded=False,
                    highlight_method="line",
                    highlight_color=[main_palette.get(
                        'dark1'), main_palette.get('dark1')],
                ),
                widget.Prompt(),
                widget.WindowName(max_chars=140),
                widget.CurrentLayoutIcon(
                    custom_icon_paths=[os.path.expanduser(
                        "~/.config/qtile/icons")],
                    padding=0,
                    scale=0.5,
                    background=main_palette.get('dark1'),
                ),
                widget.CurrentLayout(background=main_palette.get('dark2')),
                widget.Clock(format='%a, %d/%m %H:%M'),
                widget.Volume(),
                widget.Systray(),
                widget.QuickExit(),
            ],
            24,
            opacity=0.86,
            margin=[0, 0, 0, 0]
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
follow_mouse_focus = True
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
], border_focus=main_palette.get('blue1'), border_normal=main_palette.get('dark2'))
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
