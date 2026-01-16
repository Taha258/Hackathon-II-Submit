"use client"
import { motion, useScroll, useTransform } from "framer-motion"
import { useEffect, useState } from "react"
import { ArrowRight, Sparkles, Zap, Shield, Clock, Star, Users, TrendingUp, CheckCircle2, Rocket, Target, Award, Moon, Sun } from "lucide-react"

export default function LandingPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [isDark, setIsDark] = useState(true)
  const { scrollYProgress } = useScroll()
  const y = useTransform(scrollYProgress, [0, 1], [0, -100])

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) setIsLoggedIn(true)
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setIsLoggedIn(false)
    window.location.href = '/'
  }

  const features = [
    {
      icon: Zap,
      title: "Lightning Fast",
      description: "Blazing fast performance with optimized workflows that save you hours every day",
      gradient: "from-yellow-400 to-orange-500",
      glow: "shadow-[0_0_50px_rgba(251,191,36,0.3)]"
    },
    {
      icon: Shield,
      title: "Secure & Private",
      description: "Enterprise-grade security with end-to-end encryption for all your data",
      gradient: "from-blue-400 to-cyan-500",
      glow: "shadow-[0_0_50px_rgba(34,211,238,0.3)]"
    },
    {
      icon: Clock,
      title: "Real-time Sync",
      description: "Instant updates across all devices with seamless collaboration features",
      gradient: "from-purple-400 to-pink-500",
      glow: "shadow-[0_0_50px_rgba(168,85,247,0.3)]"
    },
  ]

  const stats = [
    { icon: Users, value: "50K+", label: "Active Users", color: "text-blue-400" },
    { icon: Star, value: "4.9", label: "App Rating", color: "text-yellow-400" },
    { icon: TrendingUp, value: "99.9%", label: "Uptime", color: "text-green-400" },
  ]

  const benefits = [
    "Unlimited Projects & Tasks",
    "Advanced Analytics Dashboard",
    "Team Collaboration Tools",
    "Priority Support 24/7",
    "Custom Integrations",
    "Mobile Apps (iOS & Android)"
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 text-white overflow-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 -z-10">
        <motion.div
          animate={{ scale: [1, 1.2, 1], rotate: [0, 90, 0] }}
          transition={{ duration: 20, repeat: Infinity }}
          className="absolute top-20 -left-20 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl"
        />
        <motion.div
          animate={{ scale: [1.2, 1, 1.2], rotate: [90, 0, 90] }}
          transition={{ duration: 25, repeat: Infinity }}
          className="absolute bottom-20 -right-20 w-96 h-96 bg-pink-500/20 rounded-full blur-3xl"
        />
        <motion.div
          animate={{ scale: [1, 1.3, 1] }}
          transition={{ duration: 15, repeat: Infinity }}
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-500/10 rounded-full blur-3xl"
        />
      </div>

      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50 backdrop-blur-xl border-b border-white/10 bg-slate-950/50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center gap-3"
          >
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-purple-600 to-pink-600 flex items-center justify-center shadow-lg shadow-purple-500/50">
              <Sparkles className="text-white w-6 h-6" />
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-white to-purple-300 bg-clip-text text-transparent">
              TaskFlow
            </span>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center gap-4"
          >
            {/* Theme Toggle */}
            <button
              onClick={() => setIsDark(!isDark)}
              className="p-2.5 rounded-full backdrop-blur-xl border border-white/10 hover:bg-white/5 transition-all"
            >
              {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>

            {isLoggedIn ? (
              <>
                <a href="/tasks">
                  <button className="px-6 py-2.5 rounded-full backdrop-blur-xl border border-white/10 hover:bg-white/5 transition-all">
                    My Tasks
                  </button>
                </a>
                <button 
                  onClick={handleLogout}
                  className="px-6 py-2.5 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 hover:shadow-lg hover:shadow-purple-500/50 transition-all font-semibold"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <a href="/login">
                  <button className="px-6 py-2.5 rounded-full backdrop-blur-xl border border-white/10 hover:bg-white/5 transition-all">
                    Sign In
                  </button>
                </a>
                <a href="/signup">
                  <button className="px-8 py-2.5 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 hover:shadow-lg hover:shadow-purple-500/50 transition-all font-semibold">
                    Get Started Free
                  </button>
                </a>
              </>
            )}
          </motion.div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6 relative">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-500/10 border border-purple-500/20 backdrop-blur-xl mb-8">
              <Rocket className="w-4 h-4 text-purple-400" />
              <span className="text-sm text-purple-300">Now with AI-powered insights</span>
            </div>

            <h1 className="text-7xl md:text-8xl lg:text-9xl font-black mb-6 leading-tight">
              <span className="block bg-gradient-to-r from-white via-purple-200 to-white bg-clip-text text-transparent">
                Build Your
              </span>
              <span className="block bg-gradient-to-r from-purple-400 via-pink-400 to-purple-400 bg-clip-text text-transparent">
                Dream Projects
              </span>
            </h1>

            <p className="text-xl md:text-2xl text-purple-200/80 max-w-3xl mx-auto mb-12 leading-relaxed">
              The most powerful task management platform designed for ambitious teams who want to achieve more.
            </p>

            <div className="flex flex-wrap justify-center gap-4 mb-16">
              {isLoggedIn ? (
                <a href="/tasks">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="px-10 py-5 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 text-white text-lg font-bold flex items-center gap-3 shadow-2xl shadow-purple-500/50"
                  >
                    Go to Dashboard <ArrowRight className="w-5 h-5" />
                  </motion.button>
                </a>
              ) : (
                <>
                  <a href="/signup">
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      className="px-10 py-5 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 text-white text-lg font-bold flex items-center gap-3 shadow-2xl shadow-purple-500/50"
                    >
                      Start Free Trial <ArrowRight className="w-5 h-5" />
                    </motion.button>
                  </a>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="px-10 py-5 rounded-full backdrop-blur-xl border border-white/20 text-white text-lg font-bold hover:bg-white/5 transition-all"
                  >
                    Watch Demo
                  </motion.button>
                </>
              )}
            </div>
          </motion.div>

          {/* Stats */}
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto"
          >
            {stats.map((stat, i) => (
              <motion.div
                key={i}
                whileHover={{ scale: 1.05, y: -5 }}
                className="backdrop-blur-xl bg-white/5 border border-white/10 rounded-3xl p-8 hover:shadow-xl hover:shadow-purple-500/20 transition-all"
              >
                <stat.icon className={`mx-auto ${stat.color} mb-3 w-10 h-10`} />
                <div className="text-5xl font-black mb-2">{stat.value}</div>
                <div className="text-purple-300">{stat.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-28 px-6">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-5xl md:text-6xl font-black mb-6">
              <span className="bg-gradient-to-r from-white to-purple-300 bg-clip-text text-transparent">
                Why Choose TaskFlow?
              </span>
            </h2>
            <p className="text-xl text-purple-200/70 max-w-2xl mx-auto">
              Everything you need to manage projects efficiently
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                whileHover={{ scale: 1.05, y: -10 }}
                className={`backdrop-blur-xl bg-white/5 border border-white/10 rounded-3xl p-10 hover:${feature.glow} transition-all duration-300 group`}
              >
                <div className={`w-20 h-20 rounded-2xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform shadow-lg`}>
                  <feature.icon className="text-white w-10 h-10" />
                </div>
                <h3 className="text-2xl font-bold mb-4">{feature.title}</h3>
                <p className="text-purple-200/70 leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-28 px-6 relative">
        <div className="max-w-5xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="backdrop-blur-xl bg-gradient-to-br from-purple-500/10 to-pink-500/10 border border-white/10 rounded-3xl p-12 md:p-16"
          >
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div>
                <h2 className="text-5xl font-black mb-6">
                  <span className="bg-gradient-to-r from-white to-purple-300 bg-clip-text text-transparent">
                    Everything Included
                  </span>
                </h2>
                <p className="text-xl text-purple-200/70 mb-8">
                  All the features you need to succeed, with no hidden costs
                </p>
                <div className="space-y-4">
                  {benefits.map((benefit, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: -20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: i * 0.1 }}
                      className="flex items-center gap-3"
                    >
                      <CheckCircle2 className="w-6 h-6 text-green-400 flex-shrink-0" />
                      <span className="text-lg text-purple-100">{benefit}</span>
                    </motion.div>
                  ))}
                </div>
              </div>
              <div className="relative">
                <motion.div
                  animate={{ y: [0, -20, 0] }}
                  transition={{ duration: 3, repeat: Infinity }}
                  className="w-full aspect-square rounded-3xl bg-gradient-to-br from-purple-600/20 to-pink-600/20 backdrop-blur-xl border border-white/10 flex items-center justify-center"
                >
                  <Award className="w-32 h-32 text-purple-400" />
                </motion.div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-28 px-6">
        <div className="max-w-5xl mx-auto">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="backdrop-blur-xl bg-gradient-to-br from-purple-600/20 to-pink-600/20 border border-white/20 rounded-3xl p-16 text-center shadow-2xl shadow-purple-500/20"
          >
            <Sparkles className="mx-auto text-purple-400 w-16 h-16 mb-6" />
            <h2 className="text-5xl md:text-6xl font-black mb-6">
              <span className="bg-gradient-to-r from-white to-purple-300 bg-clip-text text-transparent">
                Ready to Get Started?
              </span>
            </h2>
            <p className="text-xl text-purple-200/70 mb-10 max-w-2xl mx-auto">
              Join thousands of professionals who trust TaskFlow to manage their projects efficiently
            </p>
            
            {isLoggedIn ? (
              <a href="/tasks">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-12 py-6 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 text-white text-xl font-bold shadow-2xl shadow-purple-500/50"
                >
                  View Your Tasks
                </motion.button>
              </a>
            ) : (
              <a href="/signup">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-12 py-6 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 text-white text-xl font-bold shadow-2xl shadow-purple-500/50"
                >
                  Start Free Trial Today
                </motion.button>
              </a>
            )}

            <p className="text-sm text-purple-300/70 mt-6">
              No credit card required • 14-day free trial • Cancel anytime
            </p>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-white/10 text-center">
        <div className="max-w-7xl mx-auto px-6">
          <p className="text-purple-300/70">
            © 2026 TaskFlow. Built with 💜 by amazing developers
          </p>
        </div>
      </footer>
    </div>
  )
}