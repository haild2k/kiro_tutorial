# Project Structure

## Current State

The project is in the **requirements phase** — no source code exists yet. Only spec documents are present.

## Spec Directory

```
.kiro/
  specs/
    tic-tac-toe-4x4/
      .config.kiro       # Spec metadata (workflow type, spec ID)
      requirements.md    # Feature requirements in Vietnamese
      design.md          # (planned) Technical design document
      tasks.md           # (planned) Implementation task list
  steering/
    product.md           # Product overview and goals
    tech.md              # Tech stack and architecture components
    structure.md         # This file
```

## Expected Source Structure

Once implementation begins, organize code around the logical components defined in requirements:

```
src/
  board.{ext}            # Board state and cell management
  renderer.{ext}         # Terminal output and ANSI color formatting
  input_handler.{ext}    # Stdin reading and input validation
  win_checker.{ext}      # Win/draw condition logic
  game.{ext}             # Game loop, turn management, play-again flow
  main.{ext}             # Entry point
tests/
  board_test.{ext}
  win_checker_test.{ext}
  input_handler_test.{ext}
  game_test.{ext}
```

## Conventions

- One component per file, named to match the logical component
- Keep game logic (Win_Checker, Board) separate from I/O (Renderer, Input_Handler)
- Entry point (`main`) should only wire components together and start the game loop
- No global mutable state — pass board/game state explicitly between components
