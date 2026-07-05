import { useEffect, useState } from "react";
import { Card, Table, Typography, Button, message } from "antd";
import { useAuth } from "../contexts/AuthContext";
import { getCourses, type Course } from "../services/courses";
import {
  getEnrollments,
  createEnrollment,
} from "../services/enrollments";

const { Title } = Typography;

export default function StudentDashboard() {
  const { user } = useAuth();
  const [courses, setCourses] = useState<Course[]>([]);
  const [enrolledCourseIds, setEnrolledCourseIds] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      Promise.all([getCourses(), getEnrollments(undefined, user.id)])
        .then(([c, e]) => {
          setCourses(c.data);
          setEnrolledCourseIds(e.data.map((en) => en.course_id));
        })
        .finally(() => setLoading(false));
    }
  }, [user]);

  const handleEnroll = async (courseId: number) => {
    try {
      await createEnrollment({ student_id: user!.id, course_id: courseId });
      setEnrolledCourseIds((prev) => [...prev, courseId]);
      message.success("Enrolled successfully!");
    } catch {
      message.error("Failed to enroll");
    }
  };

  const columns = [
    { title: "ID", dataIndex: "id", key: "id" },
    { title: "Title", dataIndex: "title", key: "title" },
    { title: "Description", dataIndex: "description", key: "description" },
    { title: "Status", dataIndex: "status", key: "status" },
    {
      title: "Action",
      key: "action",
      render: (_: unknown, record: Course) =>
        enrolledCourseIds.includes(record.id) ? (
          <span style={{ color: "#52c41a" }}>Enrolled</span>
        ) : (
          <Button type="primary" size="small" onClick={() => handleEnroll(record.id)}>
            Enroll
          </Button>
        ),
    },
  ];

  return (
    <div>
      <Title level={2}>Student Dashboard</Title>
      <Card title="Available Courses">
        <Table columns={columns} dataSource={courses} rowKey="id" loading={loading} />
      </Card>
    </div>
  );
}
