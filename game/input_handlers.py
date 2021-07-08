from __future__ import annotations

from typing import Optional

import tcod

import game.actions

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


class EventHandler(tcod.event.EventDispatch[game.actions.Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[game.actions.Action]:
        raise SystemExit(0)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[game.actions.Action]:
        key = event.sym

        if event.mod & tcod.event.Modifier.CTRL and key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            return game.actions.Move(dx=dx, dy=dy)

        if event.mod & tcod.event.Modifier.ALT and key in MOVE_KEYS_DIAG:
            dx, dy = MOVE_KEYS_DIAG[key]
            return game.actions.Move(dx=dx, dy=dy)

        # And Escape
        elif key == tcod.event.K_ESCAPE:
            raise SystemExit(0)

        return None
