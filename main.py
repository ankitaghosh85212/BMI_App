from kivy.uix.label import Label
from kivy.core.text import LabelBase
import math
from kivy.app import App
from kivy.core.text import Label as CoreLabel
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line, Rectangle, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.properties import BooleanProperty, ListProperty,NumericProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.utils import platform
from kivy.core.window import Window
if platform in ('win', 'linux', 'macosx'):
    Window.size = (430, 850)
Window.clearcolor = (0.95, 0.95, 0.98, 1)
# ── Palette ───────────────────────────────────────────────────────────────────
C_PRI    = (0.54, 0.46, 0.82, 1)   # purple accent
C_PRI_LT = (0.62, 0.55, 0.88, 1)   # lighter purple
C_WHITE  = (1.00, 1.00, 1.00, 1)
C_TEXT   = (0.22, 0.22, 0.32, 1)
C_SUB    = (0, 0, 0, 1)
C_BLUE   = (0.28, 0.70, 0.88, 1)   # Underweight
C_GREEN  = (0.41, 0.79, 0.46, 1)   # Normal
C_ORANGE = (0.96, 0.65, 0.13, 1)   # Overweight
C_RED    = (0.91, 0.35, 0.35, 1)   # Obesity
SCREEN_WIDTH = Window.width
SCREEN_HEIGHT = Window.height
# ── Helpers ───────────────────────────────────────────────────────────────────
def sec_lbl(text, halign="left"):
    """Tiny section-header label."""
    l = Label(
        text=text, font_size=sp(11), color=C_SUB,
        size_hint_y=None, height=dp(22), halign=halign,
    )
    l.bind(size=lambda w, v: setattr(w, "text_size", v))
    return l
def purple_btn(text, callback):
    """Full-width pill-shaped purple button."""
    b = Button(
        text=text, size_hint_y=None, height=dp(54),
        font_size=sp(15), bold=True, color=C_WHITE,
        background_color=(0, 0, 0, 0), background_normal="",)
    with b.canvas.before:
        Color(*C_PRI)
        bg = RoundedRectangle(pos=b.pos, size=b.size, radius=[dp(27)])
    b.bind(
        pos=lambda w, v: setattr(bg, "pos", v),
        size=lambda w, v: setattr(bg, "size", v),
        on_press=lambda *_: callback(),
    )
    return b
def card_wrap(child, radius=dp(14), padding=None):
    """White rounded-rect card around a child widget."""
    padding = padding or [0, 0]
    wrap = BoxLayout(padding=padding)
    with wrap.canvas.before:
        Color(*C_WHITE)
        bg = RoundedRectangle(pos=wrap.pos, size=wrap.size, radius=[radius])
    wrap.bind(
        pos=lambda w, v: setattr(bg, "pos", v),
        size=lambda w, v: setattr(bg, "size", v),
    )
    wrap.add_widget(child)
    return wrap
# ── Popup Message ─────────────────────────────────────────────
def show_message(title, message):
    box = BoxLayout(
        orientation="vertical",
        padding=dp(15),
        spacing=dp(10)
    )

    msg = Label(
        text=message,
        font_size=sp(14),
        color=C_TEXT
    )

    btn = Button(
        text="OK",
        size_hint_y=None,
        height=dp(45),
        background_color=(0, 0, 0, 0),
        background_normal=""
    )

    with btn.canvas.before:
        Color(*C_PRI)
        btn_bg = RoundedRectangle(
            pos=btn.pos,
            size=btn.size,
            radius=[dp(20)]
        )

    btn.bind(
        pos=lambda w, v: setattr(btn_bg, "pos", v),
        size=lambda w, v: setattr(btn_bg, "size", v),
    )

    box.add_widget(msg)
    box.add_widget(btn)

    popup = Popup(
        title=title,
        content=box,
        size_hint=(0.8, 0.3),
        auto_dismiss=False
    )

    btn.bind(on_press=popup.dismiss)
    popup.open()
