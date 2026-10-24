import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { Toaster } from "react-hot-toast";
import AppShell from "@/components/layout/AppShell";
import { APP_NAME, APP_TAGLINE } from "@/utils/constants";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: {
    default: APP_NAME,
    template: `%s · ${APP_NAME}`,
  },
  description: APP_TAGLINE,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className={`${inter.className} flex min-h-screen flex-col`}>
        <a
          href="#main-content"
          className="sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[100] focus:m-0 focus:inline-flex focus:h-auto focus:w-auto focus:overflow-visible focus:whitespace-nowrap focus:rounded-inner focus:bg-emerald-600 focus:px-4 focus:py-2 focus:text-sm focus:font-semibold focus:text-white focus:shadow-floating focus:outline-none"
        >
          Skip to main content
        </a>
        <AppShell>{children}</AppShell>
        <Toaster
          position="top-right"
          toastOptions={{
            className: "text-sm",
            style: {
              borderRadius: "10px",
              border: "1px solid #e2e8f0",
              background: "#ffffff",
              color: "#0f172a",
            },
            success: {
              iconTheme: {
                primary: "#059669",
                secondary: "#ffffff",
              },
            },
          }}
        />
      </body>
    </html>
  );
}
