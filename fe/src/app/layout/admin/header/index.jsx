const HeaderAdmin = ({ headerInfo }) => {
  return (
    <div className="flex items-center">
      <div className="flex items-center gap-2">
        {headerInfo.icon}
        <h1>{headerInfo.title}</h1>
      </div>
      <div className="flex items-center"></div>
    </div>
  );
};

export default HeaderAdmin;
