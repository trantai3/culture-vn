import { useState } from "react";
import { Avatar, Dropdown, Typography, Button } from "antd";
import { UserOutlined, LockOutlined, LogoutOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import useSignOut from "react-auth-kit/hooks/useSignOut";
import useAuthUser from "react-auth-kit/hooks/useAuthUser";
import ChangePassword from "../../../../views/auth/changePassword";

const Header = ({ headerInfo }) => {
  const [changePassword, setChangePassword] = useState(false);
  const signOut = useSignOut();
  const authUser = useAuthUser(); // Kiểm tra trạng thái đăng nhập
  const navigate = useNavigate();

  const handleChangePassword = () => {
    setChangePassword((prev) => !prev);
  };

  const handleClickUserAction = (key) => {
    if (key === "logout") {
      signOut();
      navigate("/login");
    }
    if (key === "changePassword") {
      handleChangePassword();
    }
  };

  const menuItems = [
    {
      key: "changePassword",
      label: "Đổi mật khẩu",
      icon: <LockOutlined />,
    },
    {
      key: "logout",
      label: "Đăng xuất",
      icon: <LogoutOutlined />,
      danger: true,
    },
  ];

  return (
    <div className="flex justify-between items-center">
      <div className="flex items-center gap-2">
        {headerInfo?.icon}
        <h1>{headerInfo?.title}</h1>
      </div>
      <div className="flex items-center">
        {/* Kiểm tra nếu chưa đăng nhập */}
        {!authUser ? (
          <div className="flex gap-3">
            <Button type="primary" onClick={() => navigate("/login")}>
              Đăng nhập
            </Button>
            <Button onClick={() => navigate("/register")}>Đăng ký</Button>
          </div>
        ) : (
          <Dropdown
            menu={{
              items: menuItems,
              onClick: ({ key }) => handleClickUserAction(key),
            }}
            trigger={["click"]}
          >
            <div className="cursor-pointer flex items-center gap-2">
              <Typography.Text strong>{authUser.username}</Typography.Text>
              <Avatar size="large" icon={<UserOutlined />} />
            </div>
          </Dropdown>
        )}
        <ChangePassword open={changePassword} onClose={handleChangePassword} />
      </div>
    </div>
  );
};

export default Header;
