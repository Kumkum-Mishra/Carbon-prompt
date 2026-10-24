"use client";

import { useCallback, useState } from "react";
import toast from "react-hot-toast";
import { ApiServiceError, processPrompt } from "@/services/api";
import type { ProcessSuccessResponse } from "@/types/api";

interface UseProcessPromptResult {
  result: ProcessSuccessResponse | null;
  error: string | null;
  errorDetails: string | null;
  isLoading: boolean;
  loadingStep: number;
  lastPrompt: string | null;
  submit: (prompt: string) => Promise<void>;
  retry: () => Promise<void>;
  reset: () => void;
}

export function useProcessPrompt(): UseProcessPromptResult {
  const [result, setResult] = useState<ProcessSuccessResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [errorDetails, setErrorDetails] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);
  const [lastPrompt, setLastPrompt] = useState<string | null>(null);

  const submit = useCallback(async (prompt: string) => {
    setIsLoading(true);
    setError(null);
    setErrorDetails(null);
    setResult(null);
    setLoadingStep(0);
    setLastPrompt(prompt);

    const stepInterval = setInterval(() => {
      setLoadingStep((prev) => Math.min(prev + 1, 3));
    }, 800);

    try {
      const response = await processPrompt(prompt);
      if (!response.success) {
        setError(response.message);
        setErrorDetails(response.details ?? null);
        return;
      }
      setResult(response);
      toast.success("Analysis complete!");
    } catch (err) {
      const message =
        err instanceof ApiServiceError
          ? err.message
          : "Unexpected server error. Please try again.";
      setError(message);
      setErrorDetails(err instanceof ApiServiceError ? err.details ?? null : null);
    } finally {
      clearInterval(stepInterval);
      setIsLoading(false);
      setLoadingStep(3);
    }
  }, []);

  const retry = useCallback(async () => {
    if (lastPrompt) {
      await submit(lastPrompt);
    }
  }, [lastPrompt, submit]);

  const reset = useCallback(() => {
    setResult(null);
    setError(null);
    setErrorDetails(null);
    setIsLoading(false);
    setLoadingStep(0);
  }, []);

  return {
    result,
    error,
    errorDetails,
    isLoading,
    loadingStep,
    lastPrompt,
    submit,
    retry,
    reset,
  };
}
