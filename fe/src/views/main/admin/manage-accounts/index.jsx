import { Col, Input, Row, Select, Table } from "antd";
import { SearchOutlined } from "@ant-design/icons";
import { useEffect, useState } from "react";
import { CLIENTS_LIST } from "../../../../api/constants";
import useApi from "../../../../hooks/useApi";
const ManageAccounts = () => {
  const options = [
    {
      value: "",
      label: "Trạng thái",
    },
    {
      value: "active",
      label: "Trạng thái hoạt động",
    },
    {
      value: "inactive",
      label: "Trạng thái dừng hoạt động",
    },
  ];
  const columns = [
    {
      title: "Họ và tên",
      dataIndex: "full_name",
      key: "full_name",
    },
    {
      title: "Email",
      dataIndex: "email",
      key: "email",
    },
    {
      title: "Trạng thái",
      dataIndex: "is_active",
      key: "is_active",
    },
  ];
  const data = [
    { key: "1", name: "Nguyễn Văn A", age: 25, address: "Hà Nội" },
    { key: "2", name: "Trần Thị B", age: 30, address: "Hồ Chí Minh" },
    { key: "3", name: "Lê Văn C", age: 22, address: "Đà Nẵng" },
  ];
  const Api = useApi();
  const [user, setUser] = useState(null);
  const [page, setPage] = useState(1);
  const [perPage, setPerPage] = useState(20);
  useEffect(() => {
    const fetchData = async () => {
      const response = await Api.Get(CLIENTS_LIST(page, perPage));
      setUser(response.users);
    };
    fetchData();
  }, [page, perPage]);
  return (
    <>
      <div class="!mt-[24px] font-[700] text-[20px] text-[#0F1012]">
        Danh sách tài khoản
      </div>
      <Row className="!mt-[24px]" gutter={16}>
        <Col span={20}>
          <Input addonAfter={<SearchOutlined />} placeholder="" />
        </Col>
        <Col span={4}>
          <Select className="w-full" defaultValue="" options={options} />
        </Col>
      </Row>
      <Table className="!mt-[24px]" columns={columns} dataSource={data} />
    </>
  );
};

export default ManageAccounts;
