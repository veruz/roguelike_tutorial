def render_all(con, entities, game_map, root_console, screen_width, screen_height, colors):
    # draw all map tiles
    for x,y in game_map:
        wall = not game_map.transparent[x,y]

        if wall:
            con.draw_char(x, y, None, fg=None, bg=colors.get('dark wall'))
        else:
            con.draw_char(x, y, None, fg=None, bg=colors.get('dark ground'))

    # Draw all entities in list
    for entity in entities:
        draw_entity(con,entity)

    root_console.blit(con, 0, 0, screen_width, screen_height)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity):
    con.draw_char(entity.x, entity.y, entity.char, entity.color, bg=None)


def clear_entity(con, entity):
    # erase representing character
    con.draw_char(entity.x, entity.y, ' ', entity.color, bg=None)