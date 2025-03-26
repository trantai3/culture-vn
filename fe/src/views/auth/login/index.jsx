import { Button, Card, Flex, Form, Input, Typography } from "antd";
const Login = () => {
  return (
    <Flex justify="center" className="!py-20">
      <Card className="shadow">
        <Flex vertical align="center" gap={32}>
          <Flex align="center" gap={16}>
            <Typography.Text className="!text-[24px]">
              Đăng nhập
            </Typography.Text>
          </Flex>
          <Form autoComplete="off" layout="vertical" className="w-[300px]">
            <Form.Item
              label="Tên tài khoản"
              name="userName"
              rules={[
                {
                  required: true,
                  message: "Vui lòng nhập tên tài khoản!",
                },
              ]}
            >
              <Input size="large" placeholder="Tên tài khoản" />
            </Form.Item>

            <Form.Item
              label="Mật khẩu"
              name="password"
              rules={[
                {
                  required: true,
                  message: "Vui lòng nhập mật khẩu!",
                },
              ]}
            >
              <Input.Password size="large" placeholder="Mật khẩu" />
            </Form.Item>
            <Button
              size="large"
              type="primary"
              htmlType="submit"
              className="w-full"
            >
              Đăng nhập
            </Button>
          </Form>
        </Flex>
      </Card>
    </Flex>
  );
};

export default Login;
