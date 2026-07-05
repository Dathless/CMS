import { useContext } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ConfigProvider, theme } from "antd";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import { ThemeProvider, ThemeContext } from "./contexts/ThemeContext";
import AppLayout from "./components/Layout";
import Login from "./pages/Login";
import AdminDashboard from "./pages/AdminDashboard";
import LecturerDashboard from "./pages/LecturerDashboard";
import StudentDashboard from "./pages/StudentDashboard";
import Profile from "./pages/Profile";

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  if (loading) return null;
  return user ? <>{children}</> : <Navigate to="/login" />;
}

function DashboardRouter() {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" />;
  switch (user.role) {
    case "admin":
      return <AdminDashboard />;
    case "lecturer":
      return <LecturerDashboard />;
    case "student":
      return <StudentDashboard />;
    default:
      return <Navigate to="/login" />;
  }
}

function ThemedApp() {
  const { mode } = useContext(ThemeContext);

  return (
    <ConfigProvider
      theme={{
        algorithm:
          mode === "dark" ? theme.darkAlgorithm : theme.defaultAlgorithm,
        token: { colorPrimary: "#1677ff", borderRadius: 6 },
      }}
    >
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route
              path="/"
              element={
                <PrivateRoute>
                  <AppLayout />
                </PrivateRoute>
              }
            >
              <Route index element={<DashboardRouter />} />
              <Route path="profile" element={<Profile />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </ConfigProvider>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <ThemedApp />
    </ThemeProvider>
  );
}

// function DashboardRouter() {
//   const { user } = useAuth();
//   if (!user) return <Navigate to="/login" />;
//   switch (user.role) {
//     case "admin":
//       return <AdminDashboard />;
//     case "lecturer":
//       return <LecturerDashboard />;
//     case "student":
//       return <StudentDashboard />;
//     default:
//       return <Navigate to="/login" />;
//   }
// }

// function ThemedApp() {
//   const { mode } = React.useContext(ThemeContext)!;
//   const antTheme = {
//     algorithm: mode === "dark" ? antd.theme.darkAlgorithm : antd.theme.defaultAlgorithm,
//     token: { colorPrimary: "#1677ff", borderRadius: 6 },
//   };

//   return (
//     <ConfigProvider theme={antTheme}>
//       <AuthProvider>
//         <BrowserRouter>
//           <Routes>
//             <Route path="/login" element={<Login />} />
//             <Route
//               path="/"
//               element={
//                 <PrivateRoute>
//                   <AppLayout />
//                 </PrivateRoute>
//               }
//             >
//               <Route index element={<DashboardRouter />} />
//               <Route path="profile" element={<Profile />} />
//             </Route>
//           </Routes>
//         </BrowserRouter>
//       </AuthProvider>
//     </ConfigProvider>
//   );
// }

// export default function App() {
//   return (
//     <ThemeProvider>
//       <ThemedApp />
//     </ThemeProvider>
//   );
// }
