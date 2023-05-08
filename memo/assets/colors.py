# Functions of color converting

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


# This function takes Hue, Saturation, and Brightness as input and outputs the corresponding RGB HEX code.
# Hue is the degrees on the color ring; Saturation and Brightness are percentages.
def hsv_to_hex(hue, saturation, brightness):
    # 0 <= hue <= 360
    # 0 <= saturation, brightness <= 100

    saturation = saturation / 100
    brightness = brightness / 100

    # First we calculate three transitional variables: C, X, m
    C = brightness * saturation
    X = C * (1 - np.abs((hue / 60) % 2 - 1))
    m = brightness - C

    # Then we calculate another three transitional variables: red_apos, green_apos, blue_apos
    if hue < 60:
        red_apos, green_apos, blue_apos = C, X, 0
    elif hue < 120:
        red_apos, green_apos, blue_apos = X, C, 0
    elif hue < 180:
        red_apos, green_apos, blue_apos = 0, C, X
    elif hue < 240:
        red_apos, green_apos, blue_apos = 0, X, C
    elif hue < 300:
        red_apos, green_apos, blue_apos = X, 0, C
    else:
        red_apos, green_apos, blue_apos = C, 0, X

    # Calculate the final red, green, and blue values; round them into integers.
    red = int(np.round((red_apos + m) * 255))
    green = int(np.round((green_apos + m) * 255))
    blue = int(np.round((blue_apos + m) * 255))

    # Turn rgb values into hex
    if red < 16:
        red_hex = "0" + hex(red)[2]
    else:
        red_hex = hex(red)[2:]

    if green < 16:
        green_hex = "0" + hex(green)[2]
    else:
        green_hex = hex(green)[2:]

    if blue < 16:
        blue_hex = "0" + hex(blue)[2]
    else:
        blue_hex = hex(blue)[2:]

    # Making the HEX code
    return "#" + red_hex + green_hex + blue_hex


# This function takes Hue, Saturation, and Lightness as input and outputs the corresponding RGB.
# Hue is the degrees on the color ring; Saturation and Lightness are percentages.
def hsl_to_rgb(hue, saturation, lightness):
    # 0 <= hue <= 360
    # 0 <= saturation, brightness <= 100

    saturation = saturation / 100
    lightness = lightness / 100

    # First we calculate three transitional variables: C, X, m
    C = (1 - np.abs(2 * lightness - 1)) * saturation
    X = C * (1 - np.abs((hue / 60) % 2 - 1))
    m = lightness - C / 2

    # Then we calculate another three transitional variables: red_apos, green_apos, blue_apos
    if hue < 60:
        red_apos, green_apos, blue_apos = C, X, 0
    elif hue < 120:
        red_apos, green_apos, blue_apos = X, C, 0
    elif hue < 180:
        red_apos, green_apos, blue_apos = 0, C, X
    elif hue < 240:
        red_apos, green_apos, blue_apos = 0, X, C
    elif hue < 300:
        red_apos, green_apos, blue_apos = X, 0, C
    else:
        red_apos, green_apos, blue_apos = C, 0, X

    # Calculate the final red, green, and blue values; round them into integers.
    red = int(np.round((red_apos + m) * 255))
    green = int(np.round((green_apos + m) * 255))
    blue = int(np.round((blue_apos + m) * 255))

    return [red, green, blue]


# This function turns the red, green, and blue values and outputs a hex code
def rgb_to_hex(red, green, blue):
    # Turn rgb values into hex
    if red < 16:
        red_hex = "0" + hex(red)[2]
    else:
        red_hex = hex(red)[2:]

    if green < 16:
        green_hex = "0" + hex(green)[2]
    else:
        green_hex = hex(green)[2:]

    if blue < 16:
        blue_hex = "0" + hex(blue)[2]
    else:
        blue_hex = hex(blue)[2:]

    # Making the HEX code
    return "#" + red_hex + green_hex + blue_hex


