'use client';

import { useState, useEffect, useMemo } from 'react';
import Navbar from '../../components/Navbar';
import TaskCard from '../../components/TaskCard';
import TaskForm from '../../components/TaskForm';
import { Task } from '../../lib/types';
import { taskAPI } from '../../lib/api';
import toast from 'react-hot-toast';

// -------------------- NORMALIZE TASK --------------------
const normalizeTask = (task: any): Task => {
  if (!task) throw new Error('Invalid task data');

  return {
    id: String(task.id),
    title: task.title,
    description: task.description || '',
    status: task.status || 'todo',
    priority: task.priority || 'medium',
    dueDate: task.due_date || task.dueDate || '',
    completed: task.completed ?? task.status === 'completed',
    created_at: task.created_at,
    updated_at: task.updated_at,
    userId: task.user_id,
  };
};

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [filter, setFilter] =
    useState<'all' | 'todo' | 'in-progress' | 'completed'>('all');

  // -------------------- FETCH TASKS --------------------
  const fetchTasks = async () => {
    try {
      const data = await taskAPI.getTasks();
      const normalized = data.map((t: any) => normalizeTask(t));
      setTasks(normalized);
      console.log('📥 Tasks loaded:', normalized);
    } catch (err: any) {
      toast.error(err.message || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  // -------------------- CREATE --------------------
  const handleCreateTask = async (taskData: Partial<Task>) => {
    try {
      if (!taskData.title) return toast.error('Title required');

      const payload = {
        title: taskData.title,
        description: taskData.description || '',
        status: taskData.status || 'todo',
        priority: taskData.priority || 'medium',
        dueDate: taskData.dueDate || undefined,
      };

      const created = normalizeTask(await taskAPI.createTask(payload));
      setTasks(prev => [created, ...prev]);
      setShowForm(false);
      toast.success('Task created');
      console.log('✅ Task created:', created);
    } catch (err: any) {
      toast.error(err.message || 'Create failed');
    }
  };

  // -------------------- UPDATE --------------------
  const handleUpdateTask = async (taskId: string, taskData: Partial<Task>) => {
    try {
      if (!taskData.title) return toast.error('Title required');

      const payload = {
        title: taskData.title,
        description: taskData.description || '',
        status: taskData.status,
        priority: taskData.priority,
        dueDate: taskData.dueDate || undefined,
      };

      const updated = normalizeTask(
        await taskAPI.updateTask(taskId, payload)
      );

      setTasks(prev => prev.map(t => (t.id === taskId ? updated : t)));
      setEditingTask(null);
      setShowForm(false);
      toast.success('Task updated');
      console.log('✅ Task updated:', updated);
    } catch (err: any) {
      toast.error(err.message || 'Update failed');
    }
  };

  // -------------------- DELETE --------------------
  const handleDeleteTask = async (taskId: string) => {
    if (!confirm('Delete this task?')) return;

    try {
      await taskAPI.deleteTask(taskId);
      setTasks(prev => prev.filter(t => t.id !== taskId));
      toast.success('Task deleted');
      console.log('🗑️ Task deleted:', taskId);
    } catch (err: any) {
      toast.error(err.message || 'Delete failed');
    }
  };

  // -------------------- STATUS CHANGE (🔥 FIXED) --------------------
  const handleStatusChange = async (
    taskId: string,
    newStatus: Task['status']
  ) => {
    const previous = [...tasks];
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;

    try {
      console.log(`🔄 Updating task ${taskId} to status: ${newStatus}`);
      
      // Optimistic UI update
      setTasks(prev =>
        prev.map(t =>
          t.id === taskId
            ? {
                ...t,
                status: newStatus,
                completed: newStatus === 'completed',
              }
            : t
        )
      );

      // 🔴 FULL PAYLOAD (THIS FIXES 422)
      const payload = {
        title: task.title,
        description: task.description,
        status: newStatus,
        priority: task.priority,
        dueDate: task.dueDate || undefined,
      };

      const updated = normalizeTask(
        await taskAPI.updateTask(taskId, payload)
      );

      // Update with server response
      setTasks(prev => prev.map(t => (t.id === taskId ? updated : t)));
      
      console.log('✅ Status updated successfully:', updated);
      console.log('📊 Current counts:', {
        all: tasks.length,
        todo: tasks.filter(t => t.status === 'todo').length,
        inProgress: tasks.filter(t => t.status === 'in-progress').length,
        completed: tasks.filter(t => t.status === 'completed').length,
      });
    } catch (err: any) {
      console.error('❌ Status update failed:', err);
      setTasks(previous); // rollback
      toast.error(err.message || 'Status update failed');
    }
  };

  // -------------------- FILTER --------------------
  const filteredTasks =
    filter === 'all'
      ? tasks
      : tasks.filter(t => t.status === filter);

  // 🔥 FIX: Use useMemo to recalculate counts when tasks change
  const filterButtons = useMemo(() => {
    const counts = {
      all: tasks.length,
      todo: tasks.filter(t => t.status === 'todo').length,
      inProgress: tasks.filter(t => t.status === 'in-progress').length,
      completed: tasks.filter(t => t.status === 'completed').length,
    };

    console.log('🔢 Filter counts updated:', counts);

    return [
      { label: 'All', value: 'all', count: counts.all },
      { label: 'To Do', value: 'todo', count: counts.todo },
      { label: 'In Progress', value: 'in-progress', count: counts.inProgress },
      { label: 'Completed', value: 'completed', count: counts.completed },
    ];
  }, [tasks]); // 🔑 This will recalculate whenever tasks change

  // -------------------- UI --------------------
  if (loading) {
    return <div className="p-10 text-center">Loading...</div>;
  }

  return (
    <div className="min-h-screen">
      <Navbar />

      <main className="pt-24 px-6">
        {/* Header */}
        <div className="flex justify-between mb-6">
          <h1 className="text-4xl font-bold">My Tasks</h1>
          <button
            className="btn-premium"
            onClick={() => {
              setEditingTask(null);
              setShowForm(true);
            }}
          >
            + New Task
          </button>
        </div>

        {/* Filters */}
        <div className="flex gap-2 mb-6">
          {filterButtons.map(btn => (
            <button
              key={btn.value}
              onClick={() => setFilter(btn.value as any)}
              className={`px-4 py-2 rounded ${
                filter === btn.value ? 'bg-primary' : 'bg-secondary'
              }`}
            >
              {btn.label} ({btn.count})
            </button>
          ))}
        </div>

        {/* Tasks */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {filteredTasks.map(task => (
            <TaskCard
              key={task.id}
              task={task}
              onEdit={t => {
                setEditingTask(t);
                setShowForm(true);
              }}
              onDelete={handleDeleteTask}
              onStatusChange={handleStatusChange}
            />
          ))}
        </div>
      </main>

      {showForm && (
        <TaskForm
          task={editingTask}
          onSubmit={data =>
            editingTask
              ? handleUpdateTask(editingTask.id, data)
              : handleCreateTask(data)
          }
          onClose={() => {
            setShowForm(false);
            setEditingTask(null);
          }}
        />
      )}
    </div>
  );
}