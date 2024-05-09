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
    BIRD_MIN_INCREMENTAL_ANGLE = 5
    BIRD_ANGULAR_ACCELERATION = 0.3
    BIRD_ANIMATION_TIME: int = 1
    BIRD_JUMP_VELOCITY = -8
    BIRD_ACCELERATION = 3
    BIRD_MAX_DISPLACEMENT = 12
    BIRD_STARTING_X_POSITION = 150
    BIRD_STARTING_Y_POSITION = 250

    # Neat
    GENERATION = 0
    MAX_GEN = 50
    PROB_THRESHOLD_TO_JUMP = 0.8
    FAILED_PUNISHMENT = 10


settings = Settings()