# This function takes Hue, Saturation, and Lightness as input and outputs the corresponding RGB HEX code.
# Hue is the degrees on the color ring; Saturation and Lightness are percentages.
def hsl_to_hex(hue, saturation, lightness):
    # 0 <= hue <= 360
    # 0 <= saturation, brightness <= 100

    red, green, blue = [i for i in hsl_to_rgb(hue, saturation, lightness)]
    return rgb_to_hex(red, green, blue)


# A function that takes a hex code and returns a list of red, green, and blue values
def hex_to_rgb(rgb_hex):
    # Get rid of the '#'
    rgb_hex = rgb_hex[1:]

    # Get the red, green, and blue values and divide them by 255
    red = int(rgb_hex[0:2], 16)
    green = int(rgb_hex[2:4], 16)
    blue = int(rgb_hex[4:6], 16)

    return [red, green, blue]


# This function takes a string (RGB HEX code) and outputs a list that has (in order) the corresponding Hue, Saturation, and Brightness.
# Units of HSV: degrees, percentage, percentage
def hex_to_hsv(rgb_hex):
    # Get rid of the '#'
    rgb_hex = rgb_hex[1:]

    # Get the red, green, and blue values and divide them by 255
    red = int(rgb_hex[0:2], 16) / 255
    green = int(rgb_hex[2:4], 16) / 255
    blue = int(rgb_hex[4:6], 16) / 255

    # Get three intermediate variables: c_max, c_min, delta
    c_max = max(red, green, blue)
    c_min = min(red, green, blue)
    delta = c_max - c_min

    # Calculate Hue, Saturation, and Brightness values
    if delta == 0:
        hue = 0
    elif c_max == red:
        hue = 60 * (((green - blue) / delta) % 6)
    elif c_max == green:
        hue = 60 * ((blue - red) / delta + 2)
    else:
        hue = 60 * ((red - green) / delta + 4)

    if c_max == 0:
        saturation = 0 * 100
    else:
        saturation = delta / c_max * 100

    brightness = c_max * 100

    return [int(np.round(hue)), int(np.round(saturation)), int(np.round(brightness))]


# This function is the same as above, but outputs HSL
# Units: degrees, percentages, percentages


def hex_to_hsl(rgb_hex):
    # Get rid of the '#'
    rgb_hex = rgb_hex[1:]

    # Get the red, green, and blue values and divide them by 255
    red = int(rgb_hex[0:2], 16) / 255
    green = int(rgb_hex[2:4], 16) / 255
    blue = int(rgb_hex[4:6], 16) / 255

    # Get three intermediate variables: c_max, c_min, delta
    # These are exactly the same as in HSV
    c_max = max(red, green, blue)
    c_min = min(red, green, blue)
    delta = c_max - c_min

    # Calculate Hue, Saturation, and Brightness values
    # Hue here is exactly the same as in HSV
    if delta == 0:
        hue = 0
    elif c_max == red:
        hue = 60 * (((green - blue) / delta) % 6)
    elif c_max == green:
        hue = 60 * ((blue - red) / delta + 2)
    else:
        hue = 60 * ((red - green) / delta + 4)

    lightness = (c_max + c_min) * 100 / 2

    # The saturation here is different from that in HSV
    if delta == 0:
        saturation = 0 * 100
    else:
        saturation = delta * 100 / (1 - np.abs(2 * lightness / 100 - 1))

    return [int(np.round(hue)), int(np.round(saturation)), int(np.round(lightness))]


# setting the colors

# EMPTY DATAFRAME
category = pd.Series(
    ["main", "main", "main", "main", "main", "backup", "backup", "backup"]
)
role = pd.Series(
    ["hero", "primary", "highlight", "green", "water", "backup1", "backup2", "backup3"]
)

palette = pd.DataFrame(
    np.empty((8, 3), dtype=str),
    columns=["regular", "faded", "dimmed"],
    index=[category, role],
)

