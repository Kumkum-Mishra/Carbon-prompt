"""Training configuration for the prompt optimization model."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "prompt_optimization_dataset.csv"
OUTPUT_DIR = PROJECT_ROOT / "models" / "greenprompt_model"
LOGS_DIR = OUTPUT_DIR / "logs"

MODEL_NAME = "google/flan-t5-small"
TASK_PREFIX = "Simplify this prompt while preserving meaning: "

TRAIN_RATIO = 0.8
VAL_RATIO = 0.1
TEST_RATIO = 0.1
RANDOM_SEED = 42

MAX_INPUT_LENGTH = 128
MAX_TARGET_LENGTH = 96

NUM_EPOCHS = 3
BATCH_SIZE = 16
EVAL_BATCH_SIZE = 16
LEARNING_RATE = 3e-4
WEIGHT_DECAY = 0.01
WARMUP_RATIO = 0.06
GRADIENT_ACCUMULATION_STEPS = 1

SAVE_TOTAL_LIMIT = 2
LOGGING_STEPS = 100
EVAL_STRATEGY = "epoch"
SAVE_STRATEGY = "epoch"
LOAD_BEST_MODEL_AT_END = True
METRIC_FOR_BEST_MODEL = "eval_loss"
GREATER_IS_BETTER = False

FP16 = False
