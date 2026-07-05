import { Card, Descriptions, Typography } from "antd";
import { useAuth } from "../contexts/AuthContext";

const { Title } = Typography;

export default function Profile() {
  const { user } = useAuth();

  if (!user) return null;

  return (
    <div>
      <Title level={2}>Profile</Title>
      <Card>
        <Descriptions bordered column={1}>
          <Descriptions.Item label="ID">{user.id}</Descriptions.Item>
          <Descriptions.Item label="Username">{user.username}</Descriptions.Item>
          <Descriptions.Item label="Full Name">{user.full_name}</Descriptions.Item>
          <Descriptions.Item label="Email">{user.email}</Descriptions.Item>
          <Descriptions.Item label="Role">{user.role}</Descriptions.Item>
          <Descriptions.Item label="Created At">
            {new Date(user.created_at).toLocaleString()}
          </Descriptions.Item>
        </Descriptions>
      </Card>
    </div>
  );
}
