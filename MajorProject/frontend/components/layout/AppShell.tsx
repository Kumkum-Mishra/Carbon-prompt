"use client";

import type { ReactNode } from "react";
import { MotionConfig } from "framer-motion";
import Footer from "@/components/layout/Footer";
import Navbar from "@/components/layout/Navbar";
import PageTransition from "@/components/layout/PageTransition";

export default function AppShell({ children }: { children: ReactNode }) {
  return (
    <MotionConfig reducedMotion="user">
      <Navbar />
      <main id="main-content" tabIndex={-1} className="flex-1 outline-none">
        <PageTransition>{children}</PageTransition>
      </main>
      <Footer />
    </MotionConfig>
  );
}
