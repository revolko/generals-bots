import pygame
from enum import Enum
from pygame.event import Event
from abc import abstractmethod

from .properties import Properties
from generals.core import config as c


class Keybindings(Enum):
    ### General ###
    Q = pygame.K_q  # Quit the game

    ### Replay ###
    RIGHT = pygame.K_RIGHT  # Increase speed
    LEFT = pygame.K_LEFT  # Decrease speed
    SPACE = pygame.K_SPACE  # Pause
    R = pygame.K_r  # Restart
    L = pygame.K_l  # Move forward one frame
    H = pygame.K_h  # Move back one frame


class Command:
    def __init__(self):
        self.quit: bool = False


class ReplayCommand(Command):
    def __init__(self):
        super().__init__()
        self.frame_change: int = 0
        self.speed_change: float = 1.0
        self.restart: bool = False
        self.pause_toggle: bool = False


class GameCommand(Command):
    def __init__(self):
        super().__init__()
        raise NotImplementedError


class TrainCommand(Command):
    def __init__(self):
        super().__init__()


class EventHandler:
    def __init__(self, properties: Properties):
        """
        Initialize the event handler.

        Args:
            properties: the Properties object
        """
        self.properties = properties
        self.mode = properties.mode

    def handle_events(self) -> Command:
        """
        Handle pygame GUI events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.command.quit = True
            if event.type == pygame.KEYDOWN:
                self.handle_key_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_event()
        return self.command

    def is_click_on_agents_row(self, x: int, y: int, i: int) -> bool:
        """
        Check if the click is on an agent's row.

        Args:
            x: int, x-coordinate of the click
            y: int, y-coordinate of the click
            i: int, index of the row
        """
        return (
            x >= self.properties.display_grid_width
            and (i + 1) * c.GUI_ROW_HEIGHT <= y < (i + 2) * c.GUI_ROW_HEIGHT
        )

    def toggle_player_fov(self):
        agents = self.properties.game.agents
        agent_fov = self.properties.agent_fov

        x, y = pygame.mouse.get_pos()
        for i, agent in enumerate(agents):
            if self.is_click_on_agents_row(x, y, i):
                agent_fov[agent] = not agent_fov[agent]
                break

    @abstractmethod
    def handle_key_event(self, event: Event) -> Command:
        raise NotImplementedError

    @abstractmethod
    def handle_mouse_event(self):
        raise NotImplementedError


class ReplayEventHandler(EventHandler):
    def __init__(self, properties: Properties):
        super().__init__(properties)
        self.command = ReplayCommand()

    def handle_key_event(self, event: Event) -> ReplayCommand:
        match event.key:
            case Keybindings.Q.value:
                self.command.quit = True
            case Keybindings.RIGHT.value:
                self.command.speed_change = 2.0
            case Keybindings.LEFT.value:
                self.command.speed_change = 0.5
            case Keybindings.SPACE.value:
                self.command.pause_toggle = True
            case Keybindings.R.value:
                self.command.restart = True
            case Keybindings.H.value:
                self.command.frame_change = -1
            case Keybindings.L.value:
                self.command.frame_change = 1
        return self.command

    def handle_mouse_event(self) -> None:
        """
        Handle mouse clicks in replay mode.
        """
        self.toggle_player_fov()


class GameEventHandler(EventHandler):
    def __init__(self, properties: Properties):
        super().__init__(properties)
        self.command = GameCommand()

    def handle_key_event(self, event: Event) -> GameCommand:
        raise NotImplementedError

    def handle_mouse_event(self) -> None:
        self.toggle_player_fov()


class TrainEventHandler(EventHandler):
    def __init__(self, properties: Properties):
        super().__init__(properties)
        self.command = TrainCommand()

    def handle_key_event(self, event: Event) -> TrainCommand:
        if event.key == Keybindings.Q.value:
            self.command.quit = True
        return self.command

    def handle_mouse_event(self) -> None:
        self.toggle_player_fov()
