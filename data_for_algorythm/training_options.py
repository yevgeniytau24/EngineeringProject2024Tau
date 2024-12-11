# Mapping numbers to training types and preferences


training_options = {
    1: "running",
    2: "walking",
    3: "yoga",
    4: "gym",
    5: "swimming",
    6: "cycling",
    7: "basketball",
    8: "zumba",
    9: "squash",
    10: "custom"
}
intensity_options = {
    "running": 3,
    "walking": 3,
    "yoga": 3,
    "gym": 4,
    "swimming": 3,
    "cycling": 3,
    "basketball": 2,
    "zumba": 2,
    "squash": 3
}

bpm_preferences = {
    1: "shuffle",
    2: "parabolic-",
    3: "parabolic+",
    4: "increased",
    5: "decreased"
}

training_bpm_ranges_options = {
    "running": [(120, 150), (150, 180), (160, 200)],
    "walking": [(90, 110), (110, 130), (130, 150)],
    "yoga": [(50, 80), (80, 100), (100, 140)],
    "gym": [(100, 120), (120, 160), (110, 140), (140, 180)],
    "swimming": [(120, 140), (140, 170), (160, 190)],
    "cycling": [(120, 140), (140, 170), (160, 200)],
    "basketball": [(120, 150), (150, 180)],
    "zumba": [(120, 140), (140, 170)],
    "squash": [(140, 160), (160, 180), (180, 200)]
}
