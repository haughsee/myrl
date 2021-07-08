from __future__ import annotations

from typing import Optional, Union

import tcod

import game.actions
import game.engine
import game.rendering

MOVE_KEYS = {

    # Emacs keys.
    tcod.event.K_b: (-1, 0),
    tcod.event.K_p: (0, -1),
    tcod.event.K_n: (0, 1),
    tcod.event.K_f: (1, 0),
}

MOVE_KEYS_DIAG = {

    tcod.event.K_b: (-1, -1),
    tcod.event.K_p: (1, -1),
    tcod.event.K_n: (-1, 1),
    tcod.event.K_f: (1, 1),
}

ActionOrHandler = Union["game.actions.Action", "EventHandler"]
"""An event handler return value which can trigger an action or switch active handlers.

If a handler is returned then it will become the active handler for future events.
If an action is returned it will be attempted and if it's valid then
MainGameEventHandler will become the active handler.
"""
class EventHandler(tcod.event.EventDispatch[ActionOrHandler]):
    def __init__(self, engine: game.engine.Engine) -> None:
        super().__init__()
        self.engine = engine

    def handle_events(self, event: tcod.event.Event) -> EventHandler:
        """Handle an event, perform any actions, then return the next active event handler."""
        action_or_state = self.dispatch(event)
        if isinstance(action_or_state, EventHandler):
            return action_or_state
        elif isinstance(action_or_state, game.actions.Action):
            return self.handle_action(action_or_state)
        return self

    def handle_action(self, action: game.actions.Action) -> EventHandler:
        """Handle actions returned from event methods."""
        action.perform()
        return self

    def ev_quit(self, event: tcod.event.Quit) -> Optional[game.actions.Action]:
        raise SystemExit(0)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[game.actions.Action]:
        key = event.sym

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            return game.actions.Move(self.engine.player, dx=dx, dy=dy)
        elif key == tcod.event.K_ESCAPE:
            raise SystemExit(0)

        return None

    def on_render(self, console: tcod.Console) -> None:
        game.rendering.render_map(console, self.engine.game_map)
