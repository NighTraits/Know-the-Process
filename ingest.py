import json
import re
from typing import Any
from dataclasses import asdict
from pathlib import Path
from playwright.async_api import Page
from playwright.async_api._generated import Locator
import asyncio
from playwright.async_api import async_playwright
from models import IContent
from datetime import date
from pathlib import Path
from uuid import uuid4


class DataIngest:
    def __init__(self) -> None:
        self._links: list[str] = []
        self._tramites: list[IContent] = []

    async def create(self):
        async with async_playwright() as ctx:
            browser = await ctx.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 720},
            )
            page = await context.new_page()

            await self.get_link(page)

            for link in self._links:
                await self.get_info(page, link)
                await page.wait_for_timeout(2000)

            self.save_as(Path("static/db.json"))

            await browser.close()

    async def get_link(self, page: Page) -> None:
        for i in range(1, 11):
            await page.goto(
                f"https://www.panamadigital.gob.pa/TramiteInformacion?page={i}"
            )

            list_pages: list[Locator] = await page.locator(
                "div.contenedor-tramites li.list-group-item > a"
            ).all()

            for lp in list_pages:
                self._links.append(await lp.evaluate("el => el.href"))

            await page.wait_for_timeout(3000)

    async def get_info(self, page: Page, site: str) -> None:
        await page.goto(site)

        title: str = await page.locator("h4.titulo-encabezado").inner_text()
        title = self.normalize_text(title)

        location: str = await page.locator("div.nombreInst h6").inner_text()
        location = self.normalize_text(location.split(":")[-1])

        desc: str = await page.locator("div.texTramite").inner_text()
        desc = self.normalize_text(desc)

        content: dict[str, list[str]] = {}

        needs: list[Locator] = await page.locator(
            "div#accordionNeeds.accordion > div"
        ).all()

        for need in needs:
            c1: str = self.normalize_text(
                await need.locator("div.card-header button.btn-card").inner_text()
            )

            c2: list[str] = [
                self.normalize_text(txt)
                for txt in await need.locator(
                    "li.listadoRequerimiento"
                ).all_inner_texts()
            ]

            content.update({c1: c2})

        other: list[str] = [
            self.normalize_text(txt)
            for txt in await page.locator("#collapseObservaciones").all_inner_texts()
        ]

        self._tramites.append(
            IContent(
                id=uuid4(),
                title=title,
                description=desc,
                location=location,
                keywords=[],
                content=content,
                extra_content=other,
                source=site,
                updated_at=date.today(),
                created_at=date.today(),
                approved_by="Administrator",
            )
        )

    def normalize_text(self, text: str) -> str:
        text = text.strip()
        text = re.sub(r"\s{2,}", ". ", text)
        text = re.sub(r"\[. ]+|\n+|\.+", ".", text)
        return text

    def save_as(self, path: Path):
        data: list[dict[str, Any]] = [asdict(dt) for dt in self._tramites]
        data = [
            {
                key: str(value) if isinstance(value, Path) else value
                for key, value in data.items()
            }
            for data in data
        ]

        with open(path, "+w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, default=str)


if __name__ == "__main__":
    asyncio.run(DataIngest().create())
