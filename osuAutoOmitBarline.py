import tkinter as tk
from tkinter import filedialog
from typing import TextIO

root = tk.Tk()


def open_file_dialog():
    file_path = filedialog.askopenfilename(title="Select a .osu File", filetypes=[("osu! files", "*.osu")])

    if file_path:
        file_entry_text.set(file_path)
        process_file(file_path)


def open_output_dialog():
    output_path = filedialog.askdirectory(title="Select folder")

    if output_path:
        output_text.set(output_path)
        # print(f"{output_text.get()}/output.txt")


def process_file(file_path):
    # try:
    with open(file_path, 'r') as file:
        curr_map.file_format = file.readline()

        # I am just going to assume the file has a whitespace here as it should.
        file.readline()

        # [General]
        file.readline()

        lines = return_until_needle(file, "[Editor]")
        curr_map.general = MapGeneral(lines)

        lines = return_until_needle(file, "[Metadata]")
        curr_map.editor = MapEditor(lines)

        lines = return_until_needle(file, "[Difficulty]")
        curr_map.metadata = MapMetadata(lines)

        lines = return_until_needle(file, "[Events]")
        curr_map.difficulty = MapDifficulty(lines)

        lines = return_until_needle(file, "[TimingPoints]")
        curr_map.events = MapEvents(lines)

        lines = return_until_needle(file, ["[Colours]", "[HitObjects]"])
        curr_map.timing_points = MapTimingPoints(lines)

        peek = peek_line(file)
        if "Combo1" in peek:
            lines = return_until_needle(file, "[HitObjects]")
            curr_map.colours = MapColours(lines)

        lines = file.readlines()
        curr_map.hit_objects = MapHitObjects(lines)


def open_breakpoints_info():
    breakpoints_info = tk.Tk()
    breakpoints_info_label = tk.Label(breakpoints_info, text="*At least 1 required. Supply some breakpoints to help "
                                                             "the program figure out major offset shifts. You might "
                                                             "need to run the program multiple times to find where the "
                                                             "program messes up.")
    breakpoints_info_format_label = tk.Label(breakpoints_info, text="Format: [time],[bpm]:[time2],[bpm2]:etc")
    breakpoints_info_example_label = tk.Label(breakpoints_info, text="Example: 1885,168:13285,168:218945,160:220429,"
                                                                     "168")
    breakpoints_info_label.pack(anchor='w', padx=20, pady=(20, 5))
    breakpoints_info_format_label.pack(anchor='w', padx=20)
    breakpoints_info_example_label.pack(anchor='w', padx=20, pady=(5, 20))


def return_until_needle(file, needles):
    lines = []

    if not isinstance(needles, list):
        needles = [needles]

    while line := file.readline():
        for needle in needles:
            if needle in line:
                return lines
        lines.append(line)


def peek_line(file: TextIO):
    pos = file.tell()
    line = file.readline()
    file.seek(pos)
    return line


class Map:
    def __init__(self):
        self.file_format = None
        self.general: None | MapGeneral = None
        self.editor: None | MapEditor = None
        self.metadata: None | MapMetadata = None
        self.difficulty: None | MapDifficulty = None
        self.events: None | MapEvents = None
        self.timing_points: None | MapTimingPoints = None
        self.colours: None | MapColours = None
        self.hit_objects: None | MapHitObjects = None

    def __str__(self):
        return (f"{self.file_format}\n{self.general}\n{self.editor}\n{self.metadata}\n{self.difficulty}\n{self.events}"
                f"\n{self.timing_points}\n{self.colours}\n{self.hit_objects}")


def remove_newline(line):
    return line.replace('\n', '')


class MapGeneral:
    def __init__(self, lines):
        self.general = lines
        lines = map(remove_newline, lines)
        for line in lines:
            values = line.split(': ', 1)
            match values[0]:
                case "AudioFilename":
                    self.audio_filename = values[1]
                case "AudioLeadIn":
                    self.audio_lead_in = values[1]
                case "PreviewTime":
                    self.preview_time = values[1]
                case "Countdown":
                    self.countdown = values[1]
                case "SampleSet":
                    self.sample_set = values[1]
                case "StackLeniency":
                    self.stack_leniency = values[1]
                case "Mode":
                    self.mode = values[1]
                case "LetterboxInBreaks":
                    self.letterbox_in_breaks = values[1]
                case "SpecialStyle":
                    self.special_style = values[1]
                case "WidescreenStoryboard":
                    self.widescreen_storyboard = values[1]

    def __str__(self):
        return f"{self.general}"


