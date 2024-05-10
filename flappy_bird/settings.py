"""Game settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Game settings."""

    FPS: int = 60
    MAX_SCORE: int = 1000

    # Floor
    FLOOR_VELOCITY: int = 5
    FLOOR_STARTING_POSITION: int = 500

    # Pipe
    PIPE_MAX_NUM: int = 500
    PIPE_VERTICAL_GAP: int = 200
    PIPE_HORIZONTAL_GAP: int = 200
    PIPE_VELOCITY: int = 5
    PIPE_TOP_MIN_HEIGHT: int = 100
    PIPE_TOP_MAX_HEIGHT: int = 300
    PIPE_STARTING_POSITION: int = 500

    # Bird
    BIRD_MAX_UP_ANGLE: int = 35
    BIRD_MAX_DOWN_ANGLE: int = -90
    BIRD_MIN_INCREMENTAL_ANGLE: int = 5
    BIRD_ANGULAR_ACCELERATION: float = 0.3
    BIRD_ANIMATION_TIME: int = 1
    BIRD_JUMP_VELOCITY: int = -8
    BIRD_ACCELERATION: int = 3
    BIRD_MAX_DISPLACEMENT: int = 12
    BIRD_STARTING_X_POSITION: int = 150
    BIRD_STARTING_Y_POSITION: int = 250

    # Neat
    GENERATION: int = 0
    MAX_GEN: int = 50
    THRESHOLD_TO_JUMP: float = 0.8
    FAILED_PUNISHMENT: int = 10


settings = Settings()
