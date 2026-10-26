export const Loading = () => <p className="p-4 text-sm text-gray-500">Loading...</p>;
export const ErrorState = ({ message = "Something went wrong." }: { message?: string }) => (
  <p className="p-4 text-sm text-red-600">{message}</p>
);
export const EmptyState = ({ message = "Nothing to show yet." }: { message?: string }) => (
  <p className="p-4 text-sm text-gray-500">{message}</p>
);
