'use client';

import React from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  const handleStartClick = () => {
    router.push('/auth/login');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-violet-900 flex flex-col">
      
      {/* HERO SECTION */}
      <div className="flex-grow flex items-center justify-center px-4 py-12">
        <div className="max-w-4xl w-full text-center">
          <h1 className="text-6xl md:text-7xl font-bold text-blue-300 mb-6">
            TaskMaster
          </h1>

          <p className="text-2xl md:text-3xl text-indigo-100 mb-10 max-w-3xl mx-auto">
            Transform your daily routine with our cutting-edge task management platform. Achieve more with less stress.
          </p>

          <button
            onClick={handleStartClick}
            className="bg-indigo-500 hover:bg-indigo-600 text-white font-bold py-4 px-10 rounded-full text-xl transition-all duration-300 transform hover:scale-105 shadow-lg shadow-indigo-400/40"
          >
            Start Free
          </button>
        </div>
      </div>

      {/* FEATURES SECTION */}
      <div className="py-20 px-4 bg-black/20">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-center text-white mb-16">Revolutionary Tools for Peak Performance</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
            <FeatureCard title="Smart Organization" desc="Categorize and prioritize tasks with intelligent tagging systems. Streamline your workflow with smart categorization." />
            <FeatureCard title="Progress Analytics" desc="Track your productivity trends with detailed reports. Understand your patterns and optimize your performance." />
            <FeatureCard title="Privacy First" desc="Enterprise-grade security keeps your data completely safe. Your privacy is our top priority." />
          </div>
        </div>
      </div>

      {/* AI ASSISTANT SECTION */}
      <div className="py-20 px-4 bg-gradient-to-r from-indigo-900/50 to-purple-900/50 border-t border-gray-600/40">
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-8">Advanced AI Companion</h2>
          <p className="text-gray-200 text-xl max-w-3xl mx-auto mb-6">
            Our sophisticated AI understands your needs and helps you stay ahead of your schedule.
            Experience the future of task management with intelligent automation.
          </p>
          <p className="text-gray-200 text-xl max-w-3xl mx-auto mb-16">
            Simply speak or type your tasks naturally, and our AI will organize everything for you.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <FeatureMini title="Smart Recognition" desc="Identifies patterns in your workflow automatically." />
            <FeatureMini title="Personalized Tips" desc="Provides tailored advice for maximum efficiency." />
            <FeatureMini title="Adaptive Learning" desc="Evolves with your habits to become more helpful." />
          </div>
        </div>
      </div>

      {/* WHY CHOOSE US */}
      <div className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-center text-white mb-16">Why TaskMaster Stands Apart?</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div>
              <h3 className="text-3xl font-bold text-indigo-200 mb-6">Maximize Your Efficiency</h3>
              <p className="text-gray-200 text-lg mb-6">
                Our innovative platform combines simplicity with powerful capabilities for optimal results.
                With intelligent scheduling and smart notifications, you'll stay ahead of your commitments.
              </p>
              <p className="text-gray-200 text-lg">
                Collaborate effortlessly with team members and monitor project progress in real-time.
                Boost your efficiency by up to 50% with our advanced workflow solutions.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-6">
              <Stat label="Reliability Rate" value="99.9%" color="text-green-300" />
              <Stat label="Expert Support" value="24/7" color="text-blue-300" />
              <Stat label="Basic Plan" value="Free" color="text-purple-300" />
              <Stat label="On All Devices" value="Works" color="text-yellow-300" />
            </div>
          </div>
        </div>
      </div>

      {/* FOOTER */}
      <footer className="py-8 text-center text-gray-300 bg-gray-800/70 backdrop-blur-md border-t border-gray-600/50">
        <p className="text-lg">© {new Date().getFullYear()} TaskMaster Pro. All rights reserved.</p>
      </footer>
    </div>
  );
}

/* COMPONENTS */

function FeatureCard({ title, desc }) {
  return (
    <div className="bg-gray-800/60 backdrop-blur-sm border border-gray-600/50 rounded-xl p-8 shadow-xl transition-all duration-300 hover:scale-105 hover:bg-gray-700/70 hover:border-indigo-500/50">
      <h3 className="text-2xl font-bold text-white mb-3">{title}</h3>
      <p className="text-gray-200 text-lg">{desc}</p>
    </div>
  );
}

function FeatureMini({ title, desc }) {
  return (
    <div className="bg-gray-800/60 border border-gray-600/50 rounded-xl p-8 transition-all duration-300 hover:scale-105 hover:bg-gray-700/70 hover:border-indigo-500/50">
      <h3 className="text-indigo-300 font-semibold text-xl mb-3">{title}</h3>
      <p className="text-gray-300 text-base">{desc}</p>
    </div>
  );
}

function Stat({ label, value, color }) {
  return (
    <div className="bg-gray-800/60 backdrop-blur-sm border border-gray-600/50 rounded-xl p-6 shadow-xl">
      <div className={`${color} text-4xl font-bold mb-3`}>{value}</div>
      <div className="text-gray-200 text-base">{label}</div>
    </div>
  );
}
