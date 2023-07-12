from copy import deepcopy
import requests
import logging
import vdf
import re

from csgo_items_parser.structs import *

class ItemsManager():
    def __init__(self) -> None:
        self.logger = logging.getLogger("ItemsManager")

        self.items_game_url = 'https://raw.githubusercontent.com/SteamDatabase/GameTracking-CSGO/master/csgo/scripts/items/items_game.txt'
        self.items_game_cdn_url = 'https://raw.githubusercontent.com/SteamDatabase/GameTracking-CSGO/master/csgo/scripts/items/items_game_cdn.txt'
        self.csgo_english_url = 'https://raw.githubusercontent.com/SteamDatabase/GameTracking-CSGO/master/csgo/resource/csgo_english.txt'
        self.schema_url = 'https://raw.githubusercontent.com/SteamDatabase/SteamTracking/b5cba7a22ab899d6d423380cff21cec707b7c947/ItemSchema/CounterStrikeGlobalOffensive.json'

        self.items_game:        dict | None = None
        self.items_game_cdn:    list | None = None
        self.tokens:            dict | None = None

        self.attributes:        list[Attribute]   = []
        self.collections:       list[Collection]  = []
        self.colors:            list[Color]       = []
        self.graffiti_tints:    list[GraffitiTint] = []
        self.items:             list[Item]        = []
        self.lootlists:         list[Lootlist]    = []
        self.musicdefs:         list[Musicdef]    = []
        self.paintkits:         list[Paintkit]    = []
        self.prefabs:           list[Prefab]      = []
        self.qualities:         list[Quality]     = []
        self.rarities:          list[Rarity]      = []
        self.stickerkits:       list[Stickerkit]  = []

        self.update_files()

    def update_files(self):
        session = requests.Session()

        items_game_text = session.get(self.items_game_url).text
        items_game = vdf.loads(items_game_text)["items_game"]

        items_english_text = session.get(self.csgo_english_url).text
        items_english = vdf.loads(items_english_text)
        tokens = {k.lower(): v for k, v in items_english["lang"]["Tokens"].items()}

        items_game_cdn_text = session.get(self.items_game_cdn_url).text
        items_game_cdn_text = items_game_cdn_text.split("\n")
        items_game_cdn = [line.split("=")[0] for line in items_game_cdn_text if "=" in line]

        self.items_game = items_game
        self.items_game_cdn = items_game_cdn
        self.tokens = tokens

        self.__swap_keys()
        self.__remove_empty_prefabs()

        self.attributes:        list[Attribute]   = []
        self.collections:       list[Collection]  = []
        self.colors:            list[Color]       = []
        self.graffiti_tints:    list[GraffitiTint] = []
        self.items:             list[Item]        = []
        self.lootlists:         list[Lootlist]    = []
        self.musicdefs:         list[Musicdef]    = []
        self.paintkits:         list[Paintkit]    = []
        self.prefabs:           list[Prefab]      = []
        self.qualities:         list[Quality]     = []
        self.rarities:          list[Rarity]      = []
        self.stickerkits:       list[Stickerkit]  = []

        self.parse()

    # -------------------------------------- HELPERS -------------------------------------- #

    # remove prefabs that do not exist
    def __remove_empty_prefabs(self):
        for item_cdn in self.items_game["items"]:
            item_data = self.items_game["items"][item_cdn]
            if "prefab" not in item_data:
                continue

            valid_prefab_cdns = []
            prefab_cdns = item_data["prefab"].split(" ")
            for prefab_cdn in prefab_cdns:
                if prefab_cdn in self.items_game["prefabs"]:
                    valid_prefab_cdns.append(prefab_cdn)

            item_data["prefab"] = " ".join(valid_prefab_cdns)

    # change keys to be names instead of indexes
    def __swap_keys(self):
        for key in ["items", "sticker_kits", "paint_kits", "music_definitions", "attributes"]:
            temp = {}
            for item_index in self.items_game[key]:
                item_name = self.items_game[key][item_index]["name"]
                temp[item_name] = self.items_game[key][item_index]
                temp[item_name]["index"] = item_index
            self.items_game[key] = temp

    # helper func to get inherited prefabs
    def __get_prefab_tree(self, data: dict):
        tree = []
        if "prefab" not in data:
            return tree

        next_data = data["prefab"]
        if type(next_data) == str:
            tree.append(next_data)
            next_data = self.items_game["prefabs"][next_data]

        return tree + self.__get_prefab_tree(next_data)

    # helper func to get items from a lootlist
    def __get_lootlist_items(self, lootlist_cdn: str):
        lootlist_items = {}
        lootlist_regex = r'\[(.*?)\](.*?)$'
        items_game_cdns = [i.get("name") for i in self.items_game["items"].values() if i.get("name") is not None]
        for key in self.items_game["client_loot_lists"][lootlist_cdn]:
            if key in self.items_game["client_loot_lists"]:
                lootlist_items[key] = self.__get_lootlist_items(key)
            elif re.search(lootlist_regex, key) is not None:
                lootlist_items[key] = self.items_game["client_loot_lists"][lootlist_cdn][key]
            elif key in items_game_cdns: # not all items are format "[item_name]item_type"
                lootlist_items[key] = self.items_game["client_loot_lists"][lootlist_cdn][key]

        return lootlist_items

    # -------------------------------------- PARSERS -------------------------------------- #

    def parse_colors(self):
        self.logger.debug("Parsing colors...")
        for color_cdn in self.items_game["colors"]:
            color_data = self.items_game["colors"][color_cdn]
            color = Color(codename=color_cdn, data=color_data)
            self.colors.append(color)

    def parse_qualities(self):
        self.logger.debug("Parsing qualities")
        for quality_cdn in self.items_game["qualities"]:
            quality_data = self.items_game["qualities"][quality_cdn]
            quality = Quality(quality_cdn, quality_data)
            self.qualities.append(quality)

    def parse_rarities(self):
        self.logger.debug("Parsing rarities...")
        for rarity_cdn in self.items_game["rarities"]:
            rarity_data = self.items_game["rarities"][rarity_cdn]
            rarity = Rarity(codename=rarity_cdn, data=rarity_data)
            self.rarities.append(rarity)

    def parse_graffiti_tints(self):
        self.logger.debug("Parsing graffiti tints...")
        for graffiti_tint_cdn in self.items_game["graffiti_tints"]:
            graffiti_tint_data = self.items_game["graffiti_tints"][graffiti_tint_cdn]
            graffiti_tint = GraffitiTint(codename=graffiti_tint_cdn, data=graffiti_tint_data)
            self.graffiti_tints.append(graffiti_tint)

    def parse_prefabs(self):
        self.logger.debug("Parsing prefabs...")
        for temp_cdn in self.items_game["prefabs"]:
            temp_data = self.items_game["prefabs"][temp_cdn]
            prefab_tree = [temp_cdn] + self.__get_prefab_tree(temp_data)
            for prefab_cdn in reversed(prefab_tree):
                if self.get_prefab(prefab_cdn) is not None:
                    continue

                prefab_data = self.items_game["prefabs"][prefab_cdn]
                prefab = Prefab(codename=prefab_cdn, data=prefab_data)
                prefab.prefab = self.get_prefab(prefab_data.get("prefab"))
                prefab.quality = self.get_quality(prefab_data.get("item_quality"))
                prefab.rarity = self.get_rarity(prefab_data.get("item_rarity"))

                self.prefabs.append(prefab)

    def parse_attributes(self):
        self.logger.debug("Parsing attributes...")
        for attribute_cdn in self.items_game["attributes"]:
            attribute_data = self.items_game["attributes"][attribute_cdn]
            attribute = Attribute(codename=attribute_cdn, data=attribute_data)
            self.attributes.append(attribute)

    def parse_items(self):
        self.logger.debug("Parsing items...")
        for item_cdn in self.items_game["items"]:
            item_data = self.items_game["items"][item_cdn]
            item = Item(codename=item_cdn, data=item_data)
            item.prefab = self.get_prefab(item_data.get("prefab"))
            item.quality = self.get_quality(item_data.get("item_quality"))
            item.rarity = self.get_rarity(item_data.get("item_rarity"))
            if "attributes" in item_data:
                for attribute_name in item_data["attributes"]:
                    # convert type to dict
                    attribute_data = item_data["attributes"][attribute_name]
                    if not isinstance(attribute_data, dict):
                        attribute_data = {attribute_name: attribute_data}

                    # add default attribute data
                    attribute = self.get_attribute(attribute_name)
                    for key in attribute.asdict():
                        if key not in attribute_data:
                            attribute_data[key] = getattr(attribute, key)

                    # add combined attribute information
                    item.attributes[attribute_name] = attribute_data
            if item.name_tag is None:
                item.name_tag = item.prefab.name_tag

            self.items.append(item)

    def parse_stickerkits(self):
        self.logger.debug("Parsing stickerkits...")
        for stickerkit_cdn in self.items_game["sticker_kits"]:
            stickerkit_data = self.items_game["sticker_kits"][stickerkit_cdn]
            stickerkit = Stickerkit(codename=stickerkit_cdn, data=stickerkit_data)
            stickerkit.rarity = self.get_rarity(stickerkit_data.get("item_rarity"))
            self.stickerkits.append(stickerkit)

    def parse_paintkits(self):
        self.logger.debug("Parsing paintkits...")
        default_data = self.items_game["paint_kits"]["default"]
        for paintkit_cdn in self.items_game["paint_kits"]:
            combined = deepcopy(default_data)
            paintkit_data = self.items_game["paint_kits"][paintkit_cdn]
            for key in default_data:
                if key in paintkit_data:
                    combined[key] = paintkit_data[key]

            paintkit = Paintkit(codename=paintkit_cdn.lower(), data=combined)
            paintkit.rarity = self.get_rarity(self.items_game["paint_kits_rarity"].get(paintkit_cdn))
            self.paintkits.append(paintkit)

    def parse_musickits(self):
        self.logger.debug("Parsing musickits...")
        for musickit_cdn in self.items_game["music_definitions"]:
            musickit_data = self.items_game["music_definitions"][musickit_cdn]
            musickit = Musicdef(codename=musickit_cdn, data=musickit_data)
            self.musicdefs.append(musickit)

    def parse_lootlists(self):
        self.logger.debug("Parsing lootlists...")
        # parse client lootlists
        lootlist = deepcopy(self.items_game["client_loot_lists"])
        for lootlist_cdn in lootlist:
            sublists = [0]
            while sublists:
                sublists = []
                for key in lootlist[lootlist_cdn]:
                    if key in self.items_game["client_loot_lists"]:
                        sublists.append(key)

                for sublist_name in sublists:
                    for key in self.items_game["client_loot_lists"][sublist_name]:
                        lootlist[lootlist_cdn][key] = self.items_game["client_loot_lists"][sublist_name][key]

                    del lootlist[lootlist_cdn][sublist_name]

        # filter sublists and collections, create lootlist objects
        new_lootlists: dict[str, Lootlist] = {}
        for lootlist_cdn in lootlist:
            for item_cdn in self.items_game["items"]:
                item_data = self.items_game["items"][item_cdn]

                if lootlist_cdn == item_data.get("name"):
                    _lootlist = Lootlist(codename=lootlist_cdn, data=item_data)
                    new_lootlists[lootlist_cdn] = _lootlist
                    continue

                if lootlist_cdn == item_data.get("loot_list_name"):
                    _lootlist = Lootlist(codename=lootlist_cdn, data=item_data)
                    new_lootlists[lootlist_cdn] = _lootlist
                    continue

                for attribute_name in item_data.get("attributes", []):
                    if attribute_name == "set supply crate series":
                        revolving_index = item_data["attributes"][attribute_name]["value"]
                        if self.items_game["revolving_loot_lists"][revolving_index] == lootlist_cdn:
                            _lootlist = Lootlist(codename=lootlist_cdn, data=item_data)
                            new_lootlists[lootlist_cdn] = _lootlist

        # get aliases
        alias_sets = []
        for item_cdn in self.items_game["items"]:
            item_data = self.items_game["items"][item_cdn]
            alias_set = set()
            if "name" in item_data:
                alias_set.add(item_data["name"])
            if "loot_list_name" in item_data:
                alias_set.add(item_data["loot_list_name"])
            for tag in item_data.get("tags", []):
                if tag in ["ItemSet", "StickerCapsule", "PatchCapsule", "SprayCapsule"]:
                    alias_set.add(item_data["tags"][tag]["tag_value"])
            for attribute in item_data.get("attributes", []):
                if attribute == "set supply crate series":
                    index = item_data["attributes"][attribute]["value"]
                    alias_set.add(self.items_game["revolving_loot_lists"][index])

            if alias_set:
                alias_sets.append(alias_set)

        # add aliases to lootlists
        for lootlist_cdn in new_lootlists:
            for alias_set in alias_sets:
                if lootlist_cdn in alias_set:
                    new_lootlists[lootlist_cdn].aliases.update(alias_set)

                for key in lootlist[lootlist_cdn]:
                    if key in alias_set and key in self.items_game["items"]:
                        prefab = self.get_item(key).prefab
                        if "weapon_case_base" in self.get_prefab_tree(prefab):
                            new_lootlists[lootlist_cdn].aliases.update(alias_set)

        # add revolving lootlists
        existing_lootlist_aliases = [lootlist.aliases for lootlist in new_lootlists.values()]
        for revolving_index in self.items_game["revolving_loot_lists"]:
            revolving_name = self.items_game["revolving_loot_lists"][revolving_index]

            exists = False
            for existing_aliases in existing_lootlist_aliases:
                if revolving_name in existing_aliases:
                    exists = True
                    break

            if not exists:
                _lootlist = Lootlist(codename=revolving_name, data={})
                new_lootlists[revolving_name] = _lootlist

        # get items
        for loostlist_cdn in new_lootlists:
            for alias in new_lootlists[loostlist_cdn].aliases:
                if alias in self.items_game["item_sets"]:
                    new_lootlists[loostlist_cdn].items = self.items_game["item_sets"][alias]["items"]
                elif alias in lootlist:
                    new_lootlists[loostlist_cdn].items = [i for i in lootlist[alias]]

        # get crates
        for lootlist_cdn in new_lootlists:
            for item_cdn in self.items_game["items"]:
                item_data = self.items_game["items"][item_cdn]
                if item_data.get("name") in new_lootlists[lootlist_cdn].aliases or\
                   item_data.get("loot_list_name") in new_lootlists[lootlist_cdn].aliases:

                    # filter coupons, collections, standalone stickers
                    if item_data.get("loot_list_name") in self.items_game["client_loot_lists"]:
                        continue

                    container = self.get_item(item_cdn)
                    if container not in new_lootlists[lootlist_cdn].containers:
                        new_lootlists[lootlist_cdn].containers.append(container)

        self.lootlists = list(new_lootlists.values())

    def parse_collections(self):
        self.logger.debug("Parsing collections...")
        for collection_cdn in self.items_game["item_sets"]:
            collection_data = self.items_game["item_sets"][collection_cdn]
            collection = Collection(codename=collection_cdn, data=collection_data)
            for item_cdn in self.items_game["items"]:
                item_data = self.items_game["items"][item_cdn]
                if "attributes" not in item_data:
                    continue
                if "set supply crate series" not in item_data["attributes"]:
                    continue
                if "tags" not in item_data:
                    continue
                if "ItemSet" not in item_data["tags"]:
                    continue
                if item_data["tags"]["ItemSet"]["tag_value"] == collection_cdn:
                    crate = Item(codename=item_cdn, data=item_data)
                    crate.prefab = self.get_prefab(item_data["prefab"])
                    collection.crates.append(crate)

            self.collections.append(collection)

    # function to create shared objects to save memory
    def parse(self) -> None:
        self.parse_colors()
        self.parse_qualities()
        self.parse_rarities()
        self.parse_graffiti_tints()
        self.parse_prefabs()
        self.parse_attributes()
        self.parse_items()
        self.parse_stickerkits()
        self.parse_paintkits()
        self.parse_musickits()
        self.parse_lootlists()
        self.parse_collections()

    # -------------------------------------- GETTERS -------------------------------------- #

    def get_quality(self, quality_cdn: str) -> Quality | None:
        for quality in self.qualities:
            if quality.codename == quality_cdn:
                return quality

        return None

    def get_color(self, codename:str) -> Color | None:
        for color in self.colors:
            if color.codename == codename:
                return color

        return None

    def get_graffiti_tint(self, codename:str) -> GraffitiTint | None:
        for tint in self.graffiti_tints:
            if tint.codename == codename:
                return tint

        return None

    def get_rarity(self, codename:str) -> Rarity | None:
        for rarity in self.rarities:
            if rarity.codename == codename:
                return rarity

        return None

    def get_prefab(self, codename: str) -> Prefab | None:
        for prefab in self.prefabs:
            if prefab.codename == codename:
                return prefab

        return None

    def get_attribute(self, codename: str) -> Attribute | None:
        for attribute in self.attributes:
            if attribute.codename == codename:
                return attribute

        return None

    def get_item(self, codename: str) -> Item | None:
        for item in self.items:
            if item.codename == codename:
                return item

        return None

    def get_paintkit(self, codename: str) -> Paintkit | None:
        for paintkit in self.paintkits:
            if paintkit.codename == codename:
                return paintkit

        return None

    def get_musicdef(self, codename: str) -> Musicdef | None:
        for musickit in self.musicdefs:
            if musickit.codename == codename:
                return musickit

        return None

    def get_stickerkit(self, codename: str) -> Stickerkit | None:
        for stickerkit in self.stickerkits:
            if stickerkit.codename == codename:
                return stickerkit

        return None

    def get_lootlist(self, codename: str) -> Lootlist | None:
        for lootlist in self.lootlists:
            if lootlist.codename == codename:
                return lootlist

        return None

    def get_collection(self, codename: str) -> Collection | None:
        for collection in self.collections:
            if collection.codename == codename:
                return collection

        return None

    # -------------------------------------- PUBLIC HELPERS -------------------------------------- #

    def get_market_hash_name(self, name_tag: str) -> str | None:
        return self.tokens.get(name_tag.lstrip("#").lower())

    def skin_exists(self, codename:str) -> bool:
        return codename in self.items_game_cdn

    @staticmethod
    def get_prefab_tree(prefab: Prefab) -> list[str]:
        prefab_tree = []
        while prefab is not None:
            prefab_tree.append(prefab.codename)
            prefab = prefab.prefab

        return prefab_tree
