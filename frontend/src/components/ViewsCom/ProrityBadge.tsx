export function PriorityBadge({ priority }: { priority?: string }) {
    const map: Record<string, { label: string; style: string }> = {
      high: { label: "高", style: "bg-red-100 text-red-700 border-red-200 dark:bg-red-950 dark:text-red-300 dark:border-red-800" },
      medium: { label: "中", style: "bg-amber-100 text-amber-700 border-amber-200 dark:bg-amber-950 dark:text-amber-300 dark:border-amber-800" },
      low: { label: "低", style: "bg-emerald-100 text-emerald-700 border-emerald-200 dark:bg-emerald-950 dark:text-emerald-300 dark:border-emerald-800" },
    }
  
    const current = map[priority || "medium"] || map.medium
  
    return (
      <span className={`px-2 py-0.5 text-xs font-medium border rounded-md inline-flex items-center gap-1 ${current.style}`}>
        {current.label}
      </span>
    )
  }