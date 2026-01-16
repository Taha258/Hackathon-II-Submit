'use client';

import { useState, useEffect } from 'react';
import Navbar from '../../components/Navbar';
import ChatWidget from '../../components/ChatWidget';
import { Task, TaskStats } from '../../lib/types';
import { taskAPI } from '../../lib/api';
import toast from 'react-hot-toast';
import Link from 'next/link';

export default function DashboardPage() {
  const [stats, setStats] = useState<TaskStats>({
    total: 0,
    completed: 0,
    inProgress: 0,
    todo: 0,
  });
  const [recentTasks, setRecentTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const tasks: Task[] = await taskAPI.getTasks();

      const newStats = {
        total: tasks.length,
        completed: tasks.filter(t => t.status === 'completed').length,
        inProgress: tasks.filter(t => t.status === 'in-progress').length,
        todo: tasks.filter(t => t.status === 'todo').length,
      };

      setStats(newStats);
      setRecentTasks(tasks.slice(0, 5));
    } catch (error: any) {
      console.error(error);
      toast.error(error.message || 'Failed to load dashboard');
    } finally {
      setLoading(false);
    }
  };

  const statsCards = [
    { title: 'Total Tasks', value: stats.total, icon: '📋' },
    { title: 'Completed', value: stats.completed, icon: '✅' },
    { title: 'In Progress', value: stats.inProgress, icon: '⚡' },
    { title: 'To Do', value: stats.todo, icon: '📝' },
  ];

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading dashboard...</p>
      </div>
    );
  }

  return (
    <>
      <div className="min-h-screen">
        <Navbar />

        <main className="pt-24 pb-12 px-4 max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold mb-6">Dashboard</h1>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-10">
            {statsCards.map(card => (
              <div key={card.title} className="p-4 border rounded-xl">
                <div className="text-2xl">{card.icon}</div>
                <div className="text-xl font-bold">{card.value}</div>
                <div className="text-sm text-gray-500">{card.title}</div>
              </div>
            ))}
          </div>

          {/* Recent Tasks */}
          <div className="border rounded-xl p-6 mb-10">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">Recent Tasks</h2>
              <Link href="/tasks" className="text-blue-500 text-sm">
                View All →
              </Link>
            </div>

            {recentTasks.length > 0 ? (
              <div className="space-y-3">
                {recentTasks.map(task => (
                  <div key={task.id} className="p-3 border rounded">
                    <div className="flex justify-between">
                      <span>{task.title}</span>
                      <span className="text-sm text-gray-500">{task.status}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-6">
                <p className="text-gray-500 mb-3">No tasks yet</p>
                <Link
                  href="/tasks"
                  className="px-4 py-2 bg-blue-600 text-white rounded"
                >
                  Create Your First Task
                </Link>
              </div>
            )}
          </div>

          {/* Quick Actions */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Link
              href="/tasks"
              className="border rounded-xl p-6 text-center hover:bg-gray-50"
            >
              <div className="text-3xl mb-2">➕</div>
              <h3 className="font-bold">Create New Task</h3>
            </Link>

            <div className="border rounded-xl p-6 text-center">
              <div className="text-3xl mb-2">📊</div>
              <h3 className="font-bold">View Analytics</h3>
            </div>
          </div>
        </main>
      </div>

      <ChatWidget />
    </>
  );
}
