from game_messages import Message

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item, colors):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full'.format(colors.get('yellow')))
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('You picked up the {0}!'.format(item.name), colors.get('yellow'))
            })

            self.items.append(item)

        return results

    def use(self, item_entity, colors, **kwargs):
        results = []

        item_component = item_entity.item

        if item_component.use_function is None:
            results.append({'message': Message('The {0} cannot be used.'.format(item_entity.name), colors.get('yellow'))})
        else:
            kwargs = {**item_component.function_kwargs, **kwargs}
            item_use_results = item_component.use_function(self.owner, colors, **kwargs)

            for item_use_result in item_use_results:
                if item_use_result.get('consumed'):
                    self.remove_item(item_entity)

            results.extend(item_use_results)

        return results

    def remove_item(self, item):
        self.items.remove(item)

    def drop_item(self, item, colors):
        results = []

        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)
        results.append({'item': item, 'message': Message('You dropped the {0}'.format(item.name), colors.get('yellow'))})

        return results