class DefaultTheme:
    BG_COLOR = (50, 50, 50)
    BG_COLOR_SELECTED = (65, 65, 65)
    BG_SPACER = (75, 75, 75)
    TEXT_COLOR = (255, 255, 255)

class LightTheme:
    BG_COLOR = (220, 220, 220)
    BG_COLOR_SELECTED = (200, 200, 200)
    BG_SPACER = (160, 160, 160)
    TEXT_COLOR = (0, 0, 0)

class SunsetTheme:
    BG_COLOR = (255, 94, 77)
    BG_COLOR_SELECTED = (255, 149, 128)
    BG_SPACER = (204, 85, 68)
    TEXT_COLOR = (255, 255, 255)

class NeonTheme:
    BG_COLOR = (20, 20, 40)
    BG_COLOR_SELECTED = (40, 0, 80)
    BG_SPACER = (70, 0, 130)
    TEXT_COLOR = (0, 255, 200)

class ForestTheme:
    BG_COLOR = (34, 45, 34)
    BG_COLOR_SELECTED = (58, 75, 58)
    BG_SPACER = (80, 100, 80)
    TEXT_COLOR = (200, 255, 200)

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