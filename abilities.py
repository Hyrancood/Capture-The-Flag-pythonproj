class Ability:
    abilities = {}
    def __init__(self, id_num):
        self.id = id_num
        if str(id_num) in Ability.abilities:
            raise ValueError
        Ability.abilities[str(id_num)] = self

    def use(self, **kwargs):
        pass

freeze = Ability(0)
bomb = Ability(1)
swap = Ability(2)
pulling = Ability(3)
superdash = Ability(4)

def get_ability_by_num(num):
    return Ability.abilities[num]

