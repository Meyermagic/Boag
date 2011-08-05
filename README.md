# Boag

Boag is a simple AI competition game. Started as a one-night project for fun, it has been expanded and improved a bit to its current state.


## Rules

The competition occurs between two teams of n players, on a square grid of arbitrary size. 

A team wins when all players on the opposing team are killed.
The game stalemates when no ammo is left, or if no living players are left.

Each player can perform one of eight actions in per turn, and moves are applied simultaneously for all players.

The eight available moves are split into two types ("fire" and "move"), each with four directions (up, down, left, right).

Firing decreases the player's available ammo by one, and spawns a new bullet moving at one square per turn in the indicated direction.

Any player occupying the same square as a bullet at the end of a turn is declared "dead" and removed from the board.

## Restrictions

Each player has access to the position, type, and team association of every entity on the board at the start of the turn, and can use this information to decide on an appropriate action.

In addition, each player has access to an internal "states" dictionary, which persists between turns, and another states dictionary associated with its team and shared by all players on the team.

No special synchonization occurs for the team dictionary. Currently, if a player modifies the team dictionary during the computation of an action for the turn, those changes will be visible to the other players on the team during the same turn. This may be changed.
