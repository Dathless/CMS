import { useEffect, useState } from "react";
import {
  Card,
  Row,
  Col,
  Statistic,
  Table,
  Typography,
  Button,
  Modal,
  Form,
  Input,
  Select,
  DatePicker,
  message,
  Popconfirm,
} from "antd";
import {
  UserOutlined,
  BookOutlined,
  TeamOutlined,
  PlusOutlined,
  DeleteOutlined,
} from "@ant-design/icons";
import { getUsers, type User } from "../services/users";
import {
  getCourses,
  createCourse,
  deleteCourse,
  type Course,
} from "../services/courses";

const { Title } = Typography;
const { TextArea } = Input;

export default function AdminDashboard() {
  const [users, setUsers] = useState<User[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [form] = Form.useForm();

  const fetchData = () => {
    setLoading(true);
    Promise.all([getUsers(), getCourses()])
      .then(([u, c]) => {
        setUsers(u.data);
        setCourses(c.data);
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchData();
  }, []);

  const students = users.filter((u) => u.role === "student");
  const lecturers = users.filter((u) => u.role === "lecturer");

  const handleCreate = async () => {
    try {
      const values = await form.validateFields();
      setSubmitting(true);
      await createCourse({
        title: values.title,
        description: values.description,
        lecturer_id: values.lecturer_id,
        start_date: values.start_date?.toISOString() || null,
        end_date: values.end_date?.toISOString() || null,
      });
      message.success("Course created successfully!");
      setModalOpen(false);
      form.resetFields();
      fetchData();
    } catch (err: unknown) {
      if (err && typeof err === "object" && "errorFields" in err) return;
      message.error("Failed to create course");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteCourse(id);
      message.success("Course deleted successfully!");
      fetchData();
    } catch {
      message.error("Failed to delete course");
    }
  };

  const userColumns = [
    { title: "ID", dataIndex: "id", key: "id" },
    { title: "Username", dataIndex: "username", key: "username" },
    { title: "Full Name", dataIndex: "full_name", key: "full_name" },
    { title: "Email", dataIndex: "email", key: "email" },
    { title: "Role", dataIndex: "role", key: "role" },
  ];

  const courseColumns = [
    { title: "ID", dataIndex: "id", key: "id" },
    { title: "Title", dataIndex: "title", key: "title" },
    { title: "Description", dataIndex: "description", key: "description" },
    {
      title: "Lecturer",
      dataIndex: "lecturer_id",
      key: "lecturer_id",
      render: (id: number) => {
        const lec = users.find((u) => u.id === id);
        return lec ? lec.full_name : id;
      },
    },
    { title: "Status", dataIndex: "status", key: "status" },
    {
      title: "Start Date",
      dataIndex: "start_date",
      key: "start_date",
      render: (val: string) => (val ? new Date(val).toLocaleDateString() : "-"),
    },
    {
      title: "Action",
      key: "action",
      render: (_: unknown, record: Course) => (
        <Popconfirm
          title="Delete this course?"
          onConfirm={() => handleDelete(record.id)}
          okText="Yes"
          cancelText="No"
        >
          <Button type="link" danger icon={<DeleteOutlined />} size="small">
            Delete
          </Button>
        </Popconfirm>
      ),
    },
  ];

  return (
    <div>
      <Title level={2}>Admin Dashboard</Title>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={8}>
          <Card>
            <Statistic title="Total Users" value={users.length} prefix={<TeamOutlined />} />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic title="Students" value={students.length} prefix={<UserOutlined />} />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic title="Courses" value={courses.length} prefix={<BookOutlined />} />
          </Card>
        </Col>
      </Row>

      <Card
        title="All Users"
        style={{ marginBottom: 24 }}
      >
        <Table columns={userColumns} dataSource={users} rowKey="id" loading={loading} />
      </Card>

      <Card
        title="All Courses"
        extra={
          <Button type="primary" icon={<PlusOutlined />} onClick={() => setModalOpen(true)}>
            Add Course
          </Button>
        }
      >
        <Table columns={courseColumns} dataSource={courses} rowKey="id" loading={loading} />
      </Card>

      <Modal
        title="Add New Course"
        open={modalOpen}
        onOk={handleCreate}
        onCancel={() => {
          setModalOpen(false);
          form.resetFields();
        }}
        confirmLoading={submitting}
        okText="Create"
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="title"
            label="Title"
            rules={[{ required: true, message: "Please enter course title" }]}
          >
            <Input placeholder="Course title" />
          </Form.Item>
          <Form.Item name="description" label="Description">
            <TextArea rows={3} placeholder="Course description" />
          </Form.Item>
          <Form.Item
            name="lecturer_id"
            label="Lecturer"
            rules={[{ required: true, message: "Please select a lecturer" }]}
          >
            <Select placeholder="Select lecturer">
              {lecturers.map((lec) => (
                <Select.Option key={lec.id} value={lec.id}>
                  {lec.full_name} ({lec.username})
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="start_date" label="Start Date">
                <DatePicker style={{ width: "100%" }} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="end_date" label="End Date">
                <DatePicker style={{ width: "100%" }} />
              </Form.Item>
            </Col>
          </Row>
        </Form>
      </Modal>
    </div>
  );
}