class MapEditor:
    def __init__(self, lines):
        self.editor = lines
        lines = map(remove_newline, lines)
        for line in lines:
            values = line.split(': ', 1)
            match values[0]:
                case "Bookmarks":
                    self.bookmarks = values[1]
                case "DistanceSpacing":
                    self.distance_spacing = values[1]
                case "BeatDivisor":
                    self.beat_divisor = values[1]
                case "GridSize":
                    self.grid_size = values[1]
                case "TimelineZoom":
                    self.timeline_zoom = values[1]

    def __str__(self):
        return f"{self.editor}"


class MapMetadata:
    def __init__(self, lines):
        self.metadata = lines
        lines = map(remove_newline, lines)
        for line in lines:
            values = line.split(':', 1)
            match values[0]:
                case "Title":
                    self.title = values[1]
                case "TitleUnicode":
                    self.title_unicode = values[1]
                case "Artist":
                    self.artist = values[1]
                case "ArtistUnicode":
                    self.artist_unicode = values[1]
                case "Creator":
                    self.creator = values[1]
                case "Version":
                    self.version = values[1]
                case "Source":
                    self.source = values[1]
                case "Tags":
                    self.tags = values[1]
                case "BeatmapID":
                    self.beatmap_id = values[1]
                case "BeatmapSetID":
                    self.beatmap_set_id = values[1]

    def __str__(self):
        return f"{self.metadata}"


class MapDifficulty:
    def __init__(self, lines):
        self.difficulty = lines
        lines = map(remove_newline, lines)
        for line in lines:
            values = line.split(':', 1)
            match values[0]:
                case "HPDrainRate":
                    self.hp_drain_rate = values[1]
                case "CircleSize":
                    self.circle_size = values[1]
                case "OverallDifficulty":
                    self.overall_difficulty = values[1]
                case "ApproachRate":
                    self.approach_rate = values[1]
                case "SliderMultiplier":
                    self.slider_multiplier = values[1]
                case "SliderTickRate":
                    self.slider_tick_rate = values[1]

    def __str__(self):
        return f"{self.difficulty}"


class MapEvents:
    def __init__(self, lines):
        self.events = lines
        # Honestly m8 I cba this stuff I've never worked with this anyway

    def __str__(self):
        return f"{self.events}"


class TimingPoint:
    def __init__(self, line):
        self.timing_point = line
        values = line.split(',')
        self.time = int(values[0])
        self.value = float(values[1])
        self.meter = int(values[2])
        self.sample_set = int(values[3])
        self.sample_index = int(values[4])
        self.volume = int(values[5])
        # 0 = green
        self.uninherited = int(values[6])
        # 0 = none, 1 = kiai, 8 = omit barline, 9 = kiai + omit
        self.effects = int(values[7])

    def set_barline(self):
        self.effects &= ~8

    def omit_barline(self):
        self.effects |= 8

    def __str__(self):
        return (f"{self.time},{self.value},{self.meter},{self.sample_set},{self.sample_index},{self.volume},"
                f"{self.uninherited},{self.effects}")


def line_to_timing_point(line):
    if len(line) > 1:
        return TimingPoint(line)


def print_list(d):
    for x in d:
        print(x)


class MapTimingPoints:
    def __init__(self, lines):
        self.timing_points = lines
        lines = map(remove_newline, lines)
        self.timing_points_parsed: list[TimingPoint] = (
            list(x for x in map(line_to_timing_point, lines) if x is not None))

    def __str__(self):
        return f"{self.timing_points}"

    def get_inherited(self) -> list[TimingPoint]:
        return list(filter(lambda x: x.uninherited == 0, self.timing_points_parsed))

    def get_uninherited(self) -> list[TimingPoint]:
        return list(filter(lambda x: x.uninherited == 1, self.timing_points_parsed))


class MapColours:
    def __init__(self, lines):
        self.colours = lines
        self.colours_parsed = []
        lines = map(remove_newline, lines)
        for line in lines:
            values = line.split(' : ', 1)
            if len(values) > 1:
                self.colours_parsed.append(values[1])

    def __str__(self):
        return f"{self.colours}"


# ok so I don't even know why I am making classes for everything, like I don't even use it....
# I skipped this one because there's 4 modes with all their own bloody syntax and shit like cmon man what am I doing
# this for??
class MapHitObjects:
    def __init__(self, lines):
        self.hit_objects = lines
        # lines = map(remove_newline, lines)
        # self.timing_points_parsed = map(line_to_timing_point, lines)

    def __str__(self):
        return f"{self.hit_objects}"


class Breakpoint:
    def __init__(self, point):
        self.time = point[0]
        self.bpm = point[1]


def parse_breakpoint(point):
    return Breakpoint(point)


def create_new_bar(time, prev_timing_point):
    effects = prev_timing_point.effects & ~8

    return TimingPoint(f"{time},{prev_timing_point.value},{prev_timing_point.meter},"
                       f"{prev_timing_point.sample_set},{prev_timing_point.sample_index},"
                       f"{prev_timing_point.volume},1,{effects}")


