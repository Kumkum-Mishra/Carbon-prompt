import { render, screen } from "@testing-library/react";
import Navbar from "@/components/layout/Navbar";

jest.mock("next/navigation", () => ({
  usePathname: () => "/",
}));

describe("Navbar navigation", () => {
  it("renders all nav links", () => {
    render(<Navbar />);
    expect(screen.getByText("Home")).toBeInTheDocument();
    expect(screen.getByText("Analyze")).toBeInTheDocument();
    expect(screen.getByText("Mathematics")).toBeInTheDocument();
    expect(screen.getByText("Datasets")).toBeInTheDocument();
    expect(screen.getByText("GitHub")).toBeInTheDocument();
  });
});
