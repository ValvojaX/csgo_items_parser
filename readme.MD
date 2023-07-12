## CSGO Item Parser

A script to parse items_game.txt of csgo.

### Installation

```
git clone https://github.com/ValvojaX/csgo_items_parser.git
```

### Usage

```py
from csgo_items_parser import ItemsParser

parser = ItemsParser()
skins = parser.get_skins()
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
                    "magazine model": "models/weapons/w_pist_deagle_mag.mdl",
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
                "prefab": {
                    "codename": "secondary",
                    "name_tag": null,
                    ...
                }
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
                "crate_stockh2021_promo_de_overpass",
                "crate_london2018_promo_de_overpass",
                ...
            ],
            "items": [
                "[sp_spray]weapon_m249",
                "[so_stormfront]weapon_mag7",
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