## CS Item Parser

A script to parse items_game.txt of cs.

### Installation

```
git clone https://github.com/ValvojaX/cs_items_parser.git
```

### Usage

```py
from cs_parser import ItemsParser

parser = ItemsParser()
skins = parser.get_skins()
```

### CS Item Parser CLI

Clone the repository and install it using pip:

```bash
git clone https://github.com/ValvojaX/cs_items_parser.git
cd cs_items_parser
pip install .
```

Then you can use the command line interface to create a JSON file with parsed data:

```bash
cs-parser -t all -o output.json
```

### Truncated example item

```json
{
    "Desert Eagle | Urban DDPAT (Factory New)": {
        "item": {
            "codename": "weapon_deagle",
            "name_tag": "#SFUI_WPNHUD_DesertEagle",
            "baseitem": "1",
            "item_type": null,
            "index": "1",
            "tool": {},
            "tags": {},
            "attributes": {},
            "prefab": {
                "codename": "weapon_deagle_prefab",
                "name_tag": "#SFUI_WPNHUD_DesertEagle",
                "attributes": {
                    "magazine model": "weapons\/models\/deagle\/weapon_pist_deagle_mag.vmdl",
                    "heat per shot": "0.300000",
                    ...
                },
                "tags": {},
                "quality": null,
                "rarity": {
                    "codename": "uncommon",
                    "value": "2",
                    "name_tag": "Rarity_Uncommon",
                    "name_tag_weapon": "Rarity_Uncommon_Weapon",
                    "name_tag_character": "Rarity_Uncommon_Character"
                },
                "prefabs": [
                    {
                        "codename": "secondary",
                        "name_tag": null,
                        "attributes": {
                            "stattrak model": "models\/weapons\/stattrack.vmdl",
                            "flinch velocity modifier large": "0.560000",
                            ...
                        },
                        "tags": {},
                        "quality": null,
                        "rarity": null,
                        "prefabs": [
                            ...
                        ]
                    }
                ]
            },
            "quality": {
                "codename": "normal",
                "value": "0",
                "weight": "1",
                "hex_color": "#B2B2B2"
            },
            "rarity": null
        },
        "paintkit": {
            "codename": "hy_ddpat_urb",
            "name_tag": "#PaintKit_hy_ddpat_urb_Tag",
            "wear_default": "0.100000",
            "wear_remap_min": "0.060000",
            "wear_remap_max": "0.800000",
            "index": "17",
            "rarity": {
                "codename": "common",
                "value": "1",
                "name_tag": "Rarity_Common",
                "name_tag_weapon": "Rarity_Common_Weapon",
                "name_tag_character": "Rarity_Common_Character"
            }
        },
        "collection": {
            "codename": "set_overpass",
            "name_tag": "#CSGO_set_overpass",
            "items": [
                "[sp_spray]weapon_m249",
                "[so_stormfront]weapon_mag7",
                ...
            ],
            "crates": [
                {
                    "codename": "crate_esl14_promo_de_overpass",
                    "name_tag": "#CSGO_crate_esl14_promo_de_overpass",
                    "baseitem": null,
                    "item_type": null,
                    "index": "4028",
                    "tool": {},
                    "tags": {
                        "ItemSet": {
                            "tag_value": "set_overpass",
                            "tag_text": "#CSGO_set_overpass",
                            "tag_group": "ItemSet",
                            "tag_group_text": "#SFUI_InvTooltip_SetTag"
                        }
                    },
                    "attributes": {
                        "set supply crate series": {
                            "attribute_class": "supply_crate_series",
                            "value": "28",
                            "codename": "set supply crate series",
                            "hidden": "0"
                        },
                        "tournament event id": {
                            "attribute_class": "tournament_event_id",
                            "value": "4",
                            "codename": "tournament event id",
                            "hidden": "1"
                        }
                    },
                    "prefab": {
                        "codename": "weapon_case_souvenirpkg",
                        "name_tag": null,
                        ...
                    },
                    "quality": null,
                    "rarity": null
                },
                ...
            ]
        },
        "lootlist": {
            "codename": "set_overpass",
            "aliases": [
                "crate_antwerp2022_promo_de_overpass",
                "crate_boston2018_promo_de_overpass",
                ...
            ],
            "items": [
                "[cu_usp_sandpapered]weapon_usp_silencer",
                "[hy_varicamo_blue]weapon_xm1014",
                ...
            ],
            "containers": [
                {
                    "codename": "crate_esl14_promo_de_overpass",
                    "name_tag": "#CSGO_crate_esl14_promo_de_overpass",
                    "baseitem": null,
                    "item_type": null,
                    "index": "4028",
                    "tool": {},
                    "tags": {
                        "ItemSet": {
                            "tag_value": "set_overpass",
                            "tag_text": "#CSGO_set_overpass",
                            "tag_group": "ItemSet",
                            "tag_group_text": "#SFUI_InvTooltip_SetTag"
                        }
                    },
                    "attributes": {
                        "set supply crate series": {
                            "attribute_class": "supply_crate_series",
                            "value": "28",
                            "codename": "set supply crate series",
                            "hidden": "0"
                        },
                        "tournament event id": {
                            "attribute_class": "tournament_event_id",
                            "value": "4",
                            "codename": "tournament event id",
                            "hidden": "1"
                        }
                    },
                    "prefab": {
                        "codename": "weapon_case_souvenirpkg",
                        "name_tag": null,
                        ...
                    },
                    "quality": null,
                    "rarity": null
                },
                ...
            ]
        }
    }
}
```