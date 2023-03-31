"""Character Attacks"""

from attrs import define


@define
class AttackSpec:
    name: str
    damage: float
    atk_type: str
    charge_time: float
    cooldown: float


quick_attack = AttackSpec(
    name="Quick Attack",
    damage=25,
    atk_type="Melee",
    charge_time=0,
    cooldown=1
)
charge_attack = AttackSpec(
    name="Charge Attack",
    damage=100,
    atk_type="Melee",
    charge_time=1,
    cooldown=5
)
stealth_attack = AttackSpec(
    name="Stealth Attack",
    damage=float("inf"),
    atk_type="Melee",
    charge_time=3,
    cooldown=10
)
throw_knife_attack = AttackSpec(
    name="Throw knives",
    damage=20,
    atk_type="Ranged",
    charge_time=0,
    cooldown=1
)
enemy_default_attack = AttackSpec(
    name="Enemy Attack",
    damage=300,
    atk_type="Melee",
    charge_time=0,
    cooldown=2
)

player_attacks = [quick_attack, charge_attack, stealth_attack, throw_knife_attack]
default_enemy_attacks = [enemy_default_attack]