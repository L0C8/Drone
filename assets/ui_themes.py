class DefaultTheme:
    WIDGET_BG = (50, 50, 50)
    WIDGET_BG_SELECTED = (65, 65, 65)
    WIDGET_SPACER = (75, 75, 75)
    TEXT_COLOR = (255, 255, 255)
    GAME_BG = (25, 25, 25)
    GAME_GRID = (90, 90, 90)
    GAME_OUTLINE = (255, 255, 255)

class LightTheme:
    WIDGET_BG = (220, 220, 220)
    WIDGET_BG_SELECTED = (200, 200, 200)
    WIDGET_SPACER = (160, 160, 160)
    TEXT_COLOR = (0, 0, 0)
    GAME_BG = (240, 240, 240)
    GAME_GRID = (200, 200, 200)
    GAME_OUTLINE = (0, 0, 0)

class SunsetTheme:
    WIDGET_BG = (255, 94, 77)
    WIDGET_BG_SELECTED = (255, 149, 128)
    WIDGET_SPACER = (204, 85, 68)
    TEXT_COLOR = (255, 255, 255)
    GAME_BG = (255, 144, 120)
    GAME_GRID = (200, 70, 50)
    GAME_OUTLINE = (255, 255, 255)

class NeonTheme:
    WIDGET_BG = (20, 20, 40)
    WIDGET_BG_SELECTED = (40, 0, 80)
    WIDGET_SPACER = (70, 0, 130)
    TEXT_COLOR = (0, 255, 200)
    GAME_BG = (10, 10, 20)
    GAME_GRID = (100, 0, 150)
    GAME_OUTLINE = (0, 255, 200)

class ForestTheme:
    WIDGET_BG = (34, 45, 34)
    WIDGET_BG_SELECTED = (58, 75, 58)
    WIDGET_SPACER = (80, 100, 80)
    TEXT_COLOR = (200, 255, 200)
    GAME_BG = (20, 30, 20)
    GAME_GRID = (60, 80, 60)
    GAME_OUTLINE = (200, 255, 200)

def get_theme(theme_name="default"):
    themes = {
        "default": DefaultTheme,
        "light": LightTheme,
        "sunset": SunsetTheme,
        "neon": NeonTheme,
        "forest": ForestTheme
    }

    if theme_name in themes:
        return themes[theme_name]

    raise ValueError(f"Theme '{theme_name}' not found.")
