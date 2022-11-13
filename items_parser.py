from threading import Thread
from time import sleep
import re

from items_manager import ItemsManager
from structs import *

class ItemsParser(Thread):
    def __init__(self, debug: bool = False) -> None:
        super().__init__()
        self.debug = debug
        self.items_manager = ItemsManager(debug=debug)
        self.manual_changes()

        self.souvenir_collections = {
            "set_vertigo":          "The Vertigo Collection",
            "set_inferno":          "The Inferno Collection",
            "set_nuke":             "The Nuke Collection",
            "set_dust_2":           "The Dust 2 Collection",
            "set_train":            "The Train Collection",
            "set_mirage":           "The Mirage Collection",
            "set_italy":            "The Italy Collection",
            "set_lake":             "The Lake Collection",
            "set_safehouse":        "The Safehouse Collection",
            "set_overpass":         "The Overpass Collection",
            "set_cobblestone":      "The Cobblestone Collection",
            "set_cache":            "The Cache Collection",
            "set_nuke_2":           "The 2018 Nuke Collection",
            "set_inferno_2":        "The 2018 Inferno Collection",
            "set_blacksite":        "The Blacksite Collection",
            "set_dust_2_2021":      "The 2021 Dust 2 Collection",
            "set_mirage_2021":      "The 2021 Mirage Collection",
            "set_op10_ancient":     "The Ancient Collection",
            "set_vertigo_2021":     "The 2021 Vertigo Collection"
        }
        self.blank_collections = {
            "set_dust":                 "The Dust Collection",
            "set_aztec":                "The Aztec Collection",
            "set_militia":              "The Militia Collection",
            "set_office":               "The Office Collection",
            "set_assault":              "The Assault Collection",
            "set_bravo_ii":             "The Alpha Collection",
            "set_bank":                 "The Bank Collection",
            "set_baggage":              "The Baggage Collection",
            "set_gods_and_monsters":    "The Gods and Monsters Collection",
            "set_chopshop":             "The Chop Shop Collection",
            "set_kimono":               "The Rising Sun Collection",
            "set_stmarc":               "The St. Marc Collection",
            "set_canals":               "The Canals Collection",
            "set_norse":                "The Norse Collection",
            "set_op10_ct":              "The Control Collection",
            "set_op10_t":               "The Havoc Collection",
            "set_train_2021":           "The 2021 Train Collection"
        }
        self.nonexisting_containers = {
            "crate_sticker_pack_broken_fang":           "Broken Fang Sticker Collection",
            "crate_patch_pack02":                       "Metal Skill Group Patch Collection",
            "crate_patch_pack03":                       "Operation Riptide Patch Collection",
            "crate_sticker_pack_op_riptide_capsule":    "Operation Riptide Sticker Collection",
            "crate_sticker_pack_recoil":                "Recoil Sticker Collection",
            "crate_sticker_pack_riptide_surfshop":      "Riptide Surf Shop Sticker Collection",
            "crate_sticker_pack_shattered_web":         "Shattered Web Sticker Collection",
        }
        self.tinted_graffities_limited = {
            "spray_std_heart": ["Bazooka Pink", "Blood Red", "Brick Red", "Desert Amber", "Dust Brown", "Monster Purple", "Princess Pink", "Tiger Orange", "Tracer Yellow", "War Pig Pink"],
            "spray_std2_lightbulb": ["Shark White", "Tracer Yellow"],
            "spray_std_piggles": ["Bazooka Pink", "Blood Red", "Brick Red", "Desert Amber", "Dust Brown", "Monster Purple", "Princess Pink", "Tiger Orange", "Tracer Yellow", "War Pig Pink"],
            "spray_std_hl_smiley": ["Battle Green", "Bazooka Pink", "Blood Red", "Brick Red", "Cash Green", "Desert Amber", "Dust Brown", "Frog Green", "Jungle Green", "Princess Pink", "Tiger Orange", "Tracer Yellow", "War Pig Pink"],
            "spray_std_moly": ["Bazooka Pink", "Blood Red", "Brick Red", "Desert Amber", "Dust Brown", "Monster Purple", "Princess Pink", "Tiger Orange", "Tracer Yellow", "War Pig Pink"],
            "spray_std_necklace_dollar": ["Battle Green", "Blood Red", "Cash Green", "Desert Amber", "Dust Brown", "Frog Green", "Jungle Green", "Monarch Blue", "Monster Purple", "Shark White", "Tiger Orange", "Tracer Yellow", "War Pig Pink", "Wire Blue"],
            "spray_std_salty": ["Shark White"],
            "spray_std_emo_happy": ["Battle Green", "Bazooka Pink", "Blood Red", "Brick Red", "Cash Green", "Desert Amber", "Dust Brown", "Frog Green", "Jungle Green", "Princess Pink", "Tiger Orange", "Tracer Yellow", "War Pig Pink"],
            "spray_std_dollar": ["Battle Green", "Cash Green", "Frog Green", "Jungle Green"]
        }

    def __debug_print(self, data):
        if self.debug: print(f"[{self.__class__.__name__}] {data}")

    # manual changes to items data done before parsing
    def manual_changes(self):
        pass

    def update_files(self):
        self.items_manager.update_files()
        self.manual_changes()

    def run(self):
        while True:
            self.__debug_print("Updating files...")
            self.items_manager.update_files()
            sleep(60 * 60 * 6)
            break

    # -------------------------------------- PUBLIC HELPERS -------------------------------------- #

    def get_lootlist_by_item_codename(self, codename: str) -> Lootlist | None:
        for lootlist in self.items_manager.lootlists:
            if codename in lootlist.items:
                return lootlist

        return None

    def get_collection_by_item_codename(self, codename: str) -> Collection | None:
        for collection in self.items_manager.collections:
            if codename in collection.items:
                return collection

    # -------------------------------------- GETTERS -------------------------------------- #

    def get_skins(self):
        def has_stattrak(item: Item, paintkit: Paintkit) -> bool:
            prefab_tree = self.items_manager.get_prefab_tree(item.prefab)
            if "statted_item_base" not in prefab_tree:
                return False

            for collection in self.items_manager.collections:
                if f"[{paintkit.codename}]{item.codename}" in collection.items:
                    if collection.codename in self.blank_collections:
                        return False

            return True

        def has_souvenir(item: Item, paintkit: Paintkit, lootlist: Lootlist | None) -> bool:
            if lootlist is not None:
                for lootlist in self.items_manager.lootlists:
                    if f"[{paintkit.codename}]{item.codename}" in lootlist.items:
                        for container in lootlist.containers:
                            container_prefab_tree = self.items_manager.get_prefab_tree(container.prefab)
                            if "weapon_case_souvenirpkg" in container_prefab_tree:
                                return True

            # fallback
            for collection in self.items_manager.collections:
                if f"[{paintkit.codename}]{item.codename}" in collection.items:
                    if collection.codename in self.souvenir_collections:
                        return True

            # souvenir bone mask bug
            if item.codename == "weapon_revolver" and paintkit.codename == "sp_tape":
                return True

            return False

        def has_star_prefix(item: Item) -> bool:
            prefab_tree = self.items_manager.get_prefab_tree(item.prefab)

            # gloves
            if "hands_paintable" in prefab_tree:
                return True

            # knives
            if "melee_unusual" in prefab_tree:
                return True

            return False

        def get_wear_variants(item: Item, paintkit: Paintkit) -> list[str]:
            wear_ranges = {
                "Factory New": [0.00, 0.07],
                "Minimal Wear": [0.07, 0.15],
                "Field-Tested": [0.15, 0.38],
                "Well-Worn": [0.38, 0.45],
                "Battle-Scarred": [0.45, 1.00]
            }

            item_name = self.items_manager.get_market_hash_name(item.name_tag)
            paintkit_name = self.items_manager.get_market_hash_name(paintkit.name_tag)
            if paintkit.codename == "default":
                return [item_name]

            wear_remap_min = self.items_manager.get_paintkit("default").wear_remap_min
            wear_remap_max = self.items_manager.get_paintkit("default").wear_remap_max
            if paintkit.wear_remap_min is not None:
                wear_remap_min = paintkit.wear_remap_min
            if paintkit.wear_remap_max is not None:
                wear_remap_max = paintkit.wear_remap_max

            # fix doppler names
            doppler_tags = ["PaintKit_am_marbleized_Tag", "PaintKit_am_marbleized_g_Tag"]
            if paintkit.name_tag.lstrip("#") in doppler_tags:
                if "_sapphire_marbleized" in paintkit.codename:
                    paintkit_name = f"{paintkit_name} Sapphire"
                if "_blackpearl_marbleized" in paintkit.codename:
                    paintkit_name = f"{paintkit_name} Black Pearl"
                if "_ruby_marbleized" in paintkit.codename:
                    paintkit_name = f"{paintkit_name} Ruby"
                if "_emerald_marbleized" in paintkit.codename:
                    paintkit_name = f"{paintkit_name} Emerald"
                if "_phase" in paintkit.codename:
                    paintkit_name = f"{paintkit_name} Phase {paintkit.codename.split('_phase')[1][0]}"

            results = []
            for wear_name in wear_ranges:
                if float(wear_remap_min) < wear_ranges[wear_name][1] and float(wear_remap_max) > wear_ranges[wear_name][0]:
                    results.append(f"{item_name} | {paintkit_name} ({wear_name})")

            return results

        def is_customizable(item: Item) -> bool:
            prefab_tree = self.items_manager.get_prefab_tree(item.prefab)
            for key in ["melee_unusual", "hands_paintable", "primary"]:
                if key in prefab_tree and item.baseitem != "1":
                    return True

            return False


        results = {}
        self.__debug_print("Parsing skins...")
        for item in self.items_manager.items:
            for paintkit in self.items_manager.paintkits:
                skin_codename = f"{item.codename}_{paintkit.codename}"

                if paintkit.codename == "default":
                    skin_codename = item.codename
                    if not is_customizable(item):
                        continue

                if not self.items_manager.skin_exists(skin_codename):
                    continue

                lootlist = self.get_lootlist_by_item_codename(f"[{paintkit.codename}]{item.codename}")
                collection = self.get_collection_by_item_codename(f"[{paintkit.codename}]{item.codename}")

                variants = get_wear_variants(item, paintkit)
                if has_souvenir(item, paintkit, lootlist):
                    variants += [f"Souvenir {variant}" for variant in variants]
                elif has_stattrak(item, paintkit):
                    variants += [f"StatTrak™ {variant}" for variant in variants]

                if has_star_prefix(item):
                    variants = [f"★ {variant}" for variant in variants]

                for variant in variants:
                    results[variant] = {
                        "item": item.asdict(),
                        "paintkit": paintkit.asdict(),
                        "collection": None if collection is None else collection.asdict(),
                        "lootlist": None if lootlist is None else lootlist.asdict()
                    }

        return results

    def get_stickers(self):
        results = {}
        for stickerkit in self.items_manager.stickerkits:
            if stickerkit.name_tag.startswith("#StickerKit"):
                sticker_name = self.items_manager.get_market_hash_name(stickerkit.name_tag)
                market_hash_name = f"Sticker | {sticker_name}"
                results[market_hash_name] = {"stickerkit": stickerkit.asdict()}

        return results

    def get_patches(self):
        results = {}
        for stickerkit in self.items_manager.stickerkits:
            if stickerkit.name_tag.startswith("#PatchKit"):
                sticker_name = self.items_manager.get_market_hash_name(stickerkit.name_tag)
                market_hash_name = f"Patch | {sticker_name}"
                results[market_hash_name] = {"stickerkit": stickerkit.asdict()}

        return results

    def get_graffities(self):
        def get_variants(stickerkit: Stickerkit) -> list[str]:
            variants = []
            stickerkit_name = self.items_manager.get_market_hash_name(stickerkit.name_tag)
            if not stickerkit.name_tag.startswith("#SprayKit_std"):
                return [f"Sealed Graffiti | {stickerkit_name}"]

            if stickerkit.codename in self.tinted_graffities_limited:
                for tint_name in self.tinted_graffities_limited[stickerkit.codename]:
                    variants.append(f"Sealed Graffiti | {stickerkit_name} ({tint_name})")

            else:
                for graffiti_tint in self.items_manager.graffiti_tints:
                    tint_name = self.items_manager.get_market_hash_name(graffiti_tint.name_tag)
                    variants.append(f"Sealed Graffiti | {stickerkit_name} ({tint_name})")

            return variants

        results = {}
        for stickerkit in self.items_manager.stickerkits:
            if stickerkit.name_tag.startswith("#SprayKit"):
                variants = get_variants(stickerkit)
                for variant in variants:
                    results[variant] = {"stickerkit": stickerkit.asdict()}

        return results

    def get_musickits(self):
        results = {}
        lootlist_regex = r'\[(.*?)\](.*?)$'
        for lootlist in self.items_manager.lootlists:
            for lootlist_item in lootlist.items:
                if lootlist.codename == "crate_musickit_radicals_stattrak_capsule_lootlist":
                    pass
                match = re.search(lootlist_regex, lootlist_item)
                if match is not None:
                    item_cdn, itemtype_cdn = match.groups()
                    if itemtype_cdn == "musickit":
                        item = self.items_manager.get_item(itemtype_cdn)
                        musicdef = self.items_manager.get_musicdef(item_cdn)

                        item_name = self.items_manager.get_market_hash_name(item.name_tag)
                        musicdef_name = self.items_manager.get_market_hash_name(musicdef.name_tag)

                        market_hash_name = f"{item_name} | {musicdef_name}"
                        results[market_hash_name] = {"item": item.asdict(), "musicdef": musicdef.asdict()}
                        for alias in lootlist.aliases:
                            if "stattrak" in alias:
                                market_hash_name = f"StatTrak™ {market_hash_name}"
                                results[market_hash_name] = {"item": item.asdict(), "musicdef": musicdef.asdict()}
                                break

        return results

    def get_agents(self):
        results = {}
        for item in self.items_manager.items:
            if item.prefab is not None:
                if item.prefab.codename == "customplayertradable":
                    item_name = self.items_manager.get_market_hash_name(item.name_tag)
                    results[item_name] = {"item": item.asdict()}

        return results

    def get_containers(self):
        results = {}
        for lootlist in self.items_manager.lootlists:
            for container in lootlist.containers:
                if container.codename in self.nonexisting_containers:
                    continue
                container_name = self.items_manager.get_market_hash_name(container.name_tag)
                results[container_name] = {"lootlist": lootlist.asdict(), "container": container.asdict()}

        return results

    def get_container_keys(self):
        results = {}
        for item in self.items_manager.items:
            if item.prefab is None:
                continue
            if item.prefab.codename == "weapon_case_key" and "restriction" in item.tool:
                item_name = self.items_manager.get_market_hash_name(item.name_tag)
                results[item_name] = {"item": item.asdict()}

        return results

    def get_pins(self):
        results = {}
        for item in self.items_manager.items:
            if item.prefab is None:
                continue
            if item.prefab.codename == "commodity_pin":
                item_name = self.items_manager.get_market_hash_name(item.name_tag)
                results[item_name] = {"item": item.asdict()}

        return results

    def get_passes(self):
        results = {}
        for item in self.items_manager.items:
            if item.prefab is None:
                continue

            prefab_tree = self.items_manager.get_prefab_tree(item.prefab)
            if "season_pass" in prefab_tree:
                item_name = self.items_manager.get_market_hash_name(item.name_tag)
                results[item_name] = {"item": item.asdict()}

            if "fan_token" in prefab_tree:
                if item.codename.endswith("_pack"):
                    continue
                if item.codename.endswith("_charge"):
                    continue
                item_name = self.items_manager.get_market_hash_name(item.name_tag)
                results[item_name] = {"item": item.asdict()}

        return results