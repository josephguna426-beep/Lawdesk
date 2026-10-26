// Module 8: confirmation dialog -> POST /api/cases/{id}/close/
export default function CloseCaseDialog({ caseId, onClose }: { caseId: number; onClose: () => void }) {
  return (
    <div className="rounded border p-4">
      <p className="text-sm">Close case #{caseId} (TODO: outcome, closure date, remarks, final order reference)</p>
      <button onClick={onClose} className="mt-2 text-sm underline">Cancel</button>
    </div>
  );
}
