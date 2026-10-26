export type CaseStatus = "open" | "in_progress" | "on_hold" | "closed";

export interface User { id: number; username: string; first_name: string; last_name: string; email: string; is_staff: boolean }
export interface Court { id: number; name: string; court_type: string; location: string }
export interface Advocate { id: number; full_name: string; email: string; phone: string; registration_number: string; address: string }
export interface Client { id: number; full_name: string; email: string; phone: string; address: string }
export interface Party { id: number; full_name: string; party_type: string; email: string; phone: string; address: string }
export interface Case {
  id: number; case_number: string; title: string; case_type: string; description: string;
  status: CaseStatus; court: number; court_name: string; filing_date: string; is_archived: boolean;
}
export interface Hearing {
  id: number; case: number; case_number: string; hearing_datetime: string;
  status: "scheduled" | "completed" | "rescheduled" | "cancelled";
  proceedings: string; judge_comments: string; orders: string; next_hearing_date: string | null;
}
export interface DocumentItem { id: number; case: number; title: string; original_name: string; content_type: string; size_bytes: number; uploaded_at: string }
export interface ClosurePdf { id: number; case: number; version: number; status: "pending" | "processing" | "ready" | "failed"; error_message: string; generated_at: string | null }
export interface AppNotification { id: number; title: string; message: string; is_read: boolean; created_at: string }
export interface AuditEntry { id: number; username: string | null; action: string; entity_type: string; entity_id: string; created_at: string }
