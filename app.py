from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from playwright.sync_api import sync_playwright

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

URL = (
    "https://www.englandhockey.co.uk/competitions/"
    "2026-2027-4733302-eh-adult-ehl-open---mens-group-"
    "4733802-open---mens-premier-division/table"
)


@app.get("/")
def home():
    return {"message": "Hockey API is running"}


@app.get("/standings")
def get_standings():

    headers = [
        "Position",
        "Team",
        "Played",
        "Won",
        "Drawn",
        "Lost",
        "For",
        "Against",
        "GD",
        "Points",
    ]

    data = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": 1440, "height": 900}
        )

        try:
            page.goto(
                URL,
                wait_until="domcontentloaded",
                timeout=60000,
            )

            table = page.locator(
                ".js-competition-table table"
            )

            table.locator(
                "tbody tr"
            ).first.wait_for(timeout=60000)

            for row in table.locator(
                "tbody tr"
            ).all():

                cells = row.locator(
                    "td"
                ).all_text_contents()

                values = [
                    cell.strip()
                    for cell in cells
                ]

                if len(values) != len(headers):
                    continue

                data.append({
                    "id": int(values[0]),
                    "position": int(values[0]),
                    "team": values[1],
                    "played": int(values[2]),
                    "won": int(values[3]),
                    "drawn": int(values[4]),
                    "lost": int(values[5]),
                    "for": int(values[6]),
                    "against": int(values[7]),
                    "gd": int(values[8]),
                    "points": int(values[9]),
                })

        finally:
            browser.close()

return data
    
