# Chess Rules + Playing Engine

## Todo

### general
- [x] ~~Fix broken bishop jumping over pawns~~
- [ ] Clean code up. Thing is a mess.
- [ ] Refactor LegalMoveStrategy / legal move generation. Thing is a mess.
- [ ] Finish move legality (check, en-passant, queening, etc)
- [ ] Import QOL for players.

### engine
- [x] Implement actual engine.
- [ ] Use iterative deepening
- [ ] Better dynamic programming
- [ ] Make engine faster
- [ ] Profile code

## todo comments in source

```
[2017-06-10 23:40:18] 
~/git/chess-engine(master*) λ grep TODO . -r -n >> README.md

./src/engine.py:44:        # TODO: continue implementing
./src/engine.py:54:        #TODO
./src/engine.py:88:    # TODO: implement positional evaluations
./src/engine.py:97:    # TODO
./src/engine.py:101:        # TODO
./src/game.py:46:        # TODO: break this out into a Computer class
./src/move.py:128:#TODO: lots of repetition here. Use mixins. Clean it up.
```
