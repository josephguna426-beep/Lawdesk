import { Route, Routes } from "react-router-dom";
import AppLayout from "./layouts/AppLayout";
import ProtectedRoute from "./routes/ProtectedRoute";
import LoginPage from "./features/auth/LoginPage";
import DashboardPage from "./features/dashboard/DashboardPage";
import CaseListPage from "./features/cases/CaseListPage";
import CaseFormPage from "./features/cases/CaseFormPage";
import CaseDetailPage from "./features/cases/CaseDetailPage";
import ClientListPage from "./features/clients/ClientListPage";
import ClientFormPage from "./features/clients/ClientFormPage";
import PartyListPage from "./features/parties/PartyListPage";
import PartyFormPage from "./features/parties/PartyFormPage";
import CourtListPage from "./features/courts/CourtListPage";
import AdvocateListPage from "./features/advocates/AdvocateListPage";
import HearingListPage from "./features/hearings/HearingListPage";
import HearingFormPage from "./features/hearings/HearingFormPage";
import NotificationCentrePage from "./features/notifications/NotificationCentrePage";
import ReportsPage from "./features/reports/ReportsPage";
import SettingsPage from "./features/settings/SettingsPage";
import AuditHistoryPage from "./features/settings/AuditHistoryPage";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/cases" element={<CaseListPage />} />
          <Route path="/cases/new" element={<CaseFormPage />} />
          <Route path="/cases/:id" element={<CaseDetailPage />} />
          <Route path="/cases/:id/edit" element={<CaseFormPage />} />
          <Route path="/clients" element={<ClientListPage />} />
          <Route path="/clients/new" element={<ClientFormPage />} />
          <Route path="/clients/:id/edit" element={<ClientFormPage />} />
          <Route path="/parties" element={<PartyListPage />} />
          <Route path="/parties/new" element={<PartyFormPage />} />
          <Route path="/parties/:id/edit" element={<PartyFormPage />} />
          <Route path="/courts" element={<CourtListPage />} />
          <Route path="/advocates" element={<AdvocateListPage />} />
          <Route path="/hearings" element={<HearingListPage />} />
          <Route path="/hearings/new" element={<HearingFormPage />} />
          <Route path="/hearings/:id/edit" element={<HearingFormPage />} />
          <Route path="/notifications" element={<NotificationCentrePage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="/audit" element={<AuditHistoryPage />} />
        </Route>
      </Route>
      <Route path="*" element={<p className="p-6">Page not found</p>} />
    </Routes>
  );
}