# FILL IN COLORS
"""
PLEASE INPUT VALUES HERE
"""
palette.regular = [
    "#353795",  # hero, violet
    "#ef8872",  # primary, salmon
    "#fdd310",  # highlight, yellow
    "#7cbfa4",  # green, see green
    "#84cbce",  # water, turquoise
    "#f4a422",  # backup1, orange
    "#5db75a",  # backup2, forest
    "#e54225",  # backup3, red
]


# FADE/DIM FUNCTION
def make_faded(reg_hex, s_fade_ratio, l_fade_ratio):
    this_h, this_s, this_l = [i for i in hex_to_hsl(reg_hex)]
    faded_h = this_h
    faded_s = min(this_s * s_fade_ratio, 100)
    faded_l = min(this_l * l_fade_ratio, 100)
    return hsl_to_hex(faded_h, faded_s, faded_l)


def make_dimmed(reg_hex, s_dim_ratio, l_dim_ratio):
    this_h, this_s, this_l = [i for i in hex_to_hsl(reg_hex)]
    dimmed_h = this_h
    dimmed_s = this_s * s_dim_ratio
    dimmed_l = this_l * l_dim_ratio
    return hsl_to_hex(dimmed_h, dimmed_s, dimmed_l)


# FADING OR DIMMING RATIOS
"""
PLEASE INPUT VALUES HERE
"""
s_fade_ratio = np.array([1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2])
l_fade_ratio = np.array([1.3, 1.25, 1.6, 1.35, 1.35, 1.4, 1.4, 1.4])

s_dim_ratio = np.array([0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8])
l_dim_ratio = np.array([0.8, 0.75, 0.7, 0.7, 0.8, 0.8, 0.8, 0.8])

# CREATE FINAL TABLE
ratio_table = pd.DataFrame(
    {
        "regular": palette["regular"],
        "s_fade_ratio": s_fade_ratio,
        "l_fade_ratio": l_fade_ratio,
        "s_dim_ratio": s_dim_ratio,
        "l_dim_ratio": l_dim_ratio,
    }
)
# Create Faded and Dimmed colors by passing the regular colors along with ratios
palette["faded"] = ratio_table.apply(
    lambda x: make_faded(x["regular"], x["s_fade_ratio"], x["l_fade_ratio"]), axis=1
)
palette["dimmed"] = ratio_table.apply(
    lambda x: make_dimmed(x["regular"], x["s_dim_ratio"], x["l_dim_ratio"]), axis=1
)

# FINAL ADJUSTMENT
palette.loc[("main", "hero"), "faded"] = "#c8b7d9"

# OUTPUT
palette = (
    palette.reset_index()
    .rename({"level_1": "role"}, axis=1)
    .drop(["level_0"], axis=1)
    .set_index(["role"])
)
# Names of individual colors & color series
for column in palette.columns:
    globals()[f"palette_{column}"] = palette[column].values
    for row in palette.index:
        if column == "regular":
            globals()[f"palette_{row}"] = palette.loc[row, column]
        else:
            globals()[f"palette_{row}_{column}"] = palette.loc[row, column]

# Make discrete color ramps

# A function that creates a monochromatic color ramp
# Takes 3 inputs: 1. theme color (string), 2. number of colors in this color ramp (int), 3. the lightness at the end of the sequence
# End lightness should be close to 100 if using white background, and 0 if using black background
# Outputs a list of the color ramp (in RGB HEX)


def create_mono_lightness_ramp(theme_color, num_of_colors, end_lightness=100):
    # Get the HSL of the theme color
    theme_hue, theme_saturation, theme_lightness = (
        hex_to_hsl(theme_color)[0],
        hex_to_hsl(theme_color)[1],
        hex_to_hsl(theme_color)[2],
    )

    # Keep the H and S, make L lighter until 100% (or 0% against dark background)
    lightness_seq = np.linspace(theme_lightness, end_lightness, num_of_colors)

    hex_seq = []

    for i in range(num_of_colors):
        this_lightness = lightness_seq[i]
        this_hex = hsl_to_hex(theme_hue, theme_saturation, this_lightness)
        hex_seq.append(this_hex)

    hex_seq.reverse()

    return hex_seq


