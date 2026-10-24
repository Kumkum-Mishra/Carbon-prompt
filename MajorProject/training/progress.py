"""Progress bars and callbacks for training visibility."""

from __future__ import annotations

import time
from typing import Any

from tqdm.auto import tqdm
from transformers import TrainerCallback, TrainerControl, TrainerState, TrainingArguments


def format_duration(seconds: float) -> str:
    seconds = max(0, int(seconds))
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}h {minutes}m {secs}s"
    if minutes:
        return f"{minutes}m {secs}s"
    return f"{secs}s"


class PhaseProgress:
    """Single tqdm bar for a pipeline phase (preprocess, train, eval, export)."""

    def __init__(self, total: int, desc: str) -> None:
        self.bar = tqdm(
            total=total,
            desc=desc,
            unit="step",
            dynamic_ncols=True,
            leave=True,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
        )

    def update(self, n: int = 1) -> None:
        self.bar.update(n)

    def close(self) -> None:
        self.bar.close()


class TrainingProgressCallback(TrainerCallback):
    """Epoch + overall training bars with loss and ETA."""

    def __init__(self, total_steps: int, num_epochs: int) -> None:
        self.total_steps = total_steps
        self.num_epochs = num_epochs
        self.overall_bar: tqdm | None = None
        self.epoch_bar: tqdm | None = None
        self.epoch_start_time = 0.0
        self.train_start_time = 0.0

    def on_train_begin(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs: Any,
    ) -> None:
        self.train_start_time = time.time()
        tqdm.write("")
        tqdm.write("=" * 72)
        tqdm.write(
            f"Training started | epochs={self.num_epochs} | steps={self.total_steps} | "
            f"batch_size={args.per_device_train_batch_size}"
        )
        tqdm.write("=" * 72)

        self.overall_bar = tqdm(
            total=self.total_steps,
            desc="Overall",
            unit="step",
            position=0,
            leave=True,
            dynamic_ncols=True,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
        )

    def on_epoch_begin(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs: Any,
    ) -> None:
        self.epoch_start_time = time.time()
        steps_per_epoch = max(1, self.total_steps // self.num_epochs)
        if self.epoch_bar is not None:
            self.epoch_bar.close()

        self.epoch_bar = tqdm(
            total=steps_per_epoch,
            desc=f"Epoch {int(state.epoch) + 1}/{self.num_epochs}",
            unit="step",
            position=1,
            leave=False,
            dynamic_ncols=True,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
        )

    def on_log(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        logs: dict[str, float] | None = None,
        **kwargs: Any,
    ) -> None:
        if not logs:
            return

        parts = []
        if "loss" in logs:
            parts.append(f"loss={logs['loss']:.4f}")
        if "learning_rate" in logs:
            parts.append(f"lr={logs['learning_rate']:.2e}")
        if "eval_loss" in logs:
            parts.append(f"eval_loss={logs['eval_loss']:.4f}")

        if parts and state.global_step > 0:
            elapsed = time.time() - self.train_start_time
            done_ratio = state.global_step / max(1, self.total_steps)
            eta = (elapsed / done_ratio - elapsed) if done_ratio > 0 else 0
            tqdm.write(
                f"[step {state.global_step}/{self.total_steps}] "
                f"{', '.join(parts)} | elapsed={format_duration(elapsed)} | eta={format_duration(eta)}"
            )

    def on_step_end(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs: Any,
    ) -> None:
        if self.overall_bar is not None:
            self.overall_bar.update(1)
        if self.epoch_bar is not None:
            self.epoch_bar.update(1)

    def on_epoch_end(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs: Any,
    ) -> None:
        epoch_elapsed = time.time() - self.epoch_start_time
        tqdm.write(
            f"Epoch {int(state.epoch)}/{self.num_epochs} finished in {format_duration(epoch_elapsed)}"
        )
        if self.epoch_bar is not None:
            self.epoch_bar.close()
            self.epoch_bar = None

    def on_train_end(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs: Any,
    ) -> None:
        total_elapsed = time.time() - self.train_start_time
        if self.epoch_bar is not None:
            self.epoch_bar.close()
        if self.overall_bar is not None:
            self.overall_bar.close()
        tqdm.write("=" * 72)
        tqdm.write(f"Training finished in {format_duration(total_elapsed)}")
        tqdm.write("=" * 72)
