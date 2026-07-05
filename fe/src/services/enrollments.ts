import api from "./api";

export interface Enrollment {
  id: number;
  student_id: number;
  course_id: number;
  status: string;
  enrolled_at: string;
}

export const getEnrollments = (courseId?: number, studentId?: number) =>
  api.get<Enrollment[]>("/enrollments", {
    params: {
      ...(courseId ? { course_id: courseId } : {}),
      ...(studentId ? { student_id: studentId } : {}),
    },
  });

export const getEnrollment = (id: number) =>
  api.get<Enrollment>(`/enrollments/${id}`);

export const createEnrollment = (data: Partial<Enrollment>) =>
  api.post<Enrollment>("/enrollments", data);

export const updateEnrollment = (id: number, data: { status: string }) =>
  api.put<Enrollment>(`/enrollments/${id}`, data);

export const deleteEnrollment = (id: number) =>
  api.delete(`/enrollments/${id}`);
