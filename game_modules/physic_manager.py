from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_modules.world import World
    from game_modules.objects.dynamic_object import DynamicObject
    from game_modules.objects.static_object import StaticObject
import pygame
from functools import lru_cache


class PhysicManager:
    def __init__(self, world : World):
        self.world = world
        self.static_objects : list[StaticObject] = world.static_objects
        self.dynamic_objets : list[DynamicObject] = world.dynamic_objects

    @property
    def physical_objects(self) -> list[StaticObject | DynamicObject]:
        return self.static_objects + self.dynamic_objets
    
    def move_horizontal(self, obj : pygame.sprite.Sprite) -> None:
        obj.pos.x += obj.vel.x
        obj.rect.x = obj.pos.x

    def check_horizontal_collision(self, obj : DynamicObject) -> None:
        for collision_obj in self.physical_objects:
            if obj == collision_obj:
                continue
            if not collision_obj.alive():
                continue
            if not obj.rect.colliderect(collision_obj.rect):
                continue
            self.world.handle_collisions(obj, collision_obj)
            if not collision_obj.solid:
                continue
            if obj.phasing:
                continue

            if collision_obj.pushable and collision_obj.push_vel.x != 0:
                collision_obj.vel.x = obj.vel.x
                self.move_horizontal(collision_obj)
                self.check_horizontal_collision(collision_obj)

            if obj.vel.x > 0:
                obj.rect.right = collision_obj.rect.left
            if obj.vel.x < 0:
                obj.rect.left = collision_obj.rect.right
            
        obj.vel.x = 0
        obj.pos.x = obj.rect.x

    def move_vertical(self,obj : DynamicObject) -> None:
        obj.pos.y += obj.vel.y
        obj.rect.y = obj.pos.y

    def check_vertical_collision(self, obj : DynamicObject) -> None:
        for collision_obj in self.physical_objects:
            if obj == collision_obj:
                continue
            if not collision_obj.alive():
                continue
            if not obj.rect.colliderect(collision_obj.rect):
                continue
            self.world.handle_collisions(obj, collision_obj)
            if not collision_obj.solid:
                continue
            if obj.phasing:
                continue

            if collision_obj.pushable and collision_obj.push_vel.y != 0:
                collision_obj.vel.y = obj.vel.y
                self.move_vertical(collision_obj)
                self.check_vertical_collision(collision_obj)

            if obj.vel.y > 0:
                obj.rect.bottom = collision_obj.rect.top
            if obj.vel.y < 0:
                obj.rect.top = collision_obj.rect.bottom

        obj.vel.y = 0
        obj.pos.y = obj.rect.y  

    def move_and_collide(self, obj : DynamicObject) -> None:
        if not obj.alive():
            return

        obj.calculate_velocity()
        self.move_horizontal(obj)
        self.check_horizontal_collision(obj)
        self.move_vertical(obj)
        self.check_vertical_collision(obj)

    def fixed_update(self) -> None:
        for obj in self.dynamic_objets:
            self.move_and_collide(obj)