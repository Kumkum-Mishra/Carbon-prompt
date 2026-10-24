"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip as RechartsTooltip,
  XAxis,
  YAxis,
} from "recharts";
import { motion } from "framer-motion";
import {
  Boxes,
  Clock3,
  Coins,
  Cpu,
  Database,
  Gauge,
  Layers,
  Zap,
} from "lucide-react";
import DatasetCard from "@/components/datasets/DatasetCard";
import DatasetSectionHeader from "@/components/datasets/DatasetSectionHeader";
import KPICard from "@/components/datasets/KPICard";
import ResearchNotes from "@/components/datasets/ResearchNotes";
import RevealSection from "@/components/home/RevealSection";
import PageContainer from "@/components/layout/PageContainer";
import { fadeInUp, staggerTight, viewportOnce } from "@/design/motion";
import datasetStats from "@/data/dataset-stats.json";
import {
  groupPromptTypeDistribution,
  PROMPT_TYPE_CHART_COLORS,
} from "@/utils/promptTypeChart";

const CHART_TOOLTIP_STYLE = {
  fontSize: 12,
  borderRadius: 10,
  border: "1px solid #e2e8f0",
};

export default function DatasetsPage() {
  const { carbonPromptDataset, modelDataset } = datasetStats;

  const promptTypeData = groupPromptTypeDistribution(
    carbonPromptDataset.promptTypeDistribution
  );

  const taskTypeData = Object.entries(carbonPromptDataset.taskTypeDistribution)
    .map(([name, value]) => ({ name, value }))
    .slice(0, 8);

  const modelCategoryData = Object.entries(
    modelDataset.categoryDistribution
  ).map(([name, value]) => ({ name, value }));

  const promptTypeCount = Object.keys(
    carbonPromptDataset.promptTypeDistribution
  ).length;
  const modelCategoryCount = modelDataset.categories.length;

  return (
    <PageContainer
      title="Datasets"
      subtitle="Statistics and distributions from the GreenPrompt AI reference datasets."
    >
      <div className="space-y-12">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={viewportOnce}
          variants={staggerTight()}
          className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4"
        >
            <KPICard
              icon={Database}
              label="Total Prompts"
              value={carbonPromptDataset.totalPrompts}
              description="Rows in the carbon prompt dataset"
            />
            <KPICard
              icon={Cpu}
              label="Total Models"
              value={modelDataset.totalModels}
              description="Rows in the model dataset"
            />
            <KPICard
              icon={Layers}
              label="Prompt Types"
              value={promptTypeCount}
              description="Distinct prompting strategies"
            />
            <KPICard
              icon={Boxes}
              label="Model Categories"
              value={modelCategoryCount}
              description="Text, Coding, Vision, Image, Search"
            />
          </motion.div>

          <RevealSection className="space-y-6">
            <DatasetSectionHeader
              badge="Carbon Prompt Dataset"
              title="Prompt type & task distribution"
              description="How prompting strategies and task categories are represented across the 1,000-row carbon prompt dataset that calibrates the Green Carbon Score."
            />

            <div className="grid gap-5 lg:grid-cols-2">
              <DatasetCard
                icon={Layers}
                title="Prompt Type Distribution"
                description="Distribution of prompting strategies in the carbon prompt dataset."
              >
                <ResponsiveContainer width="100%" height={320}>
                  <PieChart>
                    <Pie
                      data={promptTypeData}
                      dataKey="value"
                      nameKey="name"
                      cx="50%"
                      cy="45%"
                      outerRadius={85}
                      labelLine={{ stroke: "#94a3b8", strokeWidth: 1 }}
                      label={({ name, percent }) =>
                        `${name} (${(percent * 100).toFixed(0)}%)`
                      }
                      style={{ fontSize: 11, fontWeight: 500 }}
                    >
                      {promptTypeData.map((entry, index) => (
                        <Cell
                          key={entry.name}
                          fill={PROMPT_TYPE_CHART_COLORS[index]}
                          stroke="#ffffff"
                          strokeWidth={1}
                        />
                      ))}
                    </Pie>
                    <RechartsTooltip
                      formatter={(value: number) => [value, "Prompts"]}
                      contentStyle={CHART_TOOLTIP_STYLE}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </DatasetCard>

              <DatasetCard
                icon={Gauge}
                title="Task Type Distribution"
                description="Breakdown of prompt task categories."
              >
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={taskTypeData} layout="vertical" margin={{ left: 24 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis type="number" tick={{ fontSize: 11, fill: "#64748b" }} />
                    <YAxis
                      dataKey="name"
                      type="category"
                      width={130}
                      tick={{ fontSize: 11, fill: "#64748b" }}
                    />
                    <RechartsTooltip contentStyle={CHART_TOOLTIP_STYLE} />
                    <Bar dataKey="value" fill="#16a34a" radius={[0, 6, 6, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </DatasetCard>

              <DatasetCard
                icon={Zap}
                title="Dataset Averages"
                description="Aggregate figures used as the Green Carbon Score baseline."
                span="wide"
              >
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                  <div className="rounded-[10px] bg-slate-50 p-4">
                    <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                      Average Token Count
                    </p>
                    <p className="mt-1 text-2xl font-bold tabular-nums text-slate-900">
                      {carbonPromptDataset.averageTokenCount}
                    </p>
                  </div>
                  <div className="rounded-[10px] bg-slate-50 p-4">
                    <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                      Average Carbon Score
                    </p>
                    <p className="mt-1 text-2xl font-bold tabular-nums text-slate-900">
                      {carbonPromptDataset.averageCarbonScore}
                    </p>
                  </div>
                </div>
              </DatasetCard>
            </div>
          </RevealSection>

          <RevealSection className="space-y-6">
            <DatasetSectionHeader
              badge="Model Dataset"
              badgeVariant="blue"
              title="Model categories & performance"
              description="Category coverage and aggregate performance figures across 770 models, used to power the Green Model Efficiency Score and model recommendations."
            />

            <div className="grid gap-5 lg:grid-cols-2">
              <DatasetCard
                icon={Boxes}
                title="Model Categories"
                description="Number of models per category in the model dataset."
              >
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={modelCategoryData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis dataKey="name" tick={{ fontSize: 12, fill: "#64748b" }} />
                    <YAxis tick={{ fontSize: 11, fill: "#64748b" }} />
                    <RechartsTooltip contentStyle={CHART_TOOLTIP_STYLE} />
                    <Bar dataKey="value" fill="#15803d" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </DatasetCard>

              <DatasetCard
                icon={Cpu}
                title="Model Performance Summary"
                description="Aggregate speed, latency, context, and cost across all categories."
              >
                <div className="grid grid-cols-2 gap-3">
                  <motion.div
                    variants={fadeInUp}
                    className="rounded-[10px] bg-slate-50 p-3.5"
                  >
                    <div className="flex items-center gap-1.5 text-slate-500">
                      <Zap className="h-3.5 w-3.5" strokeWidth={1.75} />
                      <p className="text-xs font-medium">Avg Speed</p>
                    </div>
                    <p className="mt-1 text-xl font-bold tabular-nums text-slate-900">
                      {modelDataset.summaryStats.averageSpeedTps}
                      <span className="ml-1 text-xs font-medium text-slate-400">
                        tps
                      </span>
                    </p>
                  </motion.div>
                  <motion.div
                    variants={fadeInUp}
                    className="rounded-[10px] bg-slate-50 p-3.5"
                  >
                    <div className="flex items-center gap-1.5 text-slate-500">
                      <Clock3 className="h-3.5 w-3.5" strokeWidth={1.75} />
                      <p className="text-xs font-medium">Avg Latency</p>
                    </div>
                    <p className="mt-1 text-xl font-bold tabular-nums text-slate-900">
                      {modelDataset.summaryStats.averageLatencySeconds}
                      <span className="ml-1 text-xs font-medium text-slate-400">
                        s
                      </span>
                    </p>
                  </motion.div>
                  <motion.div
                    variants={fadeInUp}
                    className="rounded-[10px] bg-slate-50 p-3.5"
                  >
                    <div className="flex items-center gap-1.5 text-slate-500">
                      <Layers className="h-3.5 w-3.5" strokeWidth={1.75} />
                      <p className="text-xs font-medium">Avg Context</p>
                    </div>
                    <p className="mt-1 text-xl font-bold tabular-nums text-slate-900">
                      {(modelDataset.summaryStats.averageContextTokens / 1000).toFixed(0)}
                      <span className="ml-1 text-xs font-medium text-slate-400">
                        K tok
                      </span>
                    </p>
                  </motion.div>
                  <motion.div
                    variants={fadeInUp}
                    className="rounded-[10px] bg-slate-50 p-3.5"
                  >
                    <div className="flex items-center gap-1.5 text-slate-500">
                      <Coins className="h-3.5 w-3.5" strokeWidth={1.75} />
                      <p className="text-xs font-medium">Avg Input Cost</p>
                    </div>
                    <p className="mt-1 text-xl font-bold tabular-nums text-slate-900">
                      ${modelDataset.summaryStats.averageInputCost}
                    </p>
                  </motion.div>
                </div>
              </DatasetCard>
            </div>
          </RevealSection>

          <ResearchNotes />
        </div>
      </PageContainer>
  );
}