# ── GenderCard ────────────────────────────────────────────────────────────────
class GenderCard(ButtonBehavior, BoxLayout):
    selected = BooleanProperty(False)
    gender = StringProperty("male")
    def __init__(self, **kw):
        super().__init__(**kw)
        self.orientation = "vertical"
        self.padding = [dp(8), dp(10)]
        self.spacing = dp(6)
        self.size_hint_y = None
        self.height = max(dp(100), Window.height * 0.12)
        icon_path = "male.png" if self.gender == "male" else "female.png"
        self._icon_box = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint=(None, None),
            size=(dp(58), dp(58)),
            pos_hint={"center_x": 0.5}
        )
        with self._icon_box.canvas.before:
            self._icon_bg_col = Color(1, 1, 1, 1)
            self._icon_bg = RoundedRectangle(
                pos=self._icon_box.pos,
                size=self._icon_box.size,
                radius=[dp(29)]
            )
        self._icon_box.bind(
            pos=lambda w, v: setattr(self._icon_bg, "pos", v),
            size=lambda w, v: setattr(self._icon_bg, "size", v)
        )
        self._icon = Image(
            source=icon_path,
            size_hint=(None, None),
            size=(dp(34), dp(34))
        )
        self._icon_box.add_widget(self._icon)
        self._name = Label(
            text="Male" if self.gender == "male" else "Female",
            font_size=sp(13),
            color=C_WHITE,
            size_hint_y=None,
            height=dp(20)
        )
        self.add_widget(self._icon_box)
        self.add_widget(self._name)
        with self.canvas.before:
            self._col = Color(*C_PRI)
            self._bg = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(14)]
            )
        self.bind(
            pos=self._upd_bg,
            size=self._upd_bg,
            selected=self._upd_look
        )
        self._upd_look()
    def _upd_bg(self, *_):
        self._bg.pos = self.pos
        self._bg.size = self.size
    def _upd_look(self, *_):
        if self.selected:
            self._col.rgba = C_PRI
            self._name.color = C_WHITE
            self._icon_bg_col.rgba = C_PRI
        else:
            self._col.rgba = C_WHITE
            self._name.color = C_SUB
            self._icon_bg_col.rgba = (1, 1, 1, 1)
# ── StepperCard ───────────────────────────────────────────────────────────────
class StepperCard(BoxLayout):
    value   = NumericProperty(25)
    min_val = NumericProperty(1)
    max_val = NumericProperty(120)
    def __init__(self, **kw):
        super().__init__(**kw)
        self.orientation = "vertical"
        self.padding = [dp(12), dp(10)]
        self.spacing = dp(6)
        with self.canvas.before:
            Color(*C_WHITE)
            self._bg = RoundedRectangle(pos=self.pos, size=self.size,
radius=[dp(14)])
        self.bind(pos=self._upd_bg, size=self._upd_bg)

        self._lbl = Label(
            text=str(int(self.value)), font_size=sp(34),
            bold=True, color=C_TEXT,
        )
        self.bind(value=lambda *_: setattr(self._lbl, "text",
str(int(self.value))))
        self.add_widget(self._lbl)
        row = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=dp(30),
            spacing=dp(14), padding=[dp(10), 0],
        )
        row.add_widget(self._circle_btn("-", self.decrement))
        row.add_widget(self._circle_btn("+", self.increment))
        self.add_widget(row)
    def _upd_bg(self, *_):
        self._bg.pos  = self.pos
        self._bg.size = self.size
    def _circle_btn(self, txt, cb):
        b = Button(
            text=txt, font_size=sp(20), color=C_WHITE,
            background_color=(0, 0, 0, 0), background_normal="",
            size_hint_x=None, width=dp(30),bold = True, 
        )
        with b.canvas.before:
            Color(*C_PRI)
            el = Ellipse(pos=b.pos, size=(dp(30), dp(30)))

        def _upd(w, *_):
            el.pos  = (w.center_x - dp(15), w.center_y - dp(15))
            el.size = (dp(30), dp(30))

        b.bind(pos=_upd, size=_upd)
        b.bind(on_press=lambda *_: cb())
        return b
    def increment(self):
        if self.value < self.max_val:
            self.value += 1
    def decrement(self):
        if self.value > self.min_val:
            self.value -= 1
