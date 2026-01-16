// frontend\src\components\TaskCard.tsx
import { useState } from 'react';
import { Task } from '../lib/types';
import { Trash2, Edit, Clock, Calendar } from 'lucide-react';

interface TaskCardProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
  onStatusChange: (id: string, status: Task['status']) => void;
}

export default function TaskCard({ task, onEdit, onDelete, onStatusChange }: TaskCardProps) {
  const [isUpdating, setIsUpdating] = useState(false);
  
  if (!task) return null;

  const status = task.status || 'todo';
  const priority = task.priority || 'medium';

  const priorityColors: Record<string, string> = {
    low: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    medium: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
    high: 'bg-red-500/10 text-red-400 border-red-500/20',
  };

  const statusColors: Record<string, string> = {
    'todo': 'bg-gray-500/10 text-gray-400',
    'in-progress': 'bg-purple-500/10 text-purple-400',
    'completed': 'bg-green-500/10 text-green-400',
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return null;
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    } catch {
      return null;
    }
  };

  const getStatusLabel = (status: string) => status.replace('-', ' ');

  const handleStatusClick = async (newStatus: Task['status']) => {
    setIsUpdating(true);
    console.log(`🔘 Button clicked: ${newStatus}`);
    try {
      await onStatusChange(task.id, newStatus);
    } catch (error) {
      console.error('Button click error:', error);
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <div className="glass-card p-6 hover-card-effect group relative">
      {/* Loading Overlay */}
      {isUpdating && (
        <div className="absolute inset-0 bg-black/20 rounded-lg flex items-center justify-center z-10">
          <div className="text-sm text-white">Updating...</div>
        </div>
      )}

      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-bold mb-2 group-hover:text-primary transition-colors">
            {task.title || 'Untitled Task'}
          </h3>
          {task.description && (
            <p className="text-muted-foreground text-sm line-clamp-2">{task.description}</p>
          )}
        </div>

        {/* Actions */}
        <div className="flex gap-2 ml-4">
          <button
            onClick={() => onEdit(task)}
            disabled={isUpdating}
            className="p-2 rounded-lg hover:bg-primary/10 text-muted-foreground hover:text-primary transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            title="Edit task"
          >
            <Edit className="w-4 h-4" />
          </button>
          <button
            onClick={() => onDelete(task.id)}
            disabled={isUpdating}
            className="p-2 rounded-lg hover:bg-destructive/10 text-muted-foreground hover:text-destructive transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            title="Delete task"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Metadata */}
      <div className="flex flex-wrap items-center gap-2 mb-4">
        <span className={`px-3 py-1 rounded-full text-xs font-medium capitalize ${statusColors[status] || statusColors.todo}`}>
          {getStatusLabel(status)}
        </span>
        {task.priority && (
          <span className={`px-3 py-1 rounded-full text-xs font-medium border capitalize ${priorityColors[priority]}`}>
            {priority}
          </span>
        )}
        {task.dueDate && formatDate(task.dueDate) && (
          <div className="flex items-center gap-1 text-xs text-muted-foreground">
            <Calendar className="w-3 h-3" />
            <span>{formatDate(task.dueDate)}</span>
          </div>
        )}
      </div>

      {/* Status Buttons */}
      <div className="flex gap-2">
        {status !== 'todo' && (
          <button
            onClick={() => handleStatusClick('todo')}
            disabled={isUpdating}
            className="flex-1 px-3 py-2 rounded-lg text-xs font-medium bg-gray-500/10 hover:bg-gray-500/20 text-gray-400 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isUpdating ? '...' : 'To Do'}
          </button>
        )}
        {status !== 'in-progress' && (
          <button
            onClick={() => handleStatusClick('in-progress')}
            disabled={isUpdating}
            className="flex-1 px-3 py-2 rounded-lg text-xs font-medium bg-purple-500/10 hover:bg-purple-500/20 text-purple-400 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isUpdating ? '...' : 'In Progress'}
          </button>
        )}
        {status !== 'completed' && (
          <button
            onClick={() => handleStatusClick('completed')}
            disabled={isUpdating}
            className="flex-1 px-3 py-2 rounded-lg text-xs font-medium bg-green-500/10 hover:bg-green-500/20 text-green-400 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isUpdating ? '...' : 'Complete'}
          </button>
        )}
      </div>

      {/* Created Date Footer */}
      {task.created_at && formatDate(task.created_at) && (
        <div className="flex items-center gap-1 text-xs text-muted-foreground mt-4 pt-4 border-t border-border/50">
          <Clock className="w-3 h-3" />
          <span>Created {formatDate(task.created_at)}</span>
        </div>
      )}
    </div>
  );
}