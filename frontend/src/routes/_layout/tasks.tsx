import { useState } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { TasksService, TaskPublic } from "@/client"
import { AddTaskModal } from "@/components/ViewsCom/AddTaskModal"
import { PriorityBadge } from "@/components/ViewsCom/ProrityBadge"

export const Route = createFileRoute("/_layout/tasks")({
  component: TasksPage,
})

function TasksPage() {
  const queryClient = useQueryClient()
  const [isAddModalOpen, setIsAddModalOpen] = useState(false)

  // 1. 获取任务列表
  const { data: tasksData, isLoading, isError } = useQuery({
    queryKey: ["tasks"],
    queryFn: () => TasksService.readTasks({ skip: 0, limit: 100 }),
  })

  // 2. 更新状态 (勾选/取消勾选)
  const toggleStatusMutation = useMutation({
    mutationFn: (task: TaskPublic) =>
      TasksService.updateTaskRoute({
        taskNo: task.task_no,
        requestBody: { status: task.status === "todo" ? "done" : "todo" },
      }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["tasks"] }),
  })

  // 3. 删除任务 (通过 task_no 删除)
  const deleteTaskMutation = useMutation({
    mutationFn: (taskNo: string) =>
      TasksService.deleteTaskRoute({ taskNo }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["tasks"] }),
  })

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      {/* 顶部标题栏与新建按钮 */}
      <div className="flex items-center justify-between border-b pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">任务管理</h1>
          <p className="text-sm text-muted-foreground mt-1">
            查看与管理你的项目任务清单
          </p>
        </div>
        <button
          onClick={() => setIsAddModalOpen(true)}
          className="px-4 py-2 text-sm bg-primary text-primary-foreground rounded-md shadow hover:opacity-90 transition-opacity"
        >
          + 新建任务
        </button>
      </div>

      {/* 任务列表渲染区 */}
      {isLoading ? (
        <div className="text-center py-12 text-muted-foreground">加载中...</div>
      ) : isError ? (
        <div className="text-center py-12 text-destructive">获取任务列表失败</div>
      ) : tasksData?.data.length === 0 ? (
        <div className="text-center py-12 border border-dashed rounded-lg">
          <p className="text-muted-foreground">暂无任务，快点击右上角新建一个吧！</p>
        </div>
      ) : (
        <div className="grid gap-3">
          {tasksData?.data.map((task) => (
            <div
              key={task.id}
              className={`p-4 border rounded-lg flex items-center justify-between bg-card transition-all ${
                task.status === "done" ? "opacity-60 bg-muted/40" : ""
              }`}
            >
              {/* 左侧：复选框 + 标题 + 描述 */}
              <div className="flex items-start gap-3">
                <input
                  type="checkbox"
                  checked={task.status === "done"}
                  onChange={() => toggleStatusMutation.mutate(task)}
                  className="mt-1 h-4 w-4 rounded border-gray-300 cursor-pointer"
                />
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span
                      className={`font-medium ${
                        task.status === "done" ? "line-through text-muted-foreground" : ""
                      }`}
                    >
                      {task.title}
                    </span>
                    <PriorityBadge priority={task.priority} />
                  </div>
                  {task.description && (
                    <p className="text-sm text-muted-foreground line-clamp-1">
                      {task.description}
                    </p>
                  )}
                </div>
              </div>

              {/* 右侧：截止时间 + 编号 + 删除按钮 */}
              <div className="flex items-center gap-4 text-xs text-muted-foreground">
                {task.due_date && (
                  <div className="flex items-center gap-1">
                    <span>🕒 {new Date(task.due_date).toLocaleString()}</span>
                  </div>
                )}
                <span className="font-mono bg-muted px-2 py-0.5 rounded">
                  {task.task_no}
                </span>
                <button
                  onClick={() => deleteTaskMutation.mutate(task.task_no)}
                  disabled={deleteTaskMutation.isPending}
                  className="text-destructive hover:underline"
                >
                  删除
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* 新建弹窗 */}
      <AddTaskModal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
      />
    </div>
  )
}