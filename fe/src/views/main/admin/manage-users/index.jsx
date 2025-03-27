import { Col, Input, Row, Select, Table } from "antd";
import { SearchOutlined } from "@ant-design/icons";
const ManageUsers = () => {
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
      title: "Tên",
      dataIndex: "name",
      key: "name",
    },
    {
      title: "Tuổi",
      dataIndex: "age",
      key: "age",
    },
    {
      title: "Địa chỉ",
      dataIndex: "address",
      key: "address",
    },
  ];
  const data = [
    { key: "1", name: "Nguyễn Văn A", age: 25, address: "Hà Nội" },
    { key: "2", name: "Trần Thị B", age: 30, address: "Hồ Chí Minh" },
    { key: "3", name: "Lê Văn C", age: 22, address: "Đà Nẵng" },
  ];
  return (
    <>
      <div class="!mt-[24px] font-[700] text-[20px] text-[#0F1012]">
        Danh sách người dùng
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

export default ManageUsers;
