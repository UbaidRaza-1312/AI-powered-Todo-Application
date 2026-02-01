// frontend/src/components/TaskManager/TaskItem.tsx

import React, { useState } from 'react';
import TaskService, { Task } from '../../services/taskService';
import { toast } from 'react-toastify';

interface TaskItemProps {
  task: Task;
  onTaskUpdated: (updatedTask: Task) => void;
  onTaskDeleted: (taskId: string) => void;
  onToggleCompletion: (taskId: string) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onTaskUpdated, onTaskDeleted, onToggleCompletion }) => {
  const [isEditing, setIsEditing] = useState<boolean>(false);
  const [title, setTitle] = useState<string>(task.title);
  const [description, setDescription] = useState<string>(task.description || '');

  const handleSave = async () => {
    try {
      const updatedTask = await TaskService.updateTask(task.id, {
        title: title || task.title,
        description: description || task.description,
        completed: task.completed, // Preserve the completed status
        due_date: task.due_date, // Send the due date value
      });
      onTaskUpdated(updatedTask);
      setIsEditing(false);
      toast.info(`"${updatedTask.title}" updated successfully!`, {
        position: "top-center",
        autoClose: 2000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        theme: "colored",
        style: {
          backgroundColor: '#3b82f6', // Blue background
          color: 'white',             // White text
          borderRadius: '8px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
        }
      });
    } catch (err) {
      console.error('Failed to update task:', err);
      toast.error('Failed to update task. Please try again.', {
        position: "top-center",
        autoClose: 3000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        theme: "colored",
        style: {
          backgroundColor: '#ef4444', // Red background
          color: 'white',             // White text
          borderRadius: '8px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
        }
      });
    }
  };

  const handleCancel = () => {
    // Reset to original values
    setTitle(task.title);
    setDescription(task.description || '');
    setIsEditing(false);
  };

  const handleDelete = async () => {
    try {
      await TaskService.deleteTask(task.id);
      onTaskDeleted(task.id);
      toast.success(`"${task.title}" has been deleted successfully!`, {
        position: "top-center",
        autoClose: 2000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        theme: "colored",
        style: {
          backgroundColor: '#10b981', // Green background
          color: 'white',             // White text
          borderRadius: '8px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
        }
      });
    } catch (err) {
      console.error('Failed to delete task:', err);
      toast.error('Failed to delete task. Please try again.', {
        position: "top-center",
        autoClose: 3000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        theme: "colored",
        style: {
          backgroundColor: '#ef4444', // Red background
          color: 'white',             // White text
          borderRadius: '8px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
        }
      });
    }
  };


  const handleToggleCompletion = async () => {
    try {
      const updatedTask = await TaskService.toggleTaskCompletion(task.id);
      onTaskUpdated(updatedTask);
      toast.info(`"${updatedTask.title}" ${updatedTask.completed ? 'completed' : 'marked as pending'}!`, {
        position: "top-center",
        autoClose: 2000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        theme: "colored",
        style: {
          backgroundColor: '#8b5cf6', // Purple background
          color: 'white',             // White text
          borderRadius: '8px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
        }
      });
    } catch (err) {
      console.error('Failed to update task completion:', err);
      toast.error('Failed to update task completion. Please try again.', {
        position: "top-center",
        autoClose: 3000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        theme: "colored",
        style: {
          backgroundColor: '#ef4444', // Red background
          color: 'white',             // White text
          borderRadius: '8px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
        }
      });
    }
  };

  // Define the fadeIn animation style
  const fadeInStyle = {
    animation: 'fadeIn 0.3s ease-out forwards'
  };

  // Add the keyframes to the document
  React.useEffect(() => {
    const style = document.createElement('style');
    style.innerHTML = `
      @keyframes fadeIn {
        from {
          opacity: 0;
          transform: translateY(10px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }
    `;
    document.head.appendChild(style);

    return () => {
      document.head.removeChild(style);
    };
  }, []);

  return (
    <div className={`
      bg-gray-800/60 backdrop-blur-sm border border-gray-700/50 rounded-xl p-5 transition-all duration-300 ease-in-out
      hover:shadow-lg hover:shadow-blue-500/10 hover:border-blue-500/30 hover:-translate-y-0.5
      ${task.completed ? 'opacity-70' : ''}
    `}>
      {isEditing ? (
        <div className="space-y-4" style={fadeInStyle}>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full p-3 bg-gray-700/50 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Task title"
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full p-3 bg-gray-700/50 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Task description"
            rows={3}
          />
          <div className="flex space-x-3 pt-2">
            <button
              onClick={handleSave}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors duration-200"
            >
              Save
            </button>
            <button
              onClick={handleCancel}
              className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors duration-200"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div style={fadeInStyle}>
          <div className="flex items-start">
            <div
              onClick={handleToggleCompletion}
              className={`
                mt-1 w-6 h-6 rounded-full border-2 flex items-center justify-center cursor-pointer transition-colors duration-300
                ${task.completed
                  ? 'bg-green-500 border-green-500'
                  : 'border-gray-400 bg-transparent hover:border-gray-300'}
              `}
            >
              {task.completed && (
                <svg
                  className="w-4 h-4 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7"></path>
                </svg>
              )}
            </div>
            <div className="flex-1 ml-3 flex justify-between items-start">
              <div>
                <h3 className={`text-lg font-medium ${task.completed ? 'line-through text-gray-400' : 'text-white'}`}>
                  {task.title}
                </h3>
                {task.description && (
                  <p className="text-gray-300 mt-2">{task.description}</p>
                )}
                <div className="flex flex-wrap gap-2 mt-3">
                  <span className="px-3 py-1 bg-gray-700/50 text-gray-300 rounded-full text-xs font-medium border border-gray-600/50">
                    Created: {new Date(task.created_at).toLocaleDateString()}
                  </span>
                  {task.updated_at && Math.abs(new Date(task.updated_at).getTime() - new Date(task.created_at).getTime()) > 1000 &&
                    <span className="px-3 py-1 bg-blue-900/50 text-blue-300 rounded-full text-xs font-medium border border-blue-800/50">
                      Updated: {new Date(task.updated_at).toLocaleDateString()}
                    </span>
                  }
                </div>
              </div>
              <div className={`
                px-3 py-1 rounded-full text-xs font-medium
                ${task.completed
                  ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                  : 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'}
              `}>
                {task.completed ? 'Complete' : 'Pending'}
              </div>
            </div>
          </div>
          <div className="flex justify-end space-x-2 mt-4">
            <button
              onClick={() => setIsEditing(true)}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors duration-200 text-sm"
            >
              Edit
            </button>
            <button
              onClick={handleDelete}
              className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors duration-200 text-sm"
            >
              Delete
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskItem;