import api from "./api";

export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export const login = (data: LoginRequest) =>
  api.post<TokenResponse>("/auth/login", data);

export const logout = (refreshToken: string) =>
  api.post("/auth/logout", { refresh_token: refreshToken });

export const refreshToken = (refreshToken: string) =>
  api.post<TokenResponse>("/auth/refresh", { refresh_token: refreshToken });
