import requests_mock
from nomenklatura.cache import Cache
from zavod.crawl import crawl_dataset
from zavod.meta import Dataset
from nomenklatura.enrich import get_enricher, enrich, match
from nomenklatura.enrich.common import Enricher
from nomenklatura.entity import CompositeEntity
from nomenklatura.judgement import Judgement
from nomenklatura.resolver import Resolver

PATH = "zavod.runner.local_enricher:LocalEnricher"
dataset = Dataset.make(
    {
        "name": "nominatim",
        "title": "Nomimatim",
        "config": {"dataset": "testdataset1", "threshold": 0.7},
    }
)


def load_enricher():
    enricher_cls = get_enricher(PATH)
    assert issubclass(enricher_cls, Enricher)
    cache = Cache.make_default(dataset)
    return enricher_cls(dataset, cache, dataset.config)


def make_entity(dataset):
    data = {
        "schema": "LegalEntity",
        "id": "xxx",
        "properties": {"name": ["Umbrella Corp."]},
    }
    ent = CompositeEntity.from_data(dataset, data)
    return ent


def test_match(testdataset1: Dataset):
    """"""
    crawl_dataset(testdataset1)
    enricher = load_enricher()
    entity = make_entity(testdataset1)
    results = list(enricher.match(entity))
    assert len(results) == 1, results
    assert str(results[0].id) == "osv-umbrella-corp", results[0]

    adjacent = list(enricher.expand(entity, results[0]))
    assert len(adjacent) == 2, adjacent
    adjacent.remove(results[0])
    assert adjacent[0].schema.name == "Ownership"
    assert adjacent[0].get("owner") == ["osv-oswell-spencer"]
    assert adjacent[0].get("asset") == ["osv-umbrella-corp"]
