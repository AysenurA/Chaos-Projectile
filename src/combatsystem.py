"""
.. module:: combatsystem
    :platform: Unix, Windows
    :synopsis: Handles collision between characters and projectiles, handles attacks etc.
"""

import events


class CombatSystem():
    """Handles collision between characters and projectiles, handles attacks etc.
    
    :Attributes:
        - *event_manager* (:class:`events.EventManager`): event manager
        - *world* (:class:`gameWorld.GameWorld`): game world contains entities
    """

    def __init__(self, event_manager, world):
        """
        :param event_manager: event manager
        :type event_manager: events.EventManager
        :param world: game world contains entities
        :type world: gameWorld.GameWorld
        """
        self.event_manager = event_manager
        self.event_manager.register_listener(self)

        self.world = world

    def notify(self, event):
        """Notify, when event occurs. 
        
        :param event: occured event
        :type event: events.Event
        """
        if isinstance(event, events.TickEvent):
            self.update()
        #if isinstance(event, events.CollisionOccured):
        #    self.handle_collision(event.collider_ID, event.collidee_ID)

    def update(self):
        """Update all particle emitters, remove dead objects and execute attacks."""
        #Execute attacks
        for entity_ID in self.world.state:
            attack_Nr = self.world.state[entity_ID].attacks
            if attack_Nr > -1:
                self.execute_attack(entity_ID, attack_Nr)
        for attacks in self.world.attacks.itervalues():
            for attack in attacks:
                attack.update()
        #Check for collision
        self.check_projectile_collision()

    def check_projectile_collision(self):
        """Checks for collision between projectiles and other objects."""
        for attacks_ID in self.world.attacks:
            for attack in self.world.attacks[attacks_ID]:
                for projectile in attack.particles:
                    for collider_ID in self.world.collider:
                        if not collider_ID == attacks_ID:
                            if self.world.collider[collider_ID].colliderect(projectile.rect):
                                projectile.life = -1

    def execute_attack(self, entity_ID, attack_Nr):
        """Entity executes one of its possible attacks if cooldown is ready.
        
        :param entity_ID: entity
        :type entity_ID: int
        :param attack_Nr: number of the attacks that is executed
        :type attack_Nr: int
        """
        if entity_ID in self.world.players:
            orb_ID = self.world.players[entity_ID].orb_ID
            position = self.world.appearance[orb_ID].rect.center
        else:
            position = self.world.appearance[entity_ID].rect.center
        direction = self.world.direction[entity_ID]
        velocity = [direction[0] * 3,
                    direction[1] * 3]
        spawned = self.world.attacks[entity_ID][attack_Nr].spawn_particles(velocity, position)
        if spawned:
            #Post attack event
            ev = events.EntityAttacks(entity_ID)
            self.event_manager.post(ev)
        #Attack executed, so reset state
        self.world.state[entity_ID].attacks = -1

#    def handle_collision(self, collider_ID, collidee_ID):
#        pass