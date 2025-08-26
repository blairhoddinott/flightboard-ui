import httpx
import os

from dotenv import load_dotenv
from nicegui import ui
from PIL import Image, ImageDraw, ImageFont

load_dotenv()
flightboard_api_address = os.getenv("FLIGHTBOARD_API_URL", "http://localhost:8000/sweep")
callsign_font = ImageFont.truetype("LiberationSans-Bold.ttf", 28)
flightstrip_font = ImageFont.truetype("LiberationSans-Regular.ttf", 20)


@ui.refreshable
def get_sweep():
    radar_sweep = httpx.get(flightboard_api_address, timeout=30)
    for plane in radar_sweep.json():
        if plane["origin"] is None:
            plane["origin"] = ""
        if plane["destination"] is None:
            plane["destination"] = ""
        if plane["squawk"] is None:
            plane["squawk"] = ""
        if plane["type"] is None:
            plane["type"] = ""
        if plane["vs_rate"] is None:
            plane["vs_rate"] = ""
        strip = Image.open("assets/empty_strip.jpg")
        draw = ImageDraw.Draw(strip)

        # Column 1: Callsign, Aircraft Type
        draw.text((5, 5), plane["callsign"], fill=(0, 0, 0), font=callsign_font)
        draw.text((5, 35), plane["type"], fill=(0, 0, 0), font=flightstrip_font)
        # Column 2: Squawk, Speed, Altitude
        draw.text((160, 5), plane["squawk"], fill=(0, 0, 0), font=flightstrip_font)
        draw.text((160, 38), plane["speed"], fill=(0, 0, 0), font=flightstrip_font)
        draw.text((160, 70), plane["altitude"], fill=(0, 0, 0), font=flightstrip_font)
        # Column 3: Destination
        draw.text((340, 5), plane["destination"], fill=(0, 0, 0), font=callsign_font)
        # Column 4: Origin, Route (if possible)
        draw.text((230, 5), plane["origin"], fill=(0, 0, 0), font=callsign_font)
        # Column 5: Heading, VS Rate, Emergency
        draw.text((740, 5), plane["heading"], fill=(0, 0, 0), font=flightstrip_font)
        draw.text((740, 38), plane["vs_rate"], fill=(0, 0, 0), font=flightstrip_font)
        if plane["emergency"]:
            draw.text((740, 68), "EMERGENCY", fill=(255, 0, 0), font=callsign_font)

        # ui.separator()
        ui.image(strip).props("fit=scale-down").classes("w-1000 h-100 border-2 border-red-1002")
        # ui.separator()


def main():
    ui.markdown("# Flight Strips")
    ui.button("Radar Sweep", on_click=get_sweep.refresh)
    get_sweep()
    ui.run()

if __name__ in {"__main__", "__mp_main__"}:
    main()
