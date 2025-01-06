from datetime import datetime

from zavod import Context, helpers as h
from zavod.logic.pep import categorise, OccupancyStatus
from zavod.shed.trans import (
    apply_translit_full_name,
    make_position_translation_prompt,
)

TRANSLIT_OUTPUT = {
    "eng": ("Latin", "English"),
}
POSITION_PROMPT = prompt = make_position_translation_prompt("cnr")


def get_latest_date(dates):
    if dates:
        # Convert string dates to datetime objects
        dates = [datetime.strptime(item["datum"], "%Y-%m-%d") for item in dates]
        latest_date = max(dates)
        return latest_date.strftime("%Y-%m-%d")
    return None


def crawl_person(context: Context, person):
    name = person.pop("imeIPrezime")
    position = person.pop("nazivFunkcije")
    dates = person.pop("izvjestajImovine")
    latest_date = get_latest_date(dates)

    entity = context.make("Person")
    entity.id = context.make_id(name, position)
    entity.add("name", name)
    entity.add("topics", "role.pep")
    for pos in position:
        position = h.make_position(
            context,
            name=pos,
            country="ME",
            # lang="cnr",
        )
        entity.add("position", pos)

        apply_translit_full_name(
            context, position, "slk", pos, TRANSLIT_OUTPUT, POSITION_PROMPT
        )

        categorisation = categorise(context, position, is_pep=True)
        if not categorisation.is_pep:
            return

        occupancy = h.make_occupancy(
            context,
            entity,
            position,
            no_end_implies_current=False,
            categorisation=categorisation,
            status=OccupancyStatus.UNKNOWN,
        )
        occupancy.add("date", latest_date)

        context.emit(position)
        context.emit(occupancy)

    context.emit(entity, target=True)


def crawl(context: Context):
    page = 0
    max_pages = 1200
    while True:
        data_url = f"https://obsidian.antikorupcija.me/api/ask-interni-pretraga/ank-izvjestaj-imovine/pretraga-izvjestaj-imovine-javni?page={page}&size=20"
        doc = context.fetch_json(data_url.format(page=page), cache_days=1)

        if not doc:  # Break if an empty list is returned
            context.log.info(f"Stopped at page {page}")
            break

        for person in doc:
            crawl_person(context, person)
        page += 1

        if page >= max_pages:
            context.log.error(
                f"Emergency exit: Reached the maximum page limit of {max_pages}."
            )
            break