# A function that creates a diverging color ramp
# Takes 5 inputs:
# 1. Theme color 1
# 2. Theme color 2
# 3. number of colors based off of theme color 1
# 4. number of colors based off of theme color 2
# 5. end lightness based off of theme color 1
# 6. end lightness based off of theme color 2
# 7. insert a zero color in the middle


def create_div_lightness_ramp(
    theme_color_1,
    theme_color_2,
    num_of_colors_1,
    num_of_colors_2,
    end_lightness_1=100,
    end_lightness_2=100,
    insert_color="",
):
    # Get the HSL of the theme colors
    theme_hue_1, theme_saturation_1, theme_lightness_1 = (
        hex_to_hsl(theme_color_1)[0],
        hex_to_hsl(theme_color_1)[1],
        hex_to_hsl(theme_color_1)[2],
    )
    theme_hue_2, theme_saturation_2, theme_lightness_2 = (
        hex_to_hsl(theme_color_2)[0],
        hex_to_hsl(theme_color_2)[1],
        hex_to_hsl(theme_color_2)[2],
    )

    # If end_lightness_1 == end_lightness_2 == 0 or 100,
    # it means they share a zero color, and the function automatically deletes a duplicate color

    ramp_1 = create_mono_lightness_ramp(theme_color_1, num_of_colors_1, end_lightness_1)
    ramp_2 = create_mono_lightness_ramp(theme_color_2, num_of_colors_2, end_lightness_2)
    ramp_1.reverse()
    ramp = ramp_1 + ramp_2

    if (end_lightness_1 == 100 & end_lightness_2 == 100) | (
        end_lightness_1 == 0 & end_lightness_2 == 0
    ):
        ramp.pop(num_of_colors_1)
    if insert_color != "":
        ramp.insert(num_of_colors_1, insert_color)

    return ramp


# Inputs:
# theme_color: string, hex: the main color that this cmap is based on
# aux_color: hue at the other end of the color map. Takes either a string(hex) or a number(other hex); if not, default to same
# end_saturation (optional): "same", "down", "gray", "as aux" (same as aux color) or integer (pct)
# end_lightness: integer (pct); black if 0, white if 100; or "same" "as aux"
# end_alpha: number(transparency 0-1)
# invert: True, False
def create_mono_cmap(
    theme_color,
    aux_color="same",
    end_saturation="same",
    end_lightness=100,
    end_alpha=1,
    invert=False,
):
    # First, convert this color into HSL
    this_h, this_s, this_l = [
        i for i in hex_to_hsl(theme_color)
    ]  # this_s, this_l: 0-100
    this_a = 1.0  # Starting alpha is 1.

    # Get end HSL
    # Keep hue same
    if aux_color == "same":
        end_h = this_h
        aux_h, aux_s, aux_l = [
            i for i in hex_to_hsl(theme_color)
        ]  # aux_s, aux_l: 0-100
    elif type(aux_color) == str:
        end_h = hex_to_hsl(aux_color)[0]
        aux_h, aux_s, aux_l = [i for i in hex_to_hsl(aux_color)]  # aux_s, aux_l: 0-100
    else:
        end_h = int(aux_color)

    # Saturation (0-100)
    if end_saturation == "same":
        end_s = this_s
    elif end_saturation == "down":
        end_s = this_s / 2
    elif end_saturation == "gray":
        end_s = 0
    elif end_saturation == "as aux":
        end_s = aux_s
    elif end_saturation <= 100 & end_saturation >= 0:
        end_s = end_saturation
    else:
        print("end_saturation input error")

    # Lightness (0-100)
    if end_lightness == "same":
        end_l = this_l
    elif end_lightness == "as aux":
        end_l = aux_l
    elif end_lightness >= 0 & end_lightness <= 100:
        end_l = end_lightness
    else:
        print("end_lightness input error")

    # Alpha
    if end_alpha >= 0 & end_alpha <= 1:
        end_a = end_alpha
    else:
        print("end_alpha input error")

    # Now we'll convert the hsl's into rgb's
    this_r, this_g, this_b = [i for i in hsl_to_rgb(this_h, this_s, this_l)]
    end_r, end_g, end_b = [i for i in hsl_to_rgb(end_h, end_s, end_l)]

    if invert == True:
        # Sway this and end
        temp_r, temp_g, temp_b = this_r, this_g, this_b
        this_r, this_g, this_b = end_r, end_g, end_b
        end_r, end_g, end_b = temp_r, temp_g, temp_b

    # Create color map
    cmap_array = np.ones((256, 4))  # Create a two-dimensional np.array
    cmap_array[:, 0] = np.linspace(this_r / 255, end_r / 255, 256)  # Red
    cmap_array[:, 1] = np.linspace(this_g / 255, end_g / 255, 256)  # Green
    cmap_array[:, 2] = np.linspace(this_b / 255, end_b / 255, 256)  # Blue
    cmap_array[:, 3] = np.linspace(this_a, end_a, 256)  # Alpha

    return ListedColormap(cmap_array)