# ── HorizontalRuler ───────────────────────────────────────────────────────────
class HorizontalRuler(Widget):
    value   = NumericProperty(165)
    min_val = NumericProperty(140)
    max_val = NumericProperty(200)
    PPU = dp(26)   # pixels per unit (cm)
    def __init__(self, **kw):
        super().__init__(**kw)
        self._touch_x = None
        self.bind(pos=self._draw, size=self._draw, value=self._draw)
    def _draw(self, *_):
        self.canvas.clear()
        with self.canvas:
            cx  = self.x + self.width / 2
            mid = self.y + self.height * 0.42
            for v in range(self.min_val, self.max_val + 1):
                px = cx + (v - self.value) * self.PPU
                if px < self.x or px > self.right:
                    continue
                is5  = (v % 5 == 0)
                isel = (v == self.value)
                h    = dp(16) if is5 else dp(9)
                Color(*(C_TEXT if isel else (0.66, 0.66, 0.74, 1)))
                Line(points=[px, mid - h / 2, px, mid + h / 2],
                     width=dp(1.5 if is5 else 1.0))
                if is5:
                    cl = CoreLabel(
                        text=str(v),
                        font_size=int(sp(12 if isel else 10)),
                        bold=isel,
                    )
                    cl.refresh()
                    tex = cl.texture
                    Color(*(C_TEXT if isel else C_SUB))
                    Rectangle(
                        texture=tex,
                        pos=(px - tex.width / 2, mid + h / 2 + dp(3)),
                        size=tex.size,
                    )
            # Centre marker line (purple)
            Color(*C_PRI)
            Line(points=[cx, self.y + dp(5), cx, self.y + self.height - dp(5)],
                 width=dp(2.5))
    # ── Touch ─────────────────────────────────────────────────────────────────
    def on_touch_down(self, t):
        if self.collide_point(*t.pos):
            self._touch_x = t.x
            return True
    def on_touch_move(self, t):
        if self._touch_x is not None:
            delta = -(t.x - self._touch_x) / self.PPU
            self._touch_x = t.x
            nv = int(round(self.value + delta))
            self.value = max(self.min_val, min(self.max_val, nv))
            return True
    def on_touch_up(self, t):
        self._touch_x = None
# ── BMIGauge ──────────────────────────────────────────────────────────────────
class BMIGauge(Widget):
    bmi_value = NumericProperty(18.0)
    _MIN, _MAX = 10.0, 40.0
    _SEGS = [
        (10.0, 18.5, C_BLUE),
        (18.5, 24.9, C_GREEN),
        (24.9, 29.9, C_ORANGE),
        (29.9, 40.0, C_RED),
    ]
    def __init__(self, **kw):
        super().__init__(**kw)
        self.bind(pos=self._draw, size=self._draw, bmi_value=self._draw)
    # Map BMI → angle counterclockwise from east (180° = left, 0° = right)
    def _angle(self, bmi):
        bmi = max(self._MIN, min(self._MAX, bmi))
        # map BMI from 180° → 360°
        return 180 + (
            (bmi - self._MIN)
            / (self._MAX - self._MIN)
        ) * 180
    def category(self):
        b = self.bmi_value
        if b < 18.5: return "Underweight"
        if b < 25.0: return "Normal"
        if b < 30.0: return "Overweight"
        return "Obesity"
    def _draw(self, *_):
        if self.width < 10 or self.height < 10:
            return
        self.canvas.clear()
        # Center position
        cx = self.center_x
        cy = self.y + self.height * 0.1
        # Radius (responsive and centered)
        r = min(self.width * 0.33, self.height * 0.75)
        # Arc thickness
        th = dp(26)
        # Gap between colors
        gap = 2.5
        with self.canvas:
            # ── Background arc ────────────────────────────────────────────────
            Color(0.87, 0.87, 0.91, 1)
            Line(
                ellipse=(
                    cx - r,
                    cy - r,
                    r * 2,
                    r * 2,
                   0,
                    90
                ),
                width=th,
                cap="round"
            )
            # ── Coloured segments ─────────────────────────────────────────────
            for bmi_lo, bmi_hi, col in self._SEGS:
                start_angle = self._angle(bmi_lo) + gap+90
                end_angle = self._angle(bmi_hi) - gap+90
                Color(*col)
                Line(
                    ellipse=(
                        cx - r,
                        cy - r,
                        r * 2,
                        r * 2,
                        start_angle,
                        end_angle,
                    ),
                    width=th,
                    cap="round"
                )               
            # ── Needle ────────────────────────────────────────────────────────
            nr = r - dp(35)
            na  = math.radians(10-self._angle(self.bmi_value))
            nx  = cx + nr * math.cos(na)
            ny  = cy + nr * math.sin(na)
            Color(0, 0, 0, 0.4)
            Line(points=[cx, cy, nx, ny], width=dp(3), cap="round")
            # ── Hub dot ───────────────────────────────────────────────────────
            hr = dp(6)
            Color(*C_TEXT)
            Ellipse(pos=(cx - hr, cy - hr), size=(hr * 2, hr * 2))
            # ── BMI value text ────────────────────────────────────────────────
            text_cy = cy + r * (0.5)
            val_cl = CoreLabel(text=f"{self.bmi_value:.1f}",
                               font_size=int(sp(28)), bold=True)
            val_cl.refresh()
            vt = val_cl.texture
            Color(*C_TEXT)
            Rectangle(texture=vt,
                      pos=(cx - vt.width / 2, text_cy - vt.height / 2),
                      size=vt.size)
            # ── Category text ─────────────────────────────────────────────────
            cat_cl = CoreLabel(text=self.category().upper(),
                               font_size=int(sp(10)))
            cat_cl.refresh()
            ct = cat_cl.texture
            Color(*C_SUB)
            Rectangle(texture=ct,
                      pos=(
    cx - ct.width / 2,
    text_cy - dp(30)
),
                      size=ct.size)
