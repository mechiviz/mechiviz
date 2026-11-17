from pathlib import Path

import fastplotlib as fpl
from fastplotlib.ui import ImguiWindow
import imgui_bundle
import pygfx
from imgui_bundle import imgui
from pygfx.utils.text import FontProps, font_manager


IMGUI_FONTS = Path(imgui_bundle.__file__).parent / "assets" / "fonts"
FONT = str(IMGUI_FONTS / "Roboto" / "Roboto-Regular.ttf")
ICONS = str(IMGUI_FONTS / "Font_Awesome_6_Free-Solid-900.otf")
FONT_SIZE = 14

# ==== colors
WHITE = "#FFFFFF"
INK = "#0a0a0a"  # axes, tick labels, titles, text
DIM = "#71717A"  # secondary text
FRAME = "#F4F4F5"  # subplot frame (title strip + toolbar) and imgui window background
GUTTER = "#D4D4D8"  # 1px gaps between subplots
GRID_MAJOR = "#E4E4E7"
GRID_MINOR = "#F4F4F5"
FRAME_HOVER = "#EDEDEF"
WIDGET = "#FFFFFF"  # imgui slider / combo / button / checkbox fill
WIDGET_HOVER = "#FAFAFA"
WIDGET_ACTIVE = "#E4E4E7"
BORDER = "#D4D4D8"
TITLE_BAR = "#7C7C7C"
ACCENT = "#2563EB"
ACCENT_HOVER = "#1D4ED8"
ACCENT_LIGHT = "#DBEAFE"
PALETTE = ["#0F766E", "#B45309", "#4338CA", "#BE185D", "#65A30D", "#475569"]


def rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))


def vec4(hex_color, alpha=1.0):
    return imgui.ImVec4(*rgb(hex_color), alpha)


# ==== plot text font
font_manager.add_font_file(FONT)
font_manager._default_font_props = FontProps("Roboto")

# ==== subplots
fpl.layouts.Subplot.config.init.background_color = [WHITE]
fpl.global_config.update(
    fpl.layouts.Subplot.config.init,
    frame_kwargs=dict(
        plane_color={
            "idle": rgb(FRAME),
            "highlight": rgb(FRAME),
            "action": rgb(ACCENT_LIGHT),
        },
        title_kwargs=dict(face_color=INK, font_size=13),
    ),
)

# ==== axes
fpl.global_config.update(
    fpl.Axes.config.init,
    color=INK,
    line_width=1,
    tick_size=6,
    grid_kwargs=dict(major_color=GRID_MAJOR, minor_color=GRID_MINOR),
)

# ==== graphics
fpl.LineGraphic.config.init.colors = PALETTE[0]
fpl.ScatterGraphic.config.init.colors = PALETTE[0]
fpl.VectorsGraphic.config.init.color = INK
fpl.TextGraphic.config.init.face_color = INK
fpl.TextGraphic.config.init.outline_color = WHITE
fpl.ImageGraphic.config.init.cmap = "viridis"


def style_figure(figure):
    for subplot in figure:
        if subplot.axes.grids:
            subplot.axes.grids.xy.visible = True
            subplot.axes.grids.xy.material.major_thickness = 1
            subplot.axes.grids.xy.material.minor_thickness = 1

        for ruler in (subplot.axes.x, subplot.axes.y, subplot.axes.z):
            ruler.text.material.outline_thickness = 0

        subplot.frame.resize_handle.visible = False

    # gaps between subplot frames, otherwise they're the black clear color
    figure._underlay_scene.add(pygfx.Background.from_color(GUTTER))

    # the fps Stats overlay makes its own imgui context, switch to the figure's
    imgui.set_current_context(figure.imgui_renderer.imgui_context)

    # font, with the icons merged in so the subplot toolbar icons keep working.
    # only one font: pushing a second font crashes wgpu-py's imgui backend (KeyError: 0)
    io = imgui.get_io()
    font = io.fonts.add_font_from_file_ttf(FONT, FONT_SIZE)
    icons_cfg = imgui.ImFontConfig()
    icons_cfg.merge_mode = True
    io.fonts.add_font_from_file_ttf(ICONS, FONT_SIZE, icons_cfg)
    io.font_default = font
    figure._default_imgui_font = font

    style = imgui.get_style()
    imgui.style_colors_light(style)

    style.window_padding = (8, 6)
    style.frame_padding = (6, 4)
    style.item_spacing = (6, 6)
    style.item_inner_spacing = (6, 4)
    style.window_rounding = 0
    style.child_rounding = 4
    style.frame_rounding = 5
    style.popup_rounding = 5
    style.grab_rounding = 4
    style.scrollbar_rounding = 4
    style.tab_rounding = 4
    style.grab_min_size = 12
    style.window_border_size = 1
    style.frame_border_size = 1
    style.popup_border_size = 1

    c = imgui.Col_
    colors = {
        c.text: vec4(INK),
        c.text_disabled: vec4(DIM),
        c.window_bg: vec4(FRAME),
        c.child_bg: vec4(FRAME),
        c.popup_bg: vec4(WHITE),
        c.menu_bar_bg: vec4(FRAME),
        c.border: vec4(BORDER),
        c.border_shadow: vec4(WHITE, 0.0),
        c.frame_bg: vec4(WIDGET),
        c.frame_bg_hovered: vec4(WIDGET_HOVER),
        c.frame_bg_active: vec4(WIDGET_ACTIVE),
        c.title_bg: vec4(FRAME),
        c.title_bg_active: vec4(TITLE_BAR),
        c.title_bg_collapsed: vec4(FRAME),
        c.button: vec4(WIDGET),
        c.button_hovered: vec4(WIDGET_HOVER),
        c.button_active: vec4(WIDGET_ACTIVE),
        c.header: vec4(WIDGET),
        c.header_hovered: vec4(WIDGET_HOVER),
        c.header_active: vec4(WIDGET_ACTIVE),
        c.separator: vec4(BORDER),
        c.separator_hovered: vec4(ACCENT, 0.6),
        c.separator_active: vec4(ACCENT),
        c.slider_grab: vec4(ACCENT),
        c.slider_grab_active: vec4(ACCENT_HOVER),
        c.check_mark: vec4(ACCENT),
        c.text_selected_bg: vec4(ACCENT, 0.25),
        c.nav_cursor: vec4(ACCENT),
        c.resize_grip: vec4(WHITE, 0.0),
        c.resize_grip_hovered: vec4(ACCENT, 0.6),
        c.resize_grip_active: vec4(ACCENT),
        c.scrollbar_bg: vec4(FRAME),
        c.scrollbar_grab: vec4(WIDGET_ACTIVE),
        c.scrollbar_grab_hovered: vec4(DIM),
        c.scrollbar_grab_active: vec4(INK),
        c.tab: vec4(WIDGET),
        c.tab_hovered: vec4(WIDGET_HOVER),
        c.tab_selected: vec4(WHITE),
        c.tab_selected_overline: vec4(ACCENT),
        c.plot_lines: vec4(ACCENT),
        c.plot_histogram: vec4(ACCENT),
    }
    for idx, col in colors.items():
        style.set_color_(idx, col)


ImguiWindow._draw_resize_handle = lambda self: None
_imgui_figure_init = fpl.layouts.ImguiFigure.__init__


def _styled_init(self, *args, **kwargs):
    _imgui_figure_init(self, *args, **kwargs)
    style_figure(self)


fpl.layouts.ImguiFigure.__init__ = _styled_init
