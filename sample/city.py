from dataclasses import dataclass, field
from typing import List, Optional

import marshmallow.validate
import marshmallow_dataclass
from marshmallow_dataclass import NewType


@dataclass
class Geography:
    area: float = field(metadata={"validate": marshmallow.validate.Range(min=0)})
    site: list = field(metadata=dict(description="The city's area", load_only=True))
    center: int = field(default=1, metadata=dict(description="The city's center"))
    urban_areas: str = field(default="anonymous")


@dataclass
class City:
    name: Optional[str]
    contact: NewType("Email", str, field=marshmallow.fields.Email)
    geography: List[Geography] = field(default_factory=list)


CitySchema = marshmallow_dataclass.class_schema(City)

city = CitySchema().load(
    {"name": "Paris", "contact": "helpline.paris@eu.com",
     "geography": [{"area": 25000.00, "site": ["effiel tower", "notre dam"], "center": 2, 'urban_areas': "saint"}]})

print(city)
print(type(city))
city_dict = CitySchema().dump(city)
print(city_dict)
print(type(city_dict))