# ── BMILegendRow ──────────────────────────────────────────────────────────────
class BMILegendRow(BoxLayout):
    label      = StringProperty("")
    range_text = StringProperty("")
    color_rgba = ListProperty([1, 0, 0, 1])
    def __init__(self, **kw):
        super().__init__(**kw)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(30)
        self.spacing = dp(8)
        lbl = Label(text=self.label, font_size=sp(13), color=C_TEXT,
halign="left")
        lbl.bind(size=lambda w, v: setattr(w, "text_size", v))
        self.bind(label=lambda *_: setattr(lbl, "text", self.label))
        rng = Label(text=self.range_text, font_size=sp(12),
color=C_SUB, halign="left")
        rng.bind(size=lambda w, v: setattr(w, "text_size", v))
        spc = Widget()
        box = Widget(size_hint_x=None, width=dp(46))
        with box.canvas:
            Color(*self.color_rgba)
            br = RoundedRectangle(pos=box.pos, size=box.size, radius=[dp(8)])
        box.bind(
            pos=lambda w, v: setattr(br, "pos", v),
            size=lambda w, v: setattr(br, "size", v),
        )
        for w in (lbl, rng, spc, box):
            self.add_widget(w)
# ── Helper Popup ──────────────────────────────────────────────────────
def show_popup(title, message):
    popup = Popup(
        title=title,
        content=Label(text=message),
        size_hint=(0.8, 0.3)
    )
    popup.open()
# ── Login Screen ─────────────────────────────────────────────
class LoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.build_ui()
    def build_ui(self):
        root = BoxLayout(
            orientation="vertical",
            padding=[dp(20), Window.height * 0.05],
            spacing=dp(18)
        )
        root.add_widget(Widget(size_hint_y=.15))
        title = Label(
            text="BMI Calculator",
            font_size=sp(30),
            bold=True,
            color=C_PRI,
            size_hint_y=None,
            height=dp(40)
        )
        subtitle = Label(
            text="Welcome Back",
            font_size=sp(18),
            color=C_SUB,
            size_hint_y=None,
            height=dp(30)
        )
        self.username = TextInput(
            hint_text="Username",
            multiline=False,
            size_hint_y=None,
            height=dp(55),
            padding=[dp(15), dp(15)],
            background_normal="",
            background_active=""
        )
        self.password = TextInput(
            hint_text="Password",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=dp(55),
            padding=[dp(15), dp(15)],
            background_normal="",
            background_active=""
        )
        login_btn = purple_btn("Login", self.login)
        register_btn = Button(
            text="Create New Account",
            background_color=(0,0,0,0),
            color=C_PRI
        )
        register_btn.bind(
            on_press=lambda *_:
            setattr(self.manager, "current", "register")
        )
        root.add_widget(title)
        root.add_widget(subtitle)
        root.add_widget(Widget(size_hint_y=.03))
        root.add_widget(self.username)
        root.add_widget(self.password)
        root.add_widget(login_btn)
        root.add_widget(register_btn)
        root.add_widget(Widget())
        self.add_widget(root)
    def login(self):
        username = self.username.text.strip()
        password = self.password.text.strip()
        if username == "":
            show_message("Login Error",
                         "Please enter username")
            return
        if password == "":
            show_message("Login Error",
                         "Please enter password")
            return
        try:
            with open("users.txt", "r") as file:
                users = file.readlines()
                for user in users:
                    saved_user, saved_pass = \
                        user.strip().split(",")
                    if (username == saved_user and
                            password == saved_pass):
                        show_message(
                            "Success",
                            "Login Successful"
                        )
                        self.username.text = ""
                        self.password.text = ""
                        self.manager.current = "input"
                        return
            show_message(
                "Login Failed",
                "Invalid username or password"
            )
        except FileNotFoundError:
            show_message(
                "Error",
                "No registered user found"
            )
