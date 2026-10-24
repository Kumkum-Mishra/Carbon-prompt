import axios, { AxiosError } from "axios";
import type { HealthResponse, ProcessResponse } from "@/types/api";
import { API_TIMEOUT_MS } from "@/utils/constants";

const baseURL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export const API_BASE_URL = baseURL;

export const apiClient = axios.create({
  baseURL,
  timeout: API_TIMEOUT_MS,
  headers: { "Content-Type": "application/json" },
});

export class ApiServiceError extends Error {
  constructor(
    message: string,
    public readonly statusCode?: number,
    public readonly details?: string
  ) {
    super(message);
    this.name = "ApiServiceError";
  }
}

export async function processPrompt(prompt: string): Promise<ProcessResponse> {
  try {
    const { data } = await apiClient.post<ProcessResponse>("/process", {
      prompt,
    });
    return data;
  } catch (error) {
    throw mapApiError(error);
  }
}

export async function checkHealth(): Promise<HealthResponse> {
  try {
    const { data } = await apiClient.get<HealthResponse>("/health");
    return data;
  } catch (error) {
    throw mapApiError(error);
  }
}

function mapApiError(error: unknown): ApiServiceError {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<{
      message?: string;
      details?: string;
    }>;

    if (!axiosError.response) {
      if (axiosError.code === "ECONNABORTED") {
        return new ApiServiceError(
          "Request timed out. The prompt may be too complex."
        );
      }
      return new ApiServiceError(
        "Unable to connect to backend. Please ensure the server is running."
      );
    }

    const status = axiosError.response.status;
    const message =
      axiosError.response.data?.message ||
      (status >= 500
        ? "Unexpected server error. Please try again."
        : "Request failed.");

    return new ApiServiceError(
      message,
      status,
      axiosError.response.data?.details
    );
  }

  return new ApiServiceError("Unexpected server error. Please try again.");
}
