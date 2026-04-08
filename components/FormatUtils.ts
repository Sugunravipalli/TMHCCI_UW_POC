export function formatCurrency(value: number): string {
  if (value >= 1_000_000_000) return `$${(value / 1_000_000_000).toFixed(1)}B`;
  if (value >= 1_000_000) return `$${(value / 1_000_000).toFixed(1)}M`;
  if (value >= 1_000) return `$${(value / 1_000).toFixed(0)}K`;
  return `$${value.toLocaleString()}`;
}

export function formatNumber(value: number): string {
  return value.toLocaleString();
}

export function formatPct(value: number, decimals = 1): string {
  return `${Number(value).toFixed(decimals)}%`;
}

export function formatDate(value: string | null): string {
  if (!value) return "—";
  return new Date(value).toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

export function gradeColor(grade: string): string {
  if (grade.startsWith("A")) return "text-emerald-600";
  if (grade.startsWith("B")) return "text-blue-600";
  if (grade.startsWith("C")) return "text-amber-600";
  return "text-red-600";
}

export function gradeBg(grade: string): string {
  if (grade.startsWith("A")) return "bg-emerald-50 text-emerald-700 border-emerald-200";
  if (grade.startsWith("B")) return "bg-blue-50 text-blue-700 border-blue-200";
  if (grade.startsWith("C")) return "bg-amber-50 text-amber-700 border-amber-200";
  return "bg-red-50 text-red-700 border-red-200";
}

export function classificationColor(category: string): string {
  const map: Record<string, string> = {
    INITIAL_SUBMISSION: "bg-blue-50 text-blue-700 border-blue-200",
    FOLLOW_UP_DOCUMENTS: "bg-amber-50 text-amber-700 border-amber-200",
    BINDING_ORDER: "bg-emerald-50 text-emerald-700 border-emerald-200",
    RENEWAL_SUBMISSION: "bg-purple-50 text-purple-700 border-purple-200",
    UW_QUERY_RESPONSE: "bg-cyan-50 text-cyan-700 border-cyan-200",
    MID_JOURNEY_UPDATE: "bg-orange-50 text-orange-700 border-orange-200",
  };
  return map[category] || "bg-gray-100 text-gray-600 border-gray-200";
}

export function classificationLabel(category: string): string {
  return category
    .split("_")
    .map((w) => w.charAt(0) + w.slice(1).toLowerCase())
    .join(" ");
}

export function decisionColor(decision: string): string {
  const d = decision?.toUpperCase() || "";
  if (d === "BOUND") return "bg-emerald-50 text-emerald-700 border-emerald-200";
  if (d === "QUOTED") return "bg-blue-50 text-blue-700 border-blue-200";
  if (d === "DECLINED") return "bg-red-50 text-red-700 border-red-200";
  if (d === "NTU") return "bg-amber-50 text-amber-700 border-amber-200";
  return "bg-gray-100 text-gray-600 border-gray-200";
}
