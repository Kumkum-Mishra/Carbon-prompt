"use client";

import { useEffect, useId, useMemo, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import toast from "react-hot-toast";
import { Check, Copy, Loader2, Sparkles, Wand2 } from "lucide-react";
import { fadeInUp } from "@/design/motion";
import { samplePrompts } from "@/data/analyze";
import { cn } from "@/utils/cn";
import {
  diffWords,
  optimizedSideSegments,
  originalSideSegments,
} from "@/utils/wordDiff";
import PromptDiffView from "./PromptDiffView";

interface PromptInputProps {
  onSubmit: (prompt: string) => void;
  isLoading: boolean;
  /** Latest optimized prompt from analysis; updates the right panel. */
  optimizedPrompt?: string | null;
}

export default function PromptInput({
  onSubmit,
  isLoading,
  optimizedPrompt = null,
}: PromptInputProps) {
  const [prompt, setPrompt] = useState("");
  const [validationError, setValidationError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [isEditing, setIsEditing] = useState(true);
  const textareaId = useId();

  const trimmed = prompt.trim();
  const isEmpty = trimmed.length === 0;
  const hasOptimized = Boolean(optimizedPrompt && optimizedPrompt.length > 0);

  // When a new optimized result arrives, show the diff view on the left.
  useEffect(() => {
    if (hasOptimized) {
      setIsEditing(false);
      setCopied(false);
    }
  }, [optimizedPrompt, hasOptimized]);

  const segments = useMemo(() => {
    if (!hasOptimized || !optimizedPrompt) return [];
    return diffWords(prompt, optimizedPrompt);
  }, [prompt, optimizedPrompt, hasOptimized]);

  const originalSegments = useMemo(
    () => originalSideSegments(segments),
    [segments]
  );
  const optimizedSegments = useMemo(
    () => optimizedSideSegments(segments),
    [segments]
  );

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (isEmpty) {
      setValidationError("Please enter a prompt.");
      return;
    }
    setValidationError(null);
    onSubmit(trimmed);
  };

  const handleCopy = async () => {
    if (!optimizedPrompt) return;
    try {
      await navigator.clipboard.writeText(optimizedPrompt);
      setCopied(true);
      toast.success("Optimized prompt copied!");
      setTimeout(() => setCopied(false), 2500);
    } catch {
      toast.error("Could not copy prompt.");
    }
  };

  const showOriginalDiff = hasOptimized && !isEditing && !isLoading;

  return (
    <motion.form
      variants={fadeInUp}
      onSubmit={handleSubmit}
      className={cn(
        "rounded-panel border border-slate-200 bg-white p-5 shadow-card transition-shadow duration-200 sm:p-6",
        "focus-within:border-emerald-300 focus-within:shadow-md"
      )}
    >
      <div className="grid items-stretch gap-4 lg:grid-cols-2">
        {/* Left: Original Prompt */}
        <div className="flex min-h-[200px] flex-col rounded-card border border-slate-200 bg-slate-50/50 p-4 sm:min-h-[220px]">
          <div className="flex items-center justify-between gap-2">
            <label
              htmlFor={textareaId}
              className="text-sm font-semibold text-slate-900"
            >
              Original Prompt
            </label>
            <div className="flex items-center gap-2">
              <span className="text-xs tabular-nums text-slate-500">
                {prompt.length.toLocaleString()} chars
              </span>
              {showOriginalDiff && (
                <button
                  type="button"
                  onClick={() => setIsEditing(true)}
                  className="text-xs font-medium text-emerald-700 transition-colors hover:text-emerald-800 focus-ring rounded-sm"
                >
                  Edit
                </button>
              )}
            </div>
          </div>

          <div className="relative mt-3 min-h-0 flex-1">
            {showOriginalDiff ? (
              <div className="h-full max-h-48 overflow-y-auto rounded-inner border border-slate-200 bg-white px-3.5 py-3">
                <PromptDiffView segments={originalSegments} side="original" />
              </div>
            ) : (
              <textarea
                id={textareaId}
                rows={3}
                value={prompt}
                onChange={(e) => {
                  setPrompt(e.target.value);
                  if (validationError) setValidationError(null);
                }}
                onBlur={() => {
                  if (hasOptimized && prompt.trim()) {
                    setIsEditing(false);
                  }
                }}
                placeholder="e.g. Write CNN code using PyTorch."
                aria-invalid={validationError ? true : undefined}
                className={cn(
                  "h-full min-h-[7.5rem] w-full resize-y rounded-inner border bg-white px-3.5 py-3 text-[15px] leading-[1.65] text-slate-900 placeholder:text-slate-400 transition-colors duration-150",
                  "focus:outline-none focus:ring-2 focus:ring-emerald-100 focus:border-emerald-500",
                  validationError
                    ? "border-red-300 focus:border-red-500 focus:ring-red-100"
                    : "border-slate-300",
                  "disabled:cursor-not-allowed disabled:bg-slate-50 disabled:text-slate-400"
                )}
                disabled={isLoading}
              />
            )}
          </div>
        </div>

        {/* Right: Optimized Prompt */}
        <div className="flex min-h-[200px] flex-col rounded-card border border-emerald-100 bg-emerald-50/40 p-4 sm:min-h-[220px]">
          <div className="sticky top-0 z-10 flex items-center justify-between gap-2 bg-emerald-50/40 pb-1">
            <p className="text-sm font-semibold text-slate-900">
              Optimized Prompt
            </p>
            {hasOptimized && (
              <button
                type="button"
                onClick={handleCopy}
                className="inline-flex items-center gap-1.5 rounded-inner border border-emerald-200 bg-white px-3 py-1.5 text-xs font-semibold text-emerald-700 shadow-sm transition-all duration-150 hover:-translate-y-0.5 hover:bg-emerald-50 focus-ring active:translate-y-0"
                aria-label="Copy optimized prompt"
              >
                <AnimatePresence mode="wait" initial={false}>
                  {copied ? (
                    <motion.span
                      key="copied"
                      initial={{ opacity: 0, scale: 0.85 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.85 }}
                      transition={{ duration: 0.15 }}
                      className="inline-flex items-center gap-1.5"
                    >
                      <Check className="h-3.5 w-3.5" strokeWidth={2} />
                      Copied
                    </motion.span>
                  ) : (
                    <motion.span
                      key="copy"
                      initial={{ opacity: 0, scale: 0.85 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.85 }}
                      transition={{ duration: 0.15 }}
                      className="inline-flex items-center gap-1.5"
                    >
                      <Copy className="h-3.5 w-3.5" strokeWidth={1.75} />
                      Copy Optimized Prompt
                    </motion.span>
                  )}
                </AnimatePresence>
              </button>
            )}
          </div>

          <div className="mt-3 min-h-0 flex-1">
            {isLoading ? (
              <div className="flex h-full min-h-[7.5rem] flex-col items-center justify-center gap-2 rounded-inner border border-dashed border-emerald-200 bg-white/70 px-4 text-center">
                <Loader2 className="h-5 w-5 animate-spin text-emerald-600" />
                <p className="text-sm text-slate-500">Optimizing your prompt…</p>
              </div>
            ) : hasOptimized && optimizedPrompt ? (
              <div className="h-full max-h-48 overflow-y-auto rounded-inner border border-emerald-100 bg-white px-3.5 py-3">
                <PromptDiffView
                  segments={optimizedSegments}
                  side="optimized"
                />
              </div>
            ) : (
              <div className="flex h-full min-h-[7.5rem] flex-col items-center justify-center gap-2 rounded-inner border border-dashed border-slate-200 bg-white/80 px-4 text-center">
                <Wand2 className="h-5 w-5 text-slate-300" strokeWidth={1.5} />
                <p className="text-sm text-slate-500">
                  Your optimized prompt will appear here after analysis.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="mt-3 flex min-h-[20px] items-center justify-between">
        <p className="text-xs text-slate-500">
          Word-level changes highlight removals in red and additions in green.
        </p>
        {validationError && (
          <span role="alert" className="text-sm font-medium text-red-600">
            {validationError}
          </span>
        )}
      </div>

      <div className="mt-4">
        <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
          Try an example
        </p>
        <div className="mt-2 flex flex-wrap gap-2">
          {samplePrompts.map((example) => (
            <button
              key={example}
              type="button"
              disabled={isLoading}
              onClick={() => {
                setPrompt(example);
                setIsEditing(true);
                setValidationError(null);
              }}
              className="max-w-full truncate rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-medium text-slate-600 transition-colors duration-150 hover:border-emerald-300 hover:bg-emerald-50 hover:text-emerald-700 focus-ring disabled:cursor-not-allowed disabled:opacity-50"
              title={example}
            >
              {example.length > 48 ? `${example.slice(0, 48)}…` : example}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-5 flex justify-end">
        <button
          type="submit"
          disabled={isLoading || isEmpty}
          className="group inline-flex min-h-[48px] items-center justify-center gap-2 rounded-inner bg-emerald-600 px-6 py-3 text-sm font-semibold text-white transition-all duration-150 hover:-translate-y-0.5 hover:bg-emerald-500 focus-ring disabled:cursor-not-allowed disabled:translate-y-0 disabled:bg-slate-300"
        >
          {isLoading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              Analyzing…
            </>
          ) : (
            <>
              <Sparkles className="h-4 w-4" />
              Analyze Prompt
            </>
          )}
        </button>
      </div>
    </motion.form>
  );
}