def generate_omits():
    breakpoints = breakpoints_entry_text.get().split(':')
    breakpoints = list(map(lambda w: w.split(','), breakpoints))
    # inherited_timing_points = curr_map.timing_points.get_inherited()
    uninherited_timing_points = curr_map.timing_points.get_uninherited()

    last_bar = uninherited_timing_points[0]
    prev_timing_point = uninherited_timing_points[0]
    new_timing_points: list[TimingPoint] = []
    x = 0
    needs_bar_reset = False
    breakpoint_index = 0

    # operating at a 1/5 accuracy?
    while x < len(uninherited_timing_points):
        timing_point = uninherited_timing_points[x]

        # 1885,168:13285,168
        # 1885,168:13285,168:218945,160:220429,168
        if breakpoint_index < len(breakpoints) - 1:
            if timing_point.time == int(breakpoints[breakpoint_index + 1][0]):
                breakpoint_index += 1

        while True:
            if timing_point.time == int(breakpoints[breakpoint_index][0]):
                timing_point.set_barline()
                new_timing_points.append(timing_point)
                needs_bar_reset = False
                last_bar = timing_point
                break

            expected_bar = [
                round(60000 / float(breakpoints[breakpoint_index][1]) * (last_bar.meter - 0.15)) + last_bar.time,
                round(60000 / float(breakpoints[breakpoint_index][1]) * last_bar.meter) + last_bar.time,
                round(60000 / float(breakpoints[breakpoint_index][1]) * (last_bar.meter + 0.15)) + last_bar.time
            ]

            # we need to omit bar for the current timing point
            if timing_point.time < expected_bar[0]:
                timing_point.omit_barline()
                new_timing_points.append(timing_point)
                needs_bar_reset = True
                break

            # we need a timing point for a new bar because the next timing point is further than the next bar
            elif timing_point.time > expected_bar[2]:
                # there has been a timing point between the previous bar and the expected next bar, so we need a new bar
                if needs_bar_reset:
                    time = prev_timing_point.time
                    increment = prev_timing_point.value * 0.25
                    while True:
                        if expected_bar[0] < time < expected_bar[2]:
                            break
                        time += increment
                        if time > expected_bar[2]:
                            print("not found?")
                            break

                    new_bar = create_new_bar(round(time), prev_timing_point)
                    new_timing_points.append(new_bar)
                    last_bar = new_bar
                    needs_bar_reset = False

                # there has been no timing point between the previous bar and the expected next bar,
                # the current timing point is beyond this
                else:
                    last_bar = create_new_bar(expected_bar[1], prev_timing_point)

                continue

            # the current timing point needs to be a bar
            else:
                timing_point.set_barline()
                new_timing_points.append(timing_point)
                needs_bar_reset = False
                last_bar = timing_point
                break

        prev_timing_point = timing_point
        x += 1

    f = open(f"{output_text.get()}/output.txt", 'w')
    f.writelines(map(lambda q: f"{q.__str__()}\n", new_timing_points))


if __name__ == '__main__':
    root.title('osu! Auto Omit Barlines')
    curr_map = Map()

    open_file_button = tk.Button(root, text='Select', width=10, command=open_file_dialog)
    selected_file_label = tk.Label(root, text="Selected File:")

    file_entry_text = tk.StringVar()
    file_text = tk.Entry(root, width=80, state=tk.DISABLED, textvariable=file_entry_text)

    selected_file_label.grid(row=0, column=0, padx=10, pady=(20, 10))
    file_text.grid(row=0, column=1, padx=10, pady=(20, 10))
    open_file_button.grid(row=0, column=2, padx=10, pady=(20, 10))

    breakpoints_label = tk.Label(root, text="Breakpoints:")
    breakpoints_entry_text = tk.StringVar()
    breakpoints_entry = tk.Entry(root, width=80, textvariable=breakpoints_entry_text)
    breakpoints_info_button = tk.Button(root, text='?', command=open_breakpoints_info, width=2)

    breakpoints_label.grid(row=1, column=0, padx=10, pady=(0, 10))
    breakpoints_entry.grid(row=1, column=1, padx=10, pady=(0, 10))
    breakpoints_info_button.grid(row=1, column=2, padx=10, sticky='W', pady=(0, 10))

    output_label = tk.Label(root, text="Output:")
    output_text = tk.StringVar()
    output = tk.Entry(root, width=80, textvariable=output_text)
    output_folder_button = tk.Button(root, text='Select', width=10, command=open_output_dialog)

    output_label.grid(row=2, column=0, padx=10)
    output.grid(row=2, column=1, padx=10)
    output_folder_button.grid(row=2, column=2, padx=10)

    generate_button = tk.Button(root, text='Generate', width=10, command=generate_omits)
    generate_button.grid(row=3, column=0, columnspan=3, padx=10, pady=20)

    root.mainloop()
