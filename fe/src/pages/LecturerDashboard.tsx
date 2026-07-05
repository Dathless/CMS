import { useEffect, useState } from "react";
import { Card, Table, Typography } from "antd";
import { useAuth } from "../contexts/AuthContext";
import { getCourses, type Course } from "../services/courses";

const { Title } = Typography;

export default function LecturerDashboard() {
  const { user } = useAuth();
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      getCourses(user.id)
        .then((res) => setCourses(res.data))
        .finally(() => setLoading(false));
    }
  }, [user]);

  const columns = [
    { title: "ID", dataIndex: "id", key: "id" },
    { title: "Title", dataIndex: "title", key: "title" },
    { title: "Description", dataIndex: "description", key: "description" },
    { title: "Status", dataIndex: "status", key: "status" },
    {
      title: "Start Date",
      dataIndex: "start_date",
      key: "start_date",
      render: (val: string) => (val ? new Date(val).toLocaleDateString() : "-"),
    },
  ];

  return (
    <div>
      <Title level={2}>Lecturer Dashboard</Title>
      <Card title="My Courses">
        <Table columns={columns} dataSource={courses} rowKey="id" loading={loading} />
      </Card>
    </div>
  );
}
