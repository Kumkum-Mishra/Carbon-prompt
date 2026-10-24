import "@testing-library/jest-dom";

// Recharts' ResponsiveContainer relies on ResizeObserver, which jsdom does not
// implement. Provide a minimal no-op polyfill so chart-bearing components can
// render in tests.
if (typeof global.ResizeObserver === "undefined") {
  global.ResizeObserver = class ResizeObserver {
    observe() {}
    unobserve() {}
    disconnect() {}
  };
}
