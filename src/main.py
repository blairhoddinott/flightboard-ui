import httpx

from nicegui import ui
from PIL import Image, ImageDraw, ImageFont

flightboard_api_address = "http://localhost:8000/sweep"
callsign_font = ImageFont.truetype("LiberationSans-Bold.ttf", 28)
flightstrip_font = ImageFont.truetype("LiberationSans-Regular.ttf", 20)


# @ui.refreshable
def main():
    ui.markdown("# Flight Strips")
    # ui.button("Radar Sweep", on_click=main.refresh)

    # TODO: implement call to flightboard-api to pull the list of strips
    # get list from flightboard_api
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
        strip = Image.open("assets/empty_strip.jpg")
        draw = ImageDraw.Draw(strip)

        # Column 1: Callsign, Aircraft Type
        # Column 2: Squawk, Speed, Altitude
        # Column 3: Destination
        # Column 4: Origin, Route (if possible)
        # Column 5: Heading, VS Rate, Emergency
        # draw.text((5, 5), "CPA829", fill=(0, 0, 0), font=callsign_font)
        draw.text((5, 5), plane["callsign"], fill=(0, 0, 0), font=callsign_font)
        # draw.text((5, 35), "B77W", fill=(0, 0, 0), font=flightstrip_font)
        draw.text((5, 35), plane["type"], fill=(0, 0, 0), font=flightstrip_font)
        # draw.text((160, 5), "4441", fill=(0, 0, 0), font=flightstrip_font)
        draw.text((160, 5), plane["squawk"], fill=(0, 0, 0), font=flightstrip_font)
        # draw.text((160, 38), "250", fill=(0, 0, 0), font=flightstrip_font)
        draw.text((160, 38), plane["speed"], fill=(0, 0, 0), font=flightstrip_font)
        # draw.text((160, 70), "390", fill=(0, 0, 0), font=flightstrip_font)
        draw.text((160, 70), plane["altitude"], fill=(0, 0, 0), font=flightstrip_font)
        # draw.text((230, 5), "CYYZ", fill=(0, 0, 0), font=callsign_font)
        draw.text((230, 5), plane["origin"], fill=(0, 0, 0), font=callsign_font)
        # draw.text((340, 5), "VHHH", fill=(0, 0, 0), font=callsign_font)
        draw.text((340, 5), plane["destination"], fill=(0, 0, 0), font=callsign_font)
        # draw.text((740, 5), "043", fill=(0, 0, 0), font=flightstrip_font)
        draw.text((740, 5), plane["heading"], fill=(0, 0, 0), font=flightstrip_font)
        # draw.text((740, 38), "-1200", fill=(0, 0, 0), font=flightstrip_font)
        draw.text((740, 38), plane["vs_rate"], fill=(0, 0, 0), font=flightstrip_font)
        if plane["emergency"]:
            draw.text((740, 68), "EMERGENCY", fill=(255, 0, 0), font=callsign_font)

        ui.separator()
        ui.image(strip)
        ui.separator()

    ui.run()

if __name__ in {"__main__", "__mp_main__"}:
    main()
