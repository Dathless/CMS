import api from "./api";

export interface Grade {
  id: number;
  enrollment_id: number;
  score: number | null;
  feedback: string | null;
  graded_at: string;
}

export const getGradesByEnrollment = (enrollmentId: number) =>
  api.get<Grade[]>(`/grades/enrollment/${enrollmentId}`);

export const getGrade = (id: number) => api.get<Grade>(`/grades/${id}`);

export const createGrade = (data: Partial<Grade>) =>
  api.post<Grade>("/grades", data);

export const updateGrade = (id: number, data: Partial<Grade>) =>
  api.put<Grade>(`/grades/${id}`, data);

export const deleteGrade = (id: number) => api.delete(`/grades/${id}`);
