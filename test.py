
unused_faces = "🧛, 🧙, 🦹, 👩, 👮, 🫅🏼, 🕵️, 👨".replace(" ", "").split(",")
from wcwidth import wcswidth
import unicodedata


key_map = list({
	"floor": "⬜",
	"kitchen": "🖥️",
	"dining": "🪑",
	"entrance": "🚪"
}.values())
vals = unused_faces + key_map + ["📺", "🧑‍⚖️", "🤰"]

for e in vals:
	width = wcswidth(e)
	name = unicodedata.name(e[0], 'UNKNOWN')
	visual = f"|{e}|"
	print(f"{visual:<6} wcwidth: {width:<2} {name}")
