import requests
import logging

import vdf
import re

from vdf import VDFDict

from .structs import *

class ItemsManager:
    def __init__(self):
        self.logger = logging.getLogger("ItemsManager")

        # URLs for the items game file and other resources
        self.items_game_url = 'https://raw.githubusercontent.com/SteamDatabase/GameTracking-CS2/master/game/csgo/pak01_dir/scripts/items/items_game.txt'
        self.csgo_english_url = 'https://raw.githubusercontent.com/SteamDatabase/GameTracking-CS2/master/game/csgo/pak01_dir/resource/csgo_english.txt'
        self.pak01_url = 'https://raw.githubusercontent.com/SteamDatabase/GameTracking-CS2/refs/heads/master/game/csgo/pak01_dir.txt'

        # Stored resources
        self.items_game:        VDFDict | None = None           # Contains item data
        self.items_game_cdn:    list | None = None              # Contains item codenames
        self.tokens:            dict | None = None              # Contains translations for items

        # Parsed items
        self.attributes:        list[Attribute]    = []
        self.collections:       list[Collection]   = []
        self.colors:            list[Color]        = []
        self.graffiti_tints:    list[GraffitiTint] = []
        self.items:             list[Item]         = []
        self.lootlists:         list[Lootlist]     = []
        self.musicdefs:         list[Musicdef]     = []
        self.paintkits:         list[Paintkit]     = []
        self.prefabs:           list[Prefab]       = []
        self.qualities:         list[Quality]      = []
        self.rarities:          list[Rarity]       = []
        self.stickerkits:       list[Stickerkit]   = []
        self.keychains:         list[Keychain]     = []


    def update_files(self):
        session = requests.session()

        items_game_text = session.get(self.items_game_url).text
        self.items_game = vdf.loads(items_game_text, mapper=vdf.VDFDict, merge_duplicate_keys=False)["items_game"]

        csgo_english_text = session.get(self.csgo_english_url).text
        items_english = vdf.loads(csgo_english_text)
        self.tokens = {k.lower(): v for k, v in items_english["lang"]["Tokens"].items()}

        pak01_dir_text = session.get(self.pak01_url).text
        pak01_dir_regex = r'(?<=panorama/images/econ/default_generated/)(.*?)(?=_light_png.vtex_c|_medium_png.vtex_c|_heavy_png.vtex_c)'
        self.items_game_cdn = list(set(re.findall(pak01_dir_regex, pak01_dir_text)))

        self.__preprocess()
        self.parse()

    # -------------------------------------- PREPROCESSING -------------------------------------- #

    def __preprocess(self):
        self.__delete_unnecessary_data()
        self.__merge_duplicate_keys_root()
        self.__swap_keys()
        self.__delete_empty_prefabs()

    def __delete_unnecessary_data(self):
        for key in ["campaign_definitions", "quest_schedule", "skirmish_modes", "skirmish_rank_info", "recipes", "pro_event_results", "pro_players", "pro_teams", "items_game_live"]:
            del self.items_game[key]
        self.logger.debug(f"Deleted unnecessary data")

    def __merge_duplicate_keys_root(self):
        # Merge duplicate keys in root level to make things easier
        key_count = len(self.items_game)
        cached_items: dict[str, list[VDFDict]] = {k: self.items_game.get_all_for(k) for k, v in self.items_game.items()}
        for key in self.items_game.keys():
            self.items_game.remove_all_for(key)

        for key, vdf_dict_list in cached_items.items():
            self.items_game[key] = VDFDict()
            for item in vdf_dict_list:
                self.items_game[key].update(item)

        self.logger.debug(f"Merged duplicate keys in root level: {key_count} -> {len(self.items_game)} items")

    def __swap_keys(self):
        # Swap indexes and names
        for key in ["items", "sticker_kits", "paint_kits", "music_definitions", "attributes", "keychain_definitions"]:
            new_entry = VDFDict()
            for index in self.items_game[key]:
                item_name = self.items_game[key][index]["name"]
                new_entry[item_name] = self.items_game[key][index]
                new_entry[item_name]["index"] = index

            del self.items_game[key]
            self.items_game[key] = new_entry

        self.logger.debug(f"Swapped keys with indexes")

    def __delete_empty_prefabs(self):
        # Some items have prefabs that do not exist. Remove them.
        for item_cdn in self.items_game["items"]:
            item_data = self.items_game["items"][item_cdn]
            if "prefab" not in item_data:
                continue

            valid_prefab_cdns = []
            for prefab_cdn in item_data["prefab"].split(" "):
                if prefab_cdn in self.items_game["prefabs"]:
                    valid_prefab_cdns.append(prefab_cdn)

            item_data[(0, "prefab")] = " ".join(valid_prefab_cdns)

        self.logger.debug(f"Removed empty prefabs")

    def __get_prefab_tree(self, data: VDFDict) -> list[str]:
        tree = []
        if "prefab" not in data:
            return tree

        for prefab_name in data["prefab"].split(" "):
            tree.append(prefab_name)
            tree += self.__get_prefab_tree(self.items_game["prefabs"][prefab_name])

        return tree

    def __get_lootlist_items(self, lootlist_cdn: str) -> dict:
        lootlist_items = {}
        lootlist_regex = r'\[(.*?)\](.*?)$'
        item_cdns = [i.get("name") for i in self.items_game["items"].values() if i.get("name") is not None]

        for key in self.items_game["client_loot_lists"][lootlist_cdn]:
            if key in self.items_game["client_loot_lists"]:
                lootlist_items[key] = self.__get_lootlist_items(key)
            elif re.search(lootlist_regex, key) is not None:
                lootlist_items[key] = self.items_game["client_loot_lists"][lootlist_cdn][key]
            elif key in item_cdns: # not all items are format "[item_name]item_type"
                lootlist_items[key] = self.items_game["client_loot_lists"][lootlist_cdn][key]

        return lootlist_items

    # -------------------------------------- PARSING -------------------------------------- #

    def parse(self):
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
        self.parse_keychains()

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
        prefab_lists = [[i] + self.__get_prefab_tree(self.items_game["prefabs"][i]) for i in self.items_game["prefabs"]]
        for prefab_list in prefab_lists:
            for prefab_cdn in prefab_list:
                if self.get_prefab(prefab_cdn) is not None:
                    continue

                prefab_data = self.items_game["prefabs"][prefab_cdn]


                prefab = Prefab(codename=prefab_cdn, data=prefab_data)
                prefab.quality = self.get_quality(prefab_data.get("item_quality"))
                prefab.rarity = self.get_rarity(prefab_data.get("item_rarity"))

                if prefab_data.get("prefab") is not None:
                    prefab.prefabs = [self.get_prefab(i) for i in prefab_data.get("prefab").split(" ")]

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
                    attribute_data = item_data["attributes"][attribute_name]
                    if not isinstance(attribute_data, VDFDict):
                        attribute_data = VDFDict({attribute_name: attribute_data})

                    # add default attribute data
                    attribute = self.get_attribute(attribute_name)
                    for key in attribute.asdict():
                        if key not in attribute_data:
                            attribute_data[key] = getattr(attribute, key)

                    # add combined attribute information
                    item.attributes[attribute_name] = dict(attribute_data)
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
        default_data: VDFDict = self.items_game["paint_kits"]["default"]
        for paintkit_cdn in self.items_game["paint_kits"]:
            combined = VDFDict(default_data.copy())
            paintkit_data = self.items_game["paint_kits"][paintkit_cdn]
            for key in default_data:
                if key in paintkit_data:
                    combined[(0, key)] = paintkit_data[key]

            paintkit = Paintkit(codename=paintkit_cdn.lower(), data=combined)
            paintkit.rarity = self.get_rarity(self.items_game["paint_kits_rarity"].get(paintkit_cdn))
            self.paintkits.append(paintkit)

    def parse_musickits(self):
        self.logger.debug("Parsing musickits...")
        for musickit_cdn in self.items_game["music_definitions"]:
            musickit_data = self.items_game["music_definitions"][musickit_cdn]
            musickit = Musicdef(codename=musickit_cdn, data=musickit_data)
            self.musicdefs.append(musickit)

    def parse_keychains(self):
        self.logger.debug("Parsing keychains...")
        for keychain_cdn in self.items_game["keychain_definitions"]:
            keychain_data = self.items_game["keychain_definitions"][keychain_cdn]
            keychain = Keychain(codename=keychain_cdn, data=keychain_data)
            self.keychains.append(keychain)

    def parse_lootlists(self):
        self.logger.debug("Parsing lootlists...")

        # Replace sublist references with their contents
        client_loot_lists = VDFDict(self.items_game["client_loot_lists"].copy())
        for lootlist_cdn in client_loot_lists:
            lootlist: VDFDict = client_loot_lists[lootlist_cdn]

            sublists: dict[str, VDFDict] = {key: self.items_game["client_loot_lists"][key] for key in lootlist if key in self.items_game["client_loot_lists"]}
            for sublist_key, sublist in sublists.items():
                lootlist.update(sublist)
                del lootlist[sublist_key]

        # Seasonal lootlist
        seasonal_lootlists = {}
        for operation_index in self.items_game["seasonaloperations"]:
            seasonal_operation = self.items_game["seasonaloperations"][operation_index]
            if "operational_point_redeemable" not in seasonal_operation:
                continue

            redeemables = seasonal_operation.get_all_for("operational_point_redeemable")
            for redeemable in redeemables:
                redeemable_lootlist_name = redeemable.get("item_name").lstrip("lootlist:")
                seasonal_lootlists[redeemable_lootlist_name] = redeemable


        # Create lootlist objects
        lootlists: dict[str, Lootlist] = {}
        for item_cdn in self.items_game["items"]:
            item_data = self.items_game["items"][item_cdn]

            item_name = item_data.get("name")
            if item_name is not None and item_name in client_loot_lists:
                lootlists[item_name] = Lootlist(codename=item_name, data=item_data)
                continue

            lootlist_name = item_data.get("loot_list_name")
            if lootlist_name is not None and lootlist_name in client_loot_lists:
                lootlists[lootlist_name] = Lootlist(codename=lootlist_name, data=item_data)
                continue

            for attribute_name in item_data.get("attributes", []):
                if attribute_name == "set supply crate series":
                    revolving_index = item_data["attributes"][attribute_name]["value"]
                    revolving_lootlist_name = self.items_game["revolving_loot_lists"][revolving_index]
                    if revolving_lootlist_name is not None and revolving_lootlist_name in client_loot_lists:
                        lootlists[revolving_lootlist_name] = Lootlist(codename=revolving_lootlist_name, data=item_data)

        for lootlist_cdn in client_loot_lists:
            if lootlist_cdn not in lootlists and lootlist_cdn in seasonal_lootlists:
                lootlists[lootlist_cdn] = Lootlist(codename=lootlist_cdn, data=seasonal_lootlists[lootlist_cdn])

        # Get aliases for lootlists
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

        # Add aliases to lootlists
        for lootlist_cdn in lootlists:
            for alias_set in alias_sets:
                if lootlist_cdn in alias_set:
                    lootlists[lootlist_cdn].aliases.update(alias_set)

                for key in client_loot_lists[lootlist_cdn]:
                    if key in alias_set and key in self.items_game["items"]:
                        prefab = self.get_item(key).prefab
                        if "weapon_case_base" in self.get_prefab_tree(prefab):
                            lootlists[lootlist_cdn].aliases.update(alias_set)

        # add revolving lootlists
        existing_lootlist_aliases = [i.aliases for i in lootlists.values()]
        existing_lootlist_aliases_all = [i for i in existing_lootlist_aliases for i in i]

        for revolving_index in self.items_game["revolving_loot_lists"]:
            revolving_name = self.items_game["revolving_loot_lists"][revolving_index]
            exists = revolving_name in existing_lootlist_aliases_all

            # Skip if we have already added this lootlist
            if exists:
                continue

            lootlists[revolving_name] = Lootlist(codename=revolving_name, data=VDFDict({}))

        # get items
        for loostlist_cdn in lootlists:
            items = set()
            for alias in lootlists[loostlist_cdn].aliases:
                if alias in self.items_game["item_sets"]:
                    items.update(self.items_game["item_sets"][alias]["items"])
                elif alias in client_loot_lists:
                    items.update([i for i in client_loot_lists[alias]])

            lootlists[loostlist_cdn].items = list(items)

        # get crates
        for lootlist_cdn in lootlists:
            for item_cdn in self.items_game["items"]:
                item_data = self.items_game["items"][item_cdn]

                item_name = item_data.get("name")
                item_lootlist_name = item_data.get("loot_list_name")
                if item_name in lootlists[lootlist_cdn].aliases or\
                   item_lootlist_name in lootlists[lootlist_cdn].aliases:

                    # filter coupons, collections, standalone stickers
                    if item_lootlist_name is not None and item_lootlist_name in self.items_game["client_loot_lists"]:
                        continue

                    container = self.get_item(item_cdn)
                    if container not in lootlists[lootlist_cdn].containers:
                        lootlists[lootlist_cdn].containers.append(container)

        self.lootlists = list(sorted(lootlists.values(), key=lambda x: len(x.containers), reverse=True))

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

    def get_keychain(self, codename: str) -> Keychain | None:
        for keychain in self.keychains:
            if keychain.codename == codename:
                return keychain

        return None

    # -------------------------------------- PUBLIC HELPERS -------------------------------------- #

    def get_market_hash_name(self, name_tag: str) -> str | None:
        return self.tokens.get(name_tag.lstrip("#").lower())

    def skin_exists(self, codename:str) -> bool:
        return codename in self.items_game_cdn

    @staticmethod
    def get_prefab_tree(prefab: Prefab | None) -> list[str]:
        prefab_tree = []

        if prefab is None:
            return prefab_tree

        for i in prefab.prefabs:
            prefab_tree.append(i.codename)
            prefab_tree += ItemsManager.get_prefab_tree(i)

        return prefab_tree