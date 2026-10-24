import { fireEvent, render, screen } from "@testing-library/react";
import PromptInput from "@/components/analyze/PromptInput";

describe("PromptInput", () => {
  it("disables submit when prompt is empty", () => {
    render(<PromptInput onSubmit={jest.fn()} isLoading={false} />);
    expect(screen.getByRole("button", { name: /analyze/i })).toBeDisabled();
  });

  it("shows validation message on empty submit", () => {
    render(<PromptInput onSubmit={jest.fn()} isLoading={false} />);
    fireEvent.submit(screen.getByRole("textbox").closest("form")!);
    expect(screen.getByText("Please enter a prompt.")).toBeInTheDocument();
  });

  it("calls onSubmit with trimmed prompt", () => {
    const onSubmit = jest.fn();
    render(<PromptInput onSubmit={onSubmit} isLoading={false} />);
    fireEvent.change(screen.getByRole("textbox"), {
      target: { value: "  Write CNN code  " },
    });
    fireEvent.click(screen.getByRole("button", { name: /analyze/i }));
    expect(onSubmit).toHaveBeenCalledWith("Write CNN code");
  });

  it("shows optimized panel empty state before analysis", () => {
    render(<PromptInput onSubmit={jest.fn()} isLoading={false} />);
    expect(
      screen.getByText(/optimized prompt will appear here/i)
    ).toBeInTheDocument();
  });

  it("renders copy action when optimized prompt is present", () => {
    render(
      <PromptInput
        onSubmit={jest.fn()}
        isLoading={false}
        optimizedPrompt="Write a PyTorch CNN implementation."
      />
    );
    expect(
      screen.getByRole("button", { name: /copy optimized prompt/i })
    ).toBeInTheDocument();
    expect(
      screen.getByLabelText(/optimized prompt with changes/i)
    ).toBeInTheDocument();
  });
});