# ── Register Screen ─────────────────────────────────────────
class RegisterScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.build_ui()
    def build_ui(self):
        root = BoxLayout(
            orientation="vertical",
            padding=[dp(20), Window.height * 0.05],
            spacing=dp(18)
        )
        root.add_widget(Widget(size_hint_y=.1))
        title = Label(
            text="Create Account",
            font_size=sp(28),
            bold=True,
            color=C_PRI,
            size_hint_y=None,
            height=dp(40)
        )
        self.username = TextInput(
            hint_text="Username",
            multiline=False,
            size_hint_y=None,
            height=dp(55),
            padding=[dp(15), dp(15)],
            background_normal="",
            background_active=""
        )
        self.password = TextInput(
            hint_text="Password",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=dp(55),
            padding=[dp(15), dp(15)],
            background_normal="",
            background_active=""
        )
        self.confirm_password = TextInput(
            hint_text="Confirm Password",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=dp(55),
            padding=[dp(15), dp(15)],
            background_normal="",
            background_active=""
        )
        register_btn = purple_btn(
            "Register",
            self.register
        )
        back_btn = Button(
            text="Already have account? Login",
            background_color=(0,0,0,0),
            color=C_PRI
        )
        back_btn.bind(
            on_press=lambda *_:
            setattr(self.manager, "current", "login")
        )
        root.add_widget(title)
        root.add_widget(self.username)
        root.add_widget(self.password)
        root.add_widget(self.confirm_password)
        root.add_widget(register_btn)
        root.add_widget(back_btn)
        root.add_widget(Widget())
        self.add_widget(root)
    def register(self):
        username = self.username.text.strip()
        password = self.password.text.strip()
        confirm = self.confirm_password.text.strip()
        if username == "":
            show_message(
                "Registration Error",
                "Please enter username"
            )
            return
        if len(password) < 6:
            show_message(
                "Weak Password",
                "Password must be at least 6 characters"
            )
            return
        if password != confirm:
            show_message(
                "Password Error",
                "Passwords do not match"
            )
            return
        try:
            with open("users.txt", "a+") as file:
                file.seek(0)
                users = file.readlines()
                for user in users:
                    saved_user = \
                        user.strip().split(",")[0]
                    if username == saved_user:
                        show_message(
                            "Error",
                            "Username already exists"
                        )
                        return
                file.write(
                    f"{username},{password}\n"
                )
            show_message(
                "Success",
                "Registration Successful"
            )
            # Clear registration fields
            self.username.text = ""
            self.password.text = ""
            self.confirm_password.text = ""
            self.manager.current = "login"
        except Exception as e:
            show_message(
                "Error",
                str(e)
            )
