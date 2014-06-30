import pygame
import const

class Screen():

    """Run the display and interface."""

    def __init__(self):
        """Initialize the pygame window."""
        pygame.init()
        width  = const.TILESIZE*const.TILESWIDE
        height = const.TILESIZE*const.TILESWIDE
        self.surface = pygame.display.set_mode((width,height))
        pygame.display.set_caption(const.APPNAME)
        self.run = True

    def draw(self, player, things):
        """Update loop, called once per frame, and draws each thing object
        in list things.
        """
        self.surface.fill(pygame.Color('white'))
        for thing in things:
            thing.update()
            seeThing = player.sees(thing)
            x = seeThing[0] + (const.TILESIZE*(const.TILESWIDE/2))
            y = seeThing[1] + (const.TILESIZE*(const.TILESWIDE/2))
            rec = (x,y,const.TILESIZE,const.TILESIZE)
            pygame.draw.rect(self.surface, pygame.Color('black'), rec, 0)
        pygame.display.flip()
        return pygame.event.get()

    def close(self):
        self.run = False
        pygame.display.quit()
