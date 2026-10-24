"use client";

import { useId, useState } from "react";
import { motion } from "framer-motion";
import { ChevronDown, NotebookText } from "lucide-react";
import IconBox from "@/components/ui/IconBox";
import { fadeInUp, staggerTight, viewportOnce } from "@/design/motion";
import { researchNotes } from "@/data/datasets";
import { cn } from "@/utils/cn";

function NoteItem({
  title,
  body,
}: {
  title: string;
  body: string;
}) {
  const [open, setOpen] = useState(false);
  const panelId = useId();
  const buttonId = useId();

  return (
    <motion.div
      variants={fadeInUp}
      className="rounded-inner border border-slate-200 bg-white"
    >
      <button
        id={buttonId}
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        aria-expanded={open}
        aria-controls={panelId}
        className="flex w-full min-h-[44px] items-center justify-between gap-3 px-4 py-3.5 text-left focus-ring rounded-inner"
      >
        <span className="text-sm font-semibold text-slate-900">{title}</span>
        <ChevronDown
          className={cn(
            "h-4 w-4 shrink-0 text-slate-400 transition-transform duration-200",
            open && "rotate-180"
          )}
          strokeWidth={1.75}
          aria-hidden
        />
      </button>
      {open && (
        <p
          id={panelId}
          role="region"
          aria-labelledby={buttonId}
          className="px-4 pb-4 text-sm leading-[1.65] text-slate-600"
        >
          {body}
        </p>
      )}
    </motion.div>
  );
}

export default function ResearchNotes() {
  return (
    <motion.section
      initial="hidden"
      whileInView="visible"
      viewport={viewportOnce}
      variants={staggerTight()}
      className="rounded-card border border-slate-200 bg-slate-50 p-6 sm:p-8"
    >
      <motion.div variants={fadeInUp} className="flex items-center gap-2.5">
        <IconBox icon={NotebookText} className="bg-white" />
        <div>
          <h2 className="text-xl font-bold text-slate-900">Research Notes</h2>
          <p className="text-sm text-slate-600">
            Transparency notes on where this data comes from and how it is used.
          </p>
        </div>
      </motion.div>

      <div className="mt-5 space-y-2.5">
        {researchNotes.map((note) => (
          <NoteItem
            key={note.title}
            title={note.title}
            body={note.body}
          />
        ))}
      </div>
    </motion.section>
  );
}
