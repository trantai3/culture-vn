import React, { lazy, Suspense } from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
const Login = lazy(() => import("../../views/auth/login/index"));
const LayoutAdmin = lazy(() => import("../../app/layout/admin/index"));
const DashboardAdmin = lazy(() =>
  import("../../views/main/admin/dashboard/index")
);
const ManageAccountsAdmin = lazy(() =>
  import("../../views/main/admin/manage-accounts/index")
);
const ManageUsersAdmin = lazy(() =>
  import("../../views/main/admin/manage-users/index")
);
const router = createBrowserRouter([
  {
    path: "login",
    element: (
      <Suspense>
        <Login />
      </Suspense>
    ),
  },
  {
    path: "admin",
    element: (
      <Suspense>
        <LayoutAdmin />
      </Suspense>
    ),
    children: [
      {
        path: "dashboard",
        element: (
          <Suspense>
            <DashboardAdmin />
          </Suspense>
        ),
      },
      {
        path: "manage-users",
        element: (
          <Suspense>
            <ManageUsersAdmin />
          </Suspense>
        ),
      },
      {
        path: "manage-accounts",
        element: (
          <Suspense>
            <ManageAccountsAdmin />
          </Suspense>
        ),
      },
    ],
  },
]);

const Router = () => {
  return (
    <Suspense>
      <RouterProvider router={router} />
    </Suspense>
  );
};

export default Router;
