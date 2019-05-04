# input lib
from pygame.locals import *
import pygame, string

class ConfigError(KeyError): pass

class Config:
    """ A utility for configuration """
    def __init__(self, options, *look_for):
        assertions = []
        for key in look_for:
            if key[0] in options.keys(): exec('self.'+key[0]+' = options[\''+key[0]+'\']')
            else: exec('self.'+key[0]+' = '+key[1])
            assertions.append(key[0])
        for key in options.keys():
            if key not in assertions: raise ConfigError(key+' not expected as option')

class Input:
    """ A text input for pygame apps """
    def __init__(self, **options):
        """ Options: x, y, font, color, restricted, maxlength, prompt """
        self.options = Config(options, ['x', '0'], ['y', '0'], ['font', 'pygame.font.Font(None, 32)'],
                              ['color', '(0,0,0)'], ['restricted', '\'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&\\\'()*+,-./:;<=>?@[\]^_`{|}~\''],
                              ['maxlength', '-1'], ['prompt', '\'\''])
        self.x = self.options.x; self.y = self.options.y
        self.font = self.options.font
        self.color = self.options.color
        self.restricted = self.options.restricted
        self.maxlength = self.options.maxlength
        self.prompt = self.options.prompt; self.value = ''
        self.shifted = True

    def set_pos(self, x, y):
        """ Set the position to x, y """
        self.x = x
        self.y = y

    def set_font(self, font):
        """ Set the font for the input """
        self.font = font

    def draw(self, surface):
        """ Draw the text input to a surface """
        text = self.font.render(self.prompt+self.value, 1, self.color)
        surface.blit(text, (self.x, self.y))

    def update(self, event):

        if event.key == K_BACKSPACE: self.value = self.value[:-1]
        elif event.key == K_a and 'A' in self.restricted: self.value += 'A'
        elif event.key == K_b and 'B' in self.restricted: self.value += 'B'
        elif event.key == K_c and 'C' in self.restricted: self.value += 'C'
        elif event.key == K_d and 'D' in self.restricted: self.value += 'D'
        elif event.key == K_e and 'E' in self.restricted: self.value += 'E'
        elif event.key == K_f and 'F' in self.restricted: self.value += 'F'
        elif event.key == K_g and 'G' in self.restricted: self.value += 'G'
        elif event.key == K_h and 'H' in self.restricted: self.value += 'H'
        elif event.key == K_i and 'I' in self.restricted: self.value += 'I'
        elif event.key == K_j and 'J' in self.restricted: self.value += 'J'
        elif event.key == K_k and 'K' in self.restricted: self.value += 'K'
        elif event.key == K_l and 'L' in self.restricted: self.value += 'L'
        elif event.key == K_m and 'M' in self.restricted: self.value += 'M'
        elif event.key == K_n and 'N' in self.restricted: self.value += 'N'
        elif event.key == K_o and 'O' in self.restricted: self.value += 'O'
        elif event.key == K_p and 'P' in self.restricted: self.value += 'P'
        elif event.key == K_q and 'Q' in self.restricted: self.value += 'Q'
        elif event.key == K_r and 'R' in self.restricted: self.value += 'R'
        elif event.key == K_s and 'S' in self.restricted: self.value += 'S'
        elif event.key == K_t and 'T' in self.restricted: self.value += 'T'
        elif event.key == K_u and 'U' in self.restricted: self.value += 'U'
        elif event.key == K_v and 'V' in self.restricted: self.value += 'V'
        elif event.key == K_w and 'W' in self.restricted: self.value += 'W'
        elif event.key == K_x and 'X' in self.restricted: self.value += 'X'
        elif event.key == K_y and 'Y' in self.restricted: self.value += 'Y'
        elif event.key == K_z and 'Z' in self.restricted: self.value += 'Z'


        if len(self.value) > self.maxlength and self.maxlength >= 0: self.value = self.value[:-1]
