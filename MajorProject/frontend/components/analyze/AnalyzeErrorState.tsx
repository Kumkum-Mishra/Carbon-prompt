"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { AlertCircle, ExternalLink, RotateCcw } from "lucide-react";
import Button from "@/components/ui/Button";
import { fadeInUp } from "@/design/motion";
import { API_BASE_URL } from "@/services/api";

interface AnalyzeErrorStateProps {
  message: string;
  details?: string;
  onRetry?: () => void;
}

export default function AnalyzeErrorState({
  message,
  details,
  onRetry,
}: AnalyzeErrorStateProps) {
  const [showDetails, setShowDetails] = useState(false);

  return (
    <motion.div
      variants={fadeInUp}
      role="alert"
      className="rounded-card border border-red-200 bg-red-50 p-5"
    >
      <div className="flex gap-3">
        <AlertCircle className="mt-0.5 h-5 w-5 shrink-0 text-red-600" aria-hidden />
        <div className="flex-1">
          <p className="font-medium text-red-800">{message}</p>

          {details && (
            <div className="mt-1">
              <button
                type="button"
                onClick={() => setShowDetails((prev) => !prev)}
                className="text-xs font-medium text-red-600 underline-offset-2 hover:underline focus-ring rounded-sm"
              >
                {showDetails ? "Hide technical details" : "Show technical details"}
              </button>
              {showDetails && (
                <p className="mt-1 rounded-inner bg-red-100/70 p-2 text-xs text-red-700">
                  {details}
                </p>
              )}
            </div>
          )}

          <div className="mt-3 flex flex-wrap items-center gap-4">
            {onRetry && (
              <Button variant="danger" size="sm" onClick={onRetry}>
                <RotateCcw className="h-3.5 w-3.5" aria-hidden />
                Try again
              </Button>
            )}
            <a
              href={`${API_BASE_URL}/health`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 rounded-sm text-xs font-medium text-red-700 transition-colors duration-150 hover:text-red-800 focus-ring"
            >
              Check backend status
              <ExternalLink className="h-3 w-3" aria-hidden />
            </a>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
