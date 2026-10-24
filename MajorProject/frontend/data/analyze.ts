import type { LucideIcon } from "lucide-react";
import { Cpu, Gauge, Search, Wand2 } from "lucide-react";
import { LOADING_MESSAGES } from "@/utils/constants";

export const samplePrompts: string[] = [
  "Write CNN code using PyTorch.",
  "Can you please explain in great detail, with many examples, how neural networks work and also discuss all their applications?",
  "Summarize the key findings of this research paper in three bullet points.",
  "Act as a senior backend engineer and review this API design for scalability issues.",
];

export interface PipelineStepMeta {
  icon: LucideIcon;
  label: string;
}

export const pipelineSteps: PipelineStepMeta[] = LOADING_MESSAGES.map(
  (label, index) => ({
    label,
    icon: [Search, Gauge, Wand2, Cpu][index] ?? Search,
  })
);