# ── InputScreen ───────────────────────────────────────────────────────────────
class InputScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._build()
    def _build(self):
        root = BoxLayout(
            orientation="vertical",
            padding=[
                dp(18),
                Window.height * 0.03,
                dp(18),
                dp(18)
            ],
            spacing=dp(14),
        )
        # ── GENDER ────────────────────────────────────────────────────────────
        root.add_widget(sec_lbl("GENDER"))
        gender_row = BoxLayout(spacing=dp(12), size_hint_y=None, height=max(dp(90), Window.height * 0.11) )
        self.male_card   = GenderCard(gender="male",   selected=True)
        self.female_card = GenderCard(gender="female", selected=False)
        self.male_card.bind(on_press=lambda *_: self._sel("male"))
        self.female_card.bind(on_press=lambda *_: self._sel("female"))
        gender_row.add_widget(self.male_card)
        gender_row.add_widget(self.female_card)
        root.add_widget(gender_row)
        # ── HEIGHT ────────────────────────────────────────────────────────────
        h_hdr = BoxLayout(size_hint_y=None, height=dp(22))
        h_hdr.add_widget(sec_lbl("HEIGHT"))
        h_hdr.add_widget(sec_lbl("CM", halign="right"))
        root.add_widget(h_hdr)
        self.ruler = HorizontalRuler(value=165, min_val=140, max_val=200)
        ruler_card = BoxLayout(size_hint_y=None, height=max(dp(68), Window.height * 0.09))
        with ruler_card.canvas.before:
            Color(*C_WHITE)
            rc_bg = RoundedRectangle(pos=ruler_card.pos, size=ruler_card.size,
                                      radius=[dp(14)])
        ruler_card.bind(
            pos=lambda w, v: setattr(rc_bg, "pos", v),
            size=lambda w, v: setattr(rc_bg, "size", v),
        )
        ruler_card.add_widget(self.ruler)
        root.add_widget(ruler_card)
        # ── AGE + WEIGHT ──────────────────────────────────────────────────────
        aw = BoxLayout(spacing=dp(12), size_hint_y=None, height=max(dp(110), Window.height * 0.15))
        age_col = BoxLayout(orientation="vertical", spacing=dp(4))
        age_col.add_widget(sec_lbl("AGE"))
        self.age_s = StepperCard(value=25, min_val=1, max_val=120)
        age_col.add_widget(self.age_s)
        wt_col = BoxLayout(orientation="vertical", spacing=dp(4))
        wt_hdr = BoxLayout(size_hint_y=None, height=dp(22))
        wt_hdr.add_widget(sec_lbl("WEIGHT"))
        wt_hdr.add_widget(sec_lbl("KG", halign="right"))
        wt_col.add_widget(wt_hdr)
        self.wt_s = StepperCard(value=56, min_val=20, max_val=300)
        wt_col.add_widget(self.wt_s)
        aw.add_widget(age_col)
        aw.add_widget(wt_col)
        root.add_widget(aw)
        root.add_widget(Widget())   # flexible spacer
        root.add_widget(purple_btn("Calculate BMI >>", self._calc))
        self.add_widget(root)
    def _sel(self, g):
        self.male_card.selected   = (g == "male")
        self.female_card.selected = (g == "female")
    def _calc(self):
        h   = self.ruler.value / 100.0
        w   = self.wt_s.value
        bmi = w / h ** 2
        rs  = self.manager.get_screen("result")
        rs.set_results(bmi)
        self.manager.current = "result"