# Inputs:
# end_color_1, end_color_2: string, two colors at the ends of the color map

# mid_pos: position (number, 0-1) of the change of hue; color_1 transitions into mid_pos, and from mit_pos the color transitions into color_2
# mid_method: "white", "black", "transparent"
# mid_alpha: numeric 0-1


def create_div_cmap(
    end_color_1, end_color_2, mid_pos=0.5, mid_method="white", mid_alpha=1
):
    # Get rgb of end_color_1 and end_color_2
    # N.B. Result needs to be divided by 255
    end_r_1, end_g_1, end_b_1 = [i / 255 for i in hex_to_rgb(end_color_1)]
    end_r_2, end_g_2, end_b_2 = [i / 255 for i in hex_to_rgb(end_color_2)]

    end_alpha_1 = 1
    end_alpha_2 = 1

    # Now calculate the middle color
    # We use TWO mid colors. Although there is only one mid point, we use two mid colors to transtion with their own corresponding theme color
    # When mid_method == "white" or "black" the two mid colors are the same

    if mid_method == "white":
        mid_r_1, mid_g_1, mid_b_1 = [1.0, 1.0, 1.0]
        mid_r_2, mid_g_2, mid_b_2 = [1.0, 1.0, 1.0]
    elif mid_method == "black":
        mid_r_1, mid_g_1, mid_b_1 = [0.0, 0.0, 0.0]
        mid_r_2, mid_g_2, mid_b_2 = [0.0, 0.0, 0.0]
    elif mid_method == "alpha":
        mid_r_1, mid_g_1, mid_b_1 = end_r_1, end_g_1, end_b_1
        mid_r_2, mid_g_2, mid_b_2 = end_r_2, end_g_2, end_b_2
        mid_alpha = 0

    # find the length of two halves
    left_length = int(mid_pos * 255)
    right_length = 256 - left_length

    # Create left half
    left_array = np.ones((left_length, 4))
    left_array[:, 0] = np.linspace(end_r_1, mid_r_1, left_length)  # Red
    left_array[:, 1] = np.linspace(end_g_1, mid_g_1, left_length)  # Green
    left_array[:, 2] = np.linspace(end_b_1, mid_b_1, left_length)  # Blue
    left_array[:, 3] = np.linspace(end_alpha_1, mid_alpha, left_length)  # Alpha

    # Create right half
    right_array = np.ones((right_length, 4))
    right_array[:, 0] = np.linspace(mid_r_2, end_r_2, right_length)  # Red
    right_array[:, 1] = np.linspace(mid_g_2, end_g_2, right_length)  # Green
    right_array[:, 2] = np.linspace(mid_b_2, end_b_2, right_length)  # Blue
    right_array[:, 3] = np.linspace(mid_alpha, end_alpha_2, right_length)  # Alpha

    # Create final
    cmap_array = np.vstack((left_array, right_array))

    return ListedColormap(cmap_array)
