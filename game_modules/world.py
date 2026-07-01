import pygame, random, math
from .namings import StateName 
from .assets_loader import AssetsLoader
from game_modules.game_grid import GameGrid
from game_modules.objects.static_image import StaticImage
from game_modules.objects.static_object import StaticObject
from game_modules.objects.dynamic_object import DynamicObject
from game_modules.objects.object_clock import ObjectClock
from game_modules.objects.hud import Hud
from game_modules.objects.invisible_wall import InvisibleWall
from game_modules.objects.player import Player
from game_modules.objects.normal_mushroom import NormalMushroom
from game_modules.objects.bad_mushroom import BadMushroom
from game_modules.objects.vacuum_mushroom import VacuumMushroom
from game_modules.objects.running_mushroom import RunningMushroom
from game_modules.objects.sky_mushroom import SkyMushroom
from game_modules.objects.spike import Spike
from game_modules.objects.chest import Chest
from game_modules.objects.key import Key
from game_modules.objects.flood import Flood
from game_modules.objects.boss import Boss
from game_modules.objects.spore import Spore


class World:
    GAMEPLAY_LEVEL : int = 9
    def __init__(self, state : StateName = StateName.MAIN_MENU):
        self.state = state
        self.assets_loader = AssetsLoader()
        self.assets = self.assets_loader.assets
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.static_objects : list[StaticObject] = []
        self.dynamic_objects : list[DynamicObject] = []
        self.object_clocks : list[ObjectClock] = []
        self.get_background()
        if self.state == StateName.GAMEPLAY:
            self.collected_mushrooms : int = 0
            self.game_grid = GameGrid()
            self.get_gameplay_objects()

    def get_background(self) -> None:
        if self.state == StateName.MAIN_MENU:
            image = self.assets["title_screen.png"]
        elif self.state == StateName.LEVEL_MENU:
            image = self.assets["levels_screen.png"]
        elif self.state == StateName.SKINS_MENU:
            image = self.assets["skins_screen.png"]
        elif self.state == StateName.GAMEPLAY:
            image = self.assets["gameplay_background.png"]
        elif self.state == StateName.LEVEL_COMPLETE:
            image = self.assets["complete_screen.png"]
        elif self.state == StateName.GAME_OVER:
            image = self.assets["over_screen.png"]

        pos = pygame.Vector2(0, 0)  
        self.background = StaticImage(image, pos)
        self.all_sprites.add(self.background, layer=1)

    def get_hug(self) -> None:
        image = self.assets["game_hud.png"]
        pos = pygame.Vector2(0, 0)
        font = self.assets["PressStart2P.ttf"]
        self.hud = Hud(image, pos, font)
        self.hud.level = World.GAMEPLAY_LEVEL
        self.all_sprites.add(self.hud, layer=9)

    def get_invisible_walls(self) -> None:
        image_north = pygame.surface.Surface((800, 40))
        pos_north = pygame.Vector2(800//2, 40)
        image_south = pygame.surface.Surface((800, 40))
        pos_south = pygame.Vector2(800//2, 600 + 40)
        image_west = pygame.surface.Surface((40, 600))
        pos_west = pygame.Vector2(0 - 20, 600)
        image_east = pygame.surface.Surface((40, 600))
        pos_east = pygame.Vector2(800 + 20, 600)
        walls = [(image_north, pos_north),
                 (image_south, pos_south),
                 (image_west, pos_west),
                 (image_east, pos_east)]
        for img, pos in walls:
            wall = InvisibleWall(img, pos)
            self.static_objects.append(wall)

    def get_player(self) -> None:
        image = self.assets["player.png"]
        pos = pygame.Vector2(100, 320)
        self.player = Player(image, pos)
        self.all_sprites.add(self.player, layer=10)
        self.dynamic_objects.append(self.player)

    def get_normal_mushrooms(self) -> None:
        image = self.assets["normal_mushroom.png"]
        for _ in range(20):
            pos = self.game_grid.get_normal_object_spawn_pos()
            normal_mushroom = NormalMushroom(image, pos)
            self.all_sprites.add(normal_mushroom, layer=8)
            self.static_objects.append(normal_mushroom)

    def get_bad_mushrooms(self) -> None:
        image = self.assets["bad_mushroom.png"]
        for _ in range(20):
            pos = self.game_grid.get_normal_object_spawn_pos()
            normal_mushroom = BadMushroom(image, pos)
            self.all_sprites.add(normal_mushroom, layer=8)
            self.static_objects.append(normal_mushroom)

    def get_spikes(self) -> None:
        image = self.assets["spike.png"]
        for _ in range(20):
            pos = self.game_grid.get_normal_object_spawn_pos()
            spike = Spike(image, pos)
            self.all_sprites.add(spike, layer=8)
            self.static_objects.append(spike)

    def get_vacuum_mushrooms(self) -> None:
        image = self.assets["vacuum_mushroom.png"]
        for _ in range(20):
            pos = self.game_grid.get_normal_object_spawn_pos()
            vacuum_mushroom = VacuumMushroom(image, pos, self.get_player_pos)
            self.all_sprites.add(vacuum_mushroom, layer=8)
            self.dynamic_objects.append(vacuum_mushroom)

    def get_running_mushrooms(self) -> None:
        image = self.assets["running_mushroom.png"]
        for _ in range(20):
            pos = self.game_grid.get_normal_object_spawn_pos()
            running_mushroom = RunningMushroom(image, pos, self.get_player_pos)
            self.all_sprites.add(running_mushroom, layer=8)
            self.dynamic_objects.append(running_mushroom)

    def get_chest(self) -> None:
        image = self.assets["chest.png"]
        pos = pygame.Vector2(700, 480)
        self.chest = Chest(image, pos)
        self.all_sprites.add(self.chest, layer=8)
        self.static_objects.append(self.chest)

    def get_key(self) -> None:
        image = self.assets["key.png"]
        pos = pygame.Vector2(700, 160)
        self.key = Key(image, pos)
        self.all_sprites.add(self.key, layer=9)
        self.dynamic_objects.append(self.key)

    def get_sky_mushroom(self) -> None:
        image = self.assets["sky_mushroom.png"]
        pobible_pos_x = [20 + x * 40 for x in range(20)]
        pos_x = random.choice(pobible_pos_x)
        pos_y = -20
        pos = pygame.Vector2(pos_x, pos_y)
        sky_mushroom = SkyMushroom(image, pos)
        self.all_sprites.add(sky_mushroom, layer=8)
        self.dynamic_objects.append(sky_mushroom)

    def get_flood(self) -> None:
        image = self.assets["flood.png"]
        pos = self.game_grid.get_flood_spawn_pos()
        flood = Flood(image, pos)
        s_rects = [s.rect for s in self.all_sprites if isinstance(s, (Player, NormalMushroom, Flood))]
        for _ in range(100):
            pos = self.game_grid.get_flood_spawn_pos()
            flood = Flood(image, pos)
            if flood.rect.collidelist(s_rects) == -1:
                test_rect = flood.rect.copy()
                test_rect.scale_by_ip(3, 3)
                test_rect.center = flood.rect.center
                if not test_rect.colliderect(self.player.rect):
                    break
        else:
            print("flood failed")
            return
        self.all_sprites.add(flood, layer=7)
        self.static_objects.append(flood)
    
    def get_boss(self) -> None:
        image = self.assets["boss.png"]
        pos = pygame.Vector2(700, 320)
        self.boss = Boss(image, pos, self.get_player_pos, self.get_spores)
        self.all_sprites.add(self.boss, layer=9)
        self.dynamic_objects.append(self.boss)

    def get_spores(self) -> None:
        boss_center = pygame.Vector2(self.boss.rect.center)
        offset_from_boss = 50

        image = self.assets["spore.png"]
        starting_angles = [a for a in range(0, 341, 20)]

        for a in starting_angles:
            a += random.choice(range(-20, 21))
            if a < 0:
                a = 0

            direction_from_boss_x = round(math.cos(float(math.radians(a))), 4)
            direction_from_boss_y = round(-math.sin(float(math.radians(a))), 4)
            pos = pygame.Vector2(boss_center)
            movement_direction = pygame.Vector2(direction_from_boss_x, direction_from_boss_y).normalize()
            spore = Spore(image, pos, movement_direction)
            self.all_sprites.add(spore, layer=8)
            self.dynamic_objects.append(spore)



    def get_object_clock(self, object) -> None:
        if object == SkyMushroom:
            sky_mushroom_clock = ObjectClock(1.0, self.get_sky_mushroom)
            self.object_clocks.append(sky_mushroom_clock)
        if object == Flood:
            flood_clock = ObjectClock(0.25, self.get_flood)
            self.object_clocks.append(flood_clock)

    def get_gameplay_objects(self) -> None:
        self.get_hug()
        self.get_invisible_walls()
        self.get_player()
        if World.GAMEPLAY_LEVEL in (1, 2, 3, 8):
            self.get_normal_mushrooms()
        if World.GAMEPLAY_LEVEL == 2:
            self.get_bad_mushrooms()
        if World.GAMEPLAY_LEVEL == 3:
            self.get_spikes()
        if World.GAMEPLAY_LEVEL == 4:
            self.get_vacuum_mushrooms()
        if World.GAMEPLAY_LEVEL == 5:
            self.get_running_mushrooms()
        if World.GAMEPLAY_LEVEL == 6:
            self.get_chest()
            self.get_key()
        if World.GAMEPLAY_LEVEL == 7:
            self.get_object_clock(object=SkyMushroom)
        if World.GAMEPLAY_LEVEL == 8:
            self.get_object_clock(object=Flood)
        if World.GAMEPLAY_LEVEL == 9:
            self.get_boss()

    def get_player_pos(self) -> pygame.Vector2:
        player_center = self.player.rect.center
        return pygame.Vector2(player_center[0], player_center[1])

    def handle_collisions(self, obj_a, obj_b) -> None:
        if isinstance(obj_a, Player) and (isinstance(obj_b, NormalMushroom) or isinstance(obj_b, VacuumMushroom) or isinstance(obj_b, RunningMushroom) or isinstance(obj_b, SkyMushroom)):
            self.collected_mushrooms += 1
            self.hud.collected_mushrooms = self.collected_mushrooms
            obj_b.kill()
            self.assets["pickup.wav"].play()
            if not (isinstance(obj_b, SkyMushroom) or isinstance(obj_b, VacuumMushroom) or isinstance(obj_b, RunningMushroom)):
                x, y = obj_b.rect.midbottom 
                grid_col = (y - 40) / 40
                grid_row = (x - 20) / 40
                self.game_grid.grid[int(grid_col)][int(grid_row)] = "o"
            
        elif isinstance(obj_a, Player) and (isinstance(obj_b, BadMushroom) or isinstance(obj_b, Spike)):
            self.player.kill()
            self.assets["hit.wav"].play()
        elif isinstance(obj_a, Player) and isinstance(obj_b, Key):
            if obj_a.vel.x > 0:
                obj_b.push_vel = pygame.Vector2(1, 0)
            elif obj_a.vel.x < 0:
                obj_b.push_vel = pygame.Vector2(-1, 0)
            elif obj_a.vel.y > 0:
                obj_b.push_vel = pygame.Vector2(0, 1)
            elif obj_a.vel.y < 0:
                obj_b.push_vel = pygame.Vector2(0, -1)
        elif isinstance(obj_a, Key) and isinstance(obj_b, Chest):
            obj_a.kill()
            obj_b.kill()
            self.get_normal_mushrooms()
            self.assets["pickup.wav"].play()
        elif isinstance(obj_a, SkyMushroom) and isinstance(obj_b, InvisibleWall):
            if not obj_a.phasing:
                self.player.kill()
        elif isinstance(obj_a, Player) and isinstance(obj_b, Boss):
            player_center = pygame.Vector2(obj_a.rect.center)
            boss_center = pygame.Vector2(obj_b.rect.center)

            player_knockback_vector = player_center - boss_center
            if player_knockback_vector.length() != 0: player_knockback_vector.normalize_ip()
            player_knockback_vector = player_knockback_vector*8
            obj_a.knockback_vel.xy = player_knockback_vector.xy

            boss_knockback_vector = boss_center - player_center
            if boss_knockback_vector.length() != 0: boss_knockback_vector.normalize_ip()
            boss_knockback_vector = boss_knockback_vector*16

            if obj_b.current_phase["name"] == "chase":
                obj_b.knockback_vel.xy = boss_knockback_vector.xy