# ── ResultScreen ──────────────────────────────────────────────────────────────
class ResultScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._build()
    def _build(self):
        root = BoxLayout(orientation="vertical")
        # ── Top bar ───────────────────────────────────────────────────────────
        bar = BoxLayout(
            size_hint_y=None,
            height=max(dp(56), Window.height * 0.07),
            padding=[dp(8), 0],
            spacing=dp(5)
        )
        # Back Button
        back_btn = Button(
            text="‹",
            font_size=sp(30),
            color=C_TEXT,
            background_color=(0, 0, 0, 0),
            background_normal="",
            size_hint_x=None,
            width=dp(40),
        )
        back_btn.bind(
            on_press=lambda *_:
            self.go_back()
        )
        # Title
        title = Label(
            text="BMI Calculator",
            font_size=sp(18),
            bold=True,
            color=C_TEXT
        )
        # Logout Button (Android style)
        logout_btn = Button(
            text="Logout",
            font_size=sp(13),
            bold=True,
            color=C_WHITE,
            size_hint=(None, None),
            size=(dp(90), dp(38)),
            background_color=(0, 0, 0, 0),
            background_normal=""
        )
        with logout_btn.canvas.before:
            Color(0.91, 0.35, 0.35, 1)  # red
            logout_bg = RoundedRectangle(
                pos=logout_btn.pos,
                size=logout_btn.size,
                radius=[dp(18)]
            )
        logout_btn.bind(
            pos=lambda w, v:
            setattr(logout_bg, "pos", v),
            size=lambda w, v:
            setattr(logout_bg, "size", v),
            on_press=lambda *_:
            self.logout()
        )
        bar.add_widget(back_btn)
        bar.add_widget(title)
        bar.add_widget(logout_btn)
        root.add_widget(bar)
        # ── Scrollable body ───────────────────────────────────────────────────
        sv   = ScrollView()
        cont = BoxLayout(
            orientation="vertical", size_hint_y=None,
            padding=[dp(16), dp(6), dp(16), dp(20)], spacing=dp(12),
        )
        cont.bind(minimum_height=cont.setter("height"))
        # YOUR BMI header
        bmi_hdr = BoxLayout(size_hint_y=None, height=dp(26))
        bmi_hdr.add_widget(Label(text="YOUR BMI", font_size=sp(11), color=C_SUB,
                                  halign="left", text_size=(None, None)))
        # bmi_hdr.add_widget(Label(text="", font_size=sp(16), color=C_SUB,
                                #   size_hint_x=None, width=dp(28)))
        cont.add_widget(bmi_hdr)
        # Gauge card
        gauge_card = BoxLayout(size_hint_y=None, height=min(dp(250), Window.height * 0.35),
                               padding=[dp(8), dp(8)])
        with gauge_card.canvas.before:
            Color(*C_WHITE)
            gc_bg = RoundedRectangle(pos=gauge_card.pos, size=gauge_card.size,
                                      radius=[dp(16)])
        gauge_card.bind(
            pos=lambda w, v: setattr(gc_bg, "pos", v),
            size=lambda w, v: setattr(gc_bg, "size", v),
        )
        self.gauge = BMIGauge(bmi_value=18.0)
        gauge_card.add_widget(self.gauge)
        cont.add_widget(gauge_card)
        # DETAILED RESULTS header
        cont.add_widget(Label(
            text="DETAILED RESULTS", font_size=sp(11), color=C_SUB,
            size_hint_y=None, height=dp(26),
            halign="left", text_size=(dp(300), None),
        ))
        # Results card
        rc = BoxLayout(orientation="vertical", size_hint_y=None,
                       padding=[dp(16), dp(14)], spacing=dp(10))
        rc.bind(minimum_height=rc.setter("height"))
        with rc.canvas.before:
            Color(*C_WHITE)
            rc_bg = RoundedRectangle(pos=rc.pos, size=rc.size, radius=[dp(16)])
        rc.bind(
            pos=lambda w, v: setattr(rc_bg, "pos", v),
            size=lambda w, v: setattr(rc_bg, "size", v),
        )
        self.res_lbl = Label(
            text="", markup=True, font_size=sp(13), color=C_TEXT,
            size_hint_y=None, halign="left",
        )
        self.res_lbl.bind(
            texture_size=lambda w, v: setattr(w, "height", v[1] + dp(6)),
            width=lambda w, v: setattr(w, "text_size", (v, None)),
        )
        rc.add_widget(self.res_lbl)
        for lbl_t, rng_t, col in [
            ("Underweight", "Below 18.5",    C_BLUE),
            ("Normal",      "18.5 to 24.9",  C_GREEN),
            ("Overweight",  "24.9 to 29.9",  C_ORANGE),
            ("Obesity",     "30 or greater",  C_RED),
        ]:
            rc.add_widget(BMILegendRow(label=lbl_t, range_text=rng_t,
                                       color_rgba=col))
        cont.add_widget(rc)
        cont.add_widget(Widget(size_hint_y=None, height=dp(6)))
        cont.add_widget(purple_btn("  Edit Information", self.go_back))
        sv.add_widget(cont)
        root.add_widget(sv)
        self.add_widget(root)
    def set_results(self, bmi):
        bmi_r = round(bmi, 1)
        self.gauge.bmi_value = bmi_r
        cat = self.gauge.category()
        self.res_lbl.text = (
            f"Based on the information entered, your body mass index (BMI) is "
            f"[b]{bmi_r:.1f}[/b], indicating your weight is in the "
           f"[b]{cat}[/b] category for adults of your height."
       )
    def go_back(self):
        self.manager.current = "input"
    def logout(self):
    # Get login screen
        login_screen = self.manager.get_screen("login")
        # Clear previous username/password
        login_screen.username.text = ""
        login_screen.password.text = ""
        # Success message
        show_message(
            "Success",
            "Successfully Logged Out"
        )
        # Go back to login page
        self.manager.current = "login"
# ── App ───────────────────────────────────────────────────────────────────────
class BMIApp(App):
    from kivy.core.window import Window
    title = "BMI Calculator"
    def build(self):
        Window.softinput_mode = "below_target"
        sm = ScreenManager()
        # Login/Register
        sm.add_widget(
            LoginScreen(name="login")
        )
        sm.add_widget(
            RegisterScreen(name="register")
        )
        # BMI screens
        sm.add_widget(
            InputScreen(name="input")
        )
        sm.add_widget(
            ResultScreen(name="result")
        )
        sm.current = "login"
        return sm
if __name__ == "__main__":
    BMIApp().run()