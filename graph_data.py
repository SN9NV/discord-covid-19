import asyncio
from pathlib import Path
from sys import argv

from aiohttp import ClientSession
from matplotlib import pyplot as plt

from country_day_data import filter_countries
from graphs import graph, graph_since_nth_case
from scraper import initialize_data


async def _main():
    outdir = Path(argv[1]) if len(argv) > 1 else Path()

    async with ClientSession() as session:
        data = await initialize_data(session)

    plt.style.use("discord.mplstyle")

    cz_za_countries = filter_countries(data, ["CZ", "ZA"])
    us_za_countries = filter_countries(data, ["US", "ZA"])
    since_0_countries = filter_countries(data, ["ZA", "Italy", "KR", "CZ", "US"])

    cz_za_graph = await graph(cz_za_countries)
    us_za_graph = await graph(us_za_countries)
    since_0_graph = await graph_since_nth_case(since_0_countries, 0)

    with (outdir / "graph_cz_za.png").open("wb") as f:
        f.write(cz_za_graph.getvalue())
    with (outdir / "graph_us_za.png").open("wb") as f:
        f.write(us_za_graph.getvalue())
    with (outdir / "graph_since_0.png").open("wb") as f:
        f.write(since_0_graph.getvalue())


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(_main())
