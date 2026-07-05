import api from "./api";

export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  role: string;
  created_at: string;
}

export const getMe = () => api.get<User>("/users/me");

export const getUsers = (role?: string) =>
  api.get<User[]>("/users", { params: role ? { role } : {} });

export const getUser = (id: number) => api.get<User>(`/users/${id}`);

export const updateUser = (id: number, data: Partial<User>) =>
  api.put<User>(`/users/${id}`, data);

export const deleteUser = (id: number) => api.delete(`/users/${id}`);
