"use client";

import ArchitecturePreview from "@/components/home/ArchitecturePreview";
import FeatureGrid from "@/components/home/FeatureGrid";
import Hero from "@/components/home/Hero";
import MetricsPreview from "@/components/home/MetricsPreview";
import ProblemStatement from "@/components/home/ProblemStatement";
import ProductWorkflow from "@/components/home/ProductWorkflow";
import ResearchValue from "@/components/home/ResearchValue";
import TechStack from "@/components/home/TechStack";

export default function HomePage() {
  return (
    <>
      <Hero />
      <ProblemStatement />
      <ProductWorkflow />
      <FeatureGrid />
      <MetricsPreview />
      <ArchitecturePreview />
      <TechStack />
      <ResearchValue />
    </>
  );
}
