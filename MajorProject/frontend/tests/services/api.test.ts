jest.mock("axios", () => {
  const post = jest.fn();
  const get = jest.fn();
  return {
    __esModule: true,
    default: {
      create: jest.fn(() => ({ post, get })),
      isAxiosError: jest.fn(),
      post,
      get,
    },
    isAxiosError: jest.fn(),
  };
});

import axios from "axios";
import { processPrompt, ApiServiceError } from "@/services/api";

const mockedAxios = axios as jest.Mocked<typeof axios>;

describe("api service", () => {
  const client = (mockedAxios.create as jest.Mock).mock.results[0]?.value;

  it("processPrompt returns success response", async () => {
    const mockResponse = {
      success: true,
      pipeline: {},
      metadata: { processing_time_ms: 100, pipeline_version: "1.0" },
    };
    client.post.mockResolvedValue({ data: mockResponse });

    const result = await processPrompt("Write CNN code");
    expect(result).toEqual(mockResponse);
    expect(client.post).toHaveBeenCalledWith("/process", {
      prompt: "Write CNN code",
    });
  });

  it("processPrompt throws on network error", async () => {
    mockedAxios.isAxiosError.mockReturnValue(true);
    client.post.mockRejectedValue({ isAxiosError: true, response: undefined });

    await expect(processPrompt("test")).rejects.toBeInstanceOf(ApiServiceError);
  });
});
