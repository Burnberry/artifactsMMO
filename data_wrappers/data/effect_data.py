effect_data = {
    "boost_hp": {
        "name": "Boost HP",
        "code": "boost_hp",
        "description": "Add xHP at the start of the fight and for the duration of the fight.",
        "type": "combat",
        "subtype": "buff"
    },
    "boost_dmg_fire": {
        "name": "Boost Damage Fire",
        "code": "boost_dmg_fire",
        "description": "Add x% fire damage at the start of the fight and for the duration of the fight.",
        "type": "combat",
        "subtype": "buff"
    },
    "boost_dmg_water": {
        "name": "Boost Damage Water",
        "code": "boost_dmg_water",
        "description": "Add x% water damage at the start of the fight and for the duration of the fight.",
        "type": "combat",
        "subtype": "buff"
    },
    "boost_dmg_air": {
        "name": "Boost Damage Air",
        "code": "boost_dmg_air",
        "description": "Add x% air damage at the start of the fight and for the duration of the fight.",
        "type": "combat",
        "subtype": "buff"
    },
    "boost_dmg_earth": {
        "name": "Boost Damage Earth",
        "code": "boost_dmg_earth",
        "description": "Add x% earth damage at the start of the fight and for the duration of the fight.",
        "type": "combat",
        "subtype": "buff"
    },
    "restore": {
        "name": "Restore",
        "code": "restore",
        "description": "Restores xHP at the start of the turn if the player has lost more than 50% of his health points.",
        "type": "combat",
        "subtype": "heal"
    },
    "healing": {
        "name": "Healing",
        "code": "healing",
        "description": "Every 3 played turns, restores x% of HP at the start of the turn.\n",
        "type": "combat",
        "subtype": "special"
    },
    "antipoison": {
        "name": "Antipoison",
        "code": "antipoison",
        "description": "At the beginning of the turn, if the character has at least one poison on him, removes x poison damage.",
        "type": "combat",
        "subtype": "other"
    },
    "poison": {
        "name": "Poison",
        "code": "poison",
        "description": "At the start of his first turn, apply a poison of x on one of your opponents. Loses xHP per turn, damage cannot be dodged.",
        "type": "combat",
        "subtype": "special"
    },
    "lifesteal": {
        "name": "Lifesteal",
        "code": "lifesteal",
        "description": "Restores x% of the total attack of all elements in HP after a critical strike.",
        "type": "combat",
        "subtype": "special"
    },
    "reconstitution": {
        "name": "Reconstitution",
        "code": "reconstitution",
        "description": "At the beginning of the turn x, regains all HP.",
        "type": "combat",
        "subtype": "special"
    },
    "burn": {
        "name": "Burn",
        "code": "burn",
        "description": "On your first turn, apply a burn effect of x% of your attack of all elements. The damage is applied each turn and decreases by 10% each time. It is impossible to block.",
        "type": "combat",
        "subtype": "special"
    },
    "boost_res_air": {
        "name": "Boost Resistance Air",
        "code": "boost_res_air",
        "description": "Gives x% air resistance at the start of fight.",
        "type": "combat",
        "subtype": "buff"
    },
    "boost_res_water": {
        "name": "Boost Resistance Water",
        "code": "boost_res_water",
        "description": "Gives x% water resistance at the start of fight.",
        "type": "combat",
        "subtype": "buff"
    },
    "boost_res_earth": {
        "name": "Boost Resistance Earth",
        "code": "boost_res_earth",
        "description": "Gives x% earth resistance at the start of fight.",
        "type": "combat",
        "subtype": "buff"
    },
    "boost_res_fire": {
        "name": "Boost Resistance Fire",
        "code": "boost_res_fire",
        "description": "Gives x% fire resistance at the start of fight.",
        "type": "combat",
        "subtype": "buff"
    },
    "heal": {
        "name": "Heal",
        "code": "heal",
        "description": "Heal xHP when the item is used.",
        "type": "consumable",
        "subtype": "heal"
    },
    "teleport_x": {
        "name": "Teleport X",
        "code": "teleport_x",
        "description": "Teleports to position (X) x when the item is used.",
        "type": "consumable",
        "subtype": "teleport"
    },
    "gold": {
        "name": "Gold",
        "code": "gold",
        "description": "Adds x gold in your inventory.",
        "type": "consumable",
        "subtype": "gold"
    },
    "teleport_y": {
        "name": "Teleport Y",
        "code": "teleport_y",
        "description": "Teleports to position (Y) x when the item is used.",
        "type": "consumable",
        "subtype": "teleport"
    },
    "attack_fire": {
        "name": "Fire Attack",
        "code": "attack_fire",
        "description": "Adds x Fire Attack to its stats when equipped.",
        "type": "equipment",
        "subtype": "stat"
    },
    "attack_water": {
        "name": "Water Attack",
        "code": "attack_water",
        "description": "Adds x Water Attack to its stats when equipped.",
        "type": "equipment",
        "subtype": "stat"
    },
    "attack_air": {
        "name": "Air Attack",
        "code": "attack_air",
        "description": "Adds x Air Attack to its stats when equipped.",
        "type": "equipment",
        "subtype": "stat"
    },
    "attack_earth": {
        "name": "Earth Attack",
        "code": "attack_earth",
        "description": "Adds x Earth Attack to its stats when equipped.",
        "type": "equipment",
        "subtype": "stat"
    },
    "dmg": {
        "name": "Damage",
        "code": "dmg",
        "description": "Adds x% Damage to its stats when equipped.",
        "type": "equipment",
        "subtype": "stat"
    },
    "dmg_fire": {
        "name": "Fire Damage",
        "code": "dmg_fire",
        "description": "Adds x% Fire Damage to its stats when equipped.",
        "type": "equipment",
        "subtype": "stat"
    },
    "dmg_water": {
        "name": "Water Damage",
        "code": "dmg_water",
        "description": "Adds x% Water Damage to its stats when equipped.",
        "type": "equipment",
        "subtype": "stat"
    },
    "dmg_air": {
        "name": "Air Damage",
        "code": "dmg_air",
        "description": "Adds x% Air Damage to its stats when equipped.",
        "type": "equipment",
        "subtype": "stat"
    },
    "dmg_earth": {
        "name": "Earth Damage",
        "code": "dmg_earth",
        "description": "Adds x% Earth Damage to its stats when equipped.",
        "type": "equipment",
        "subtype": "stat"
    },
    "res_fire": {
        "name": "Fire Resistance",
        "code": "res_fire",
        "description": "Adds x% Fire Res to its stats when equipped.",
        "type": "equipment",
        "subtype": "stat"
    },
    "res_water": {
        "name": "Water Resistance",
        "code": "res_water",
        "description": "Adds x% Water Res to its stats when equipped.",
        "type": "equipment",
        "subtype": "stat"
    },
    "res_air": {
        "name": "Air Resistance",
        "code": "res_air",
        "description": "Adds x% Air Res to its stats when equipped.",
        "type": "equipment",
        "subtype": "stat"
    },
    "res_earth": {
        "name": "Earth Resistance",
        "code": "res_earth",
        "description": "Adds x% Earth Res to its stats when equipped.",
        "type": "equipment",
        "subtype": "stat"
    },
    "critical_strike": {
        "name": "Critical Strike",
        "code": "critical_strike",
        "description": "Adds x% Critical Strike to its stats when equipped. Critical strikes adds 50% extra damage to an attack (1.5x). ",
        "type": "equipment",
        "subtype": "stat"
    },
    "wisdom": {
        "name": "Wisdom",
        "code": "wisdom",
        "description": "Adds x Wisdom to its stats when equipped. Each point of wisdom increases your xp in combat. (1% extra per 10 wisdom)",
        "type": "equipment",
        "subtype": "stat"
    },
    "prospecting": {
        "name": "Prospecting",
        "code": "prospecting",
        "description": "Adds x Prospecting to its stats when equipped. Each PP increases your chance of obtaining drops. (1% extra per 10 PP)",
        "type": "equipment",
        "subtype": "stat"
    },
    "woodcutting": {
        "name": "Woodcutting",
        "code": "woodcutting",
        "description": "Reduces cooldown by x% when a character logs a tree.",
        "type": "equipment",
        "subtype": "gathering"
    },
    "fishing": {
        "name": "Fishing",
        "code": "fishing",
        "description": "Reduces cooldown by x% when a character is fishing.",
        "type": "equipment",
        "subtype": "gathering"
    },
    "mining": {
        "name": "Mining",
        "code": "mining",
        "description": "Reduces cooldown by x% when a character mines a resource.",
        "type": "equipment",
        "subtype": "gathering"
    },
    "alchemy": {
        "name": "Alchemy",
        "code": "alchemy",
        "description": "Reduces cooldown by x% when a character harvest a plant.",
        "type": "equipment",
        "subtype": "gathering"
    },
    "hp": {
        "name": "Hit points",
        "code": "hp",
        "description": "Adds x HP to its stats when equipped.",
        "type": "equipment",
        "subtype": "stat"
    },
    "inventory_space": {
        "name": "Inventory Space",
        "code": "inventory_space",
        "description": "Adds x to the maximum number of items in the inventory when equipped.",
        "type": "equipment",
        "subtype": "stat"
    },
    "haste": {
        "name": "Haste",
        "code": "haste",
        "description": "Adds x Haste to its stats when equipped. The haste reduces the cooldown of a fight. ",
        "type": "equipment",
        "subtype": "stat"
    }
}