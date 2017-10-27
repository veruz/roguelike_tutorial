from game_messages import Message


def heal(*args, **kwargs):
    entity = args[0]
    colors = args[1]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health', colors.get('yellow'))})
    else:
        entity.fighter.heal(amount)
        results.append(
            {'consumed': True, 'message': Message('Your wounds are starting to feel better', colors.get('green'))})

    return results


def cast_lightning(*args, **kwargs):
    caster = args[0]
    colors = args[1]
    entities = kwargs.get('entities')
    game_map = kwargs.get('game_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and game_map.fov[entity.x, entity.y]:
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({'consumed': True, 'target': target,
                        'message': Message('A lightning bolt strikes {0} for {1} damage!'.format(target.name, damage))})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append(
            {'consumed': False, 'target': target, 'message': Message('No enemy in range.', colors.get('red'))})

    return results


def cast_fireball(*args, **kwargs):
    colors = args[1]
    entities = kwargs.get('entities')
    game_map = kwargs.get('game_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not game_map.fov[target_x, target_y]:
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.',
                                                              colors.get('yellow'))})

        return results

    results.append({'consumed': True,
                    'message': Message('The fireball explodes, burning everything within {0} tiles!'.format(radius),
                                       colors.get('orange'))})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({'message': Message('The {0} gets burned for {1} damage.'.format(entity.name, damage))})

            results.extend(entity.fighter.take_damage(damage))

    return results
