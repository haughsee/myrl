from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        ## Using Emacs arrow-keys

        if  event.mod & tcod.event.Modifier.CTRL and key == tcod.event.K_p:
            action = MovementAction(dx=0, dy=-1)
        elif event.mod & tcod.event.Modifier.CTRL and key == tcod.event.K_n:
            action = MovementAction(dx=0, dy=1)
        elif event.mod & tcod.event.Modifier.CTRL and key == tcod.event.K_b:
            action = MovementAction(dx=-1, dy=0)
        elif event.mod & tcod.event.Modifier.CTRL and key == tcod.event.K_f:
            action = MovementAction(dx=1, dy=0)

        ## And now for the alt-ernatives
            
        elif event.mod & tcod.event.Modifier.ALT and key == tcod.event.K_f:
            action = MovementAction(dx=1, dy=1)
        elif event.mod & tcod.event.Modifier.ALT and key == tcod.event.K_b:
            action = MovementAction(dx=-1, dy=-1)
        elif event.mod & tcod.event.Modifier.ALT and key == tcod.event.K_n:
            action = MovementAction(dx=-1, dy=1)
        elif event.mod & tcod.event.Modifier.ALT and key == tcod.event.K_p:
            action = MovementAction(dx=1, dy=-1)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        # No valid key was pressed
        return action
