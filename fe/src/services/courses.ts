import api from "./api";

export interface Course {
  id: number;
  title: string;
  description: string | null;
  lecturer_id: number;
  start_date: string | null;
  end_date: string | null;
  status: string;
  created_at: string;
}

export const getCourses = (lecturerId?: number) =>
  api.get<Course[]>("/courses", {
    params: lecturerId ? { lecturer_id: lecturerId } : {},
  });

export const getCourse = (id: number) => api.get<Course>(`/courses/${id}`);

export const createCourse = (data: Partial<Course>) =>
  api.post<Course>("/courses", data);

export const updateCourse = (id: number, data: Partial<Course>) =>
  api.put<Course>(`/courses/${id}`, data);

export const deleteCourse = (id: number) => api.delete(`/courses/${id}`);
