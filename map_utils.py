from random import randint

class Rect:
    def __init__(self, x ,y , w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        # true if rect intersects with another
        return(self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1)



def create_room(game_map, room):
    # go through tiles in rect and make passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            game_map.walkable[x, y] = True
            game_map.transparent[x, y] = True


def create_h_tunnel(game_map, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2)):
        game_map.walkable[x,y] = True
        game_map.transparent[x, y] = True

def create_v_tunnel(game_map, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2)):
        game_map.walkable[x, y] = True
        game_map.transparent[x, y] = True


def make_map(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height, player):
    rooms = []
    num_rooms = 0

    for r in range(max_rooms):
        # random width and height
        w = randint(room_min_size, room_max_size)
        h = randint(room_min_size, room_max_size)
        # random position without going out of bounds
        x = randint(0, map_width - w -1)
        y = randint(0, map_height - h -1)

        new_room = Rect(x, y, w, h)
        # run through the other rooms and see if intersect
        for other_room in rooms:
            if new_room.intersect(other_room):
                break
        else:
            # no intersection, valid room

            # paint room to tiles
            create_room(game_map, new_room)

            # center coords of new room
            (new_x, new_y) = new_room.center()

            if num_rooms == 0:
                # first room/player start
                player.x = new_x
                player.y = new_y
            else:
                # rooms after first
                # connect with tunnels

                # center coords of prev room
                (prev_x, prev_y) = rooms[num_rooms -1].center()

                # coin flip
                if randint(0, 1) == 1:
                    # first move horz then vert
                    create_h_tunnel(game_map, prev_x, new_x, prev_y)
                    create_v_tunnel(game_map, prev_y, new_y, new_x)
                else:
                    # first ver then horz
                    create_v_tunnel(game_map, prev_y, new_y, prev_x)
                    create_h_tunnel(game_map, prev_x, new_x, new_y)

            # append room to list
            rooms.append(new_room)
            num_rooms += 1