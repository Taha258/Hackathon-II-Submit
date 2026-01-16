//frontend\src\components\TaskForm.tsx
'use client';

import { useState, useEffect } from 'react';
import { Task } from '../lib/types';
import { X } from 'lucide-react';

interface TaskFormProps {
  task?: Task | null;
  onSubmit: (taskData: { title: string; description?: string; status?: Task['status']; priority?: Task['priority']; dueDate?: string }) => void;
  onClose: () => void;
}

export default function TaskForm({ task, onSubmit, onClose }: TaskFormProps) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    status: 'todo' as Task['status'],
    priority: 'medium' as Task['priority'],
    dueDate: '',
  });

  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title || '',
        description: task.description || '',
        status: task.status || 'todo',
        priority: task.priority || 'medium',
        dueDate: task.dueDate || '',
      });
    }
  }, [task]);

  const handleChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.title.trim()) return;
    onSubmit({ ...formData, title: formData.title.trim() });
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="glass-card max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-6 pb-4 border-b border-border/50">
          <h2 className="text-2xl font-bold gradient-text">{task ? 'Edit Task' : 'Create New Task'}</h2>
          <button onClick={onClose} className="p-2 rounded-lg hover:bg-secondary/50 transition-colors"><X className="w-5 h-5" /></button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium mb-2">Title <span className="text-destructive">*</span></label>
            <input type="text" value={formData.title} onChange={(e) => handleChange('title', e.target.value)} required className="w-full px-4 py-3 rounded-lg bg-secondary/30 border border-border/50 focus:border-primary focus:outline-none transition-colors" />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Description</label>
            <textarea value={formData.description} onChange={(e) => handleChange('description', e.target.value)} rows={4} className="w-full px-4 py-3 rounded-lg bg-secondary/30 border border-border/50 focus:border-primary focus:outline-none transition-colors resize-none" />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Status</label>
              <select value={formData.status} onChange={(e) => handleChange('status', e.target.value)} className="w-full px-4 py-3 rounded-lg bg-secondary/30 border border-border/50 focus:border-primary focus:outline-none transition-colors">
                <option value="todo">To Do</option>
                <option value="in-progress">In Progress</option>
                <option value="completed">Completed</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Priority</label>
              <select value={formData.priority} onChange={(e) => handleChange('priority', e.target.value)} className="w-full px-4 py-3 rounded-lg bg-secondary/30 border border-border/50 focus:border-primary focus:outline-none transition-colors">
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Due Date</label>
            <input type="date" value={formData.dueDate} onChange={(e) => handleChange('dueDate', e.target.value)} className="w-full px-4 py-3 rounded-lg bg-secondary/30 border border-border/50 focus:border-primary focus:outline-none transition-colors" />
          </div>

          <div className="flex gap-3 pt-4">
            <button type="button" onClick={onClose} className="flex-1 px-6 py-3 rounded-lg bg-secondary/30 hover:bg-secondary/50 transition-colors font-medium">Cancel</button>
            <button type="submit" className="flex-1 btn-premium">{task ? 'Update Task' : 'Create Task'}</button>
          </div>
        </form>
      </div>
    </div>
  );
}
