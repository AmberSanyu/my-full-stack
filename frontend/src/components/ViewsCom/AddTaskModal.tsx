import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useForm } from "react-hook-form"
import { TaskCreate, TasksService } from "@/client"

interface AddTaskModalProps {
  isOpen: boolean
  onClose: () => void
}

export function AddTaskModal({ isOpen, onClose }: AddTaskModalProps) {
  const queryClient = useQueryClient()
  const { register, handleSubmit, reset } = useForm<TaskCreate>({
    defaultValues: {
      priority: "medium",
      status: "todo",
    },
  })

  const mutation = useMutation({
    mutationFn: (data: TaskCreate) =>
      TasksService.createTask({
        requestBody: {
          ...data,
          due_date: data.due_date ? new Date(data.due_date).toISOString() : null,
        },
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] })
      reset()
      onClose()
    },
  })

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="bg-background w-full max-w-md rounded-lg p-6 shadow-xl border">
        <h2 className="text-lg font-bold mb-4">新建任务</h2>
        
        <form onSubmit={handleSubmit((data) => mutation.mutate(data))} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">任务标题 *</label>
            <input
              {...register("title", { required: true })}
              className="w-full border rounded p-2 text-sm bg-background"
              placeholder="请输入任务标题..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">描述</label>
            <textarea
              {...register("description")}
              className="w-full border rounded p-2 text-sm bg-background h-20"
              placeholder="添加详细描述..."
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">优先级</label>
              <select {...register("priority")} className="w-full border rounded p-2 text-sm bg-background">
                <option value="low">🟢 低优先级</option>
                <option value="medium">🟡 中优先级</option>
                <option value="high">🔴 高优先级</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">截止时间</label>
              <input
                type="datetime-local"
                {...register("due_date")}
                className="w-full border rounded p-2 text-sm bg-background"
              />
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm border rounded hover:bg-muted"
            >
              取消
            </button>
            <button
              type="submit"
              disabled={mutation.isPending}
              className="px-4 py-2 text-sm bg-primary text-primary-foreground rounded hover:opacity-90 disabled:opacity-50"
            >
              {mutation.isPending ? "创建中..." : "确认创建"}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}