# Tech Stack

## Language & Runtime

- **Language**: To be determined (project is in requirements phase)
- The game runs entirely in the terminal — no GUI, no web, no external services

## Expected Characteristics

Based on the requirements, the implementation should:
- Support ANSI escape codes for terminal color output
- Read from stdin for player input
- Have no external runtime dependencies (self-contained CLI program)

## Architecture Components

The requirements define these logical components:

| Component | Responsibility |
|---|---|
| `Board` | 4×4 grid state, cell numbering 1–16 |
| `Renderer` | Terminal output, ANSI color formatting, board display |
| `Input_Handler` | Stdin reading, input validation, error prompting |
| `Win_Checker` | Win/draw condition evaluation after each move |
| `Game` | Turn management, game loop, play-again flow |

## Common Commands

> To be filled in once the language and build system are chosen.

```
# Example placeholders — update when stack is decided
build:   <build command>
run:     <run command>
test:    <test command>
```
