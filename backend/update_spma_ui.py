import os

html_code = '''<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Smart Project Manager Assistant (SPMA) - Blue Nile University</title>
  <!-- Tailwind CSS, Lucide Icons, Marked -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Inter:wght@400;500;600;700;800;900&display=swap');
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: #F8FAFC;
      color: #0F172A;
    }
    html[dir="rtl"] body {
      font-family: 'Cairo', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .custom-scrollbar::-webkit-scrollbar {
      width: 5px;
      height: 5px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: transparent;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: #CBD5E1;
      border-radius: 4px;
    }
    .custom-scrollbar-dark::-webkit-scrollbar {
      width: 4px;
    }
    .custom-scrollbar-dark::-webkit-scrollbar-track {
      background: transparent;
    }
    .custom-scrollbar-dark::-webkit-scrollbar-thumb {
      background: #334155;
      border-radius: 4px;
    }
    .tabular-nums {
      font-variant-numeric: tabular-nums;
    }
    .markdown-content {
      direction: auto;
      unicode-bidi: plaintext;
    }
    .markdown-content table {
      width: 100%;
      border-collapse: collapse;
      margin: 10px 0;
    }
    .markdown-content th, .markdown-content td {
      border: 1px solid #E2E8F0;
      padding: 6px 10px;
    }
    .markdown-content th {
      background: #F8FAFC;
      color: #1E293B;
      font-weight: 700;
    }
    .blueprint-pattern {
      background-color: #061124;
      background-image: 
        radial-gradient(rgba(59, 130, 246, 0.15) 1px, transparent 0),
        linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
      background-size: 24px 24px, 48px 48px, 48px 48px;
    }
    .pulse-glow {
      box-shadow: 0 0 25px rgba(16, 185, 129, 0.35);
    }
    .hero-glow {
      background: radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.25) 0%, transparent 70%);
    }
  </style>
  <link rel="manifest" href="/static/manifest.json">
  <meta name="theme-color" content="#0B1E3B">
</head>
<body class="h-screen w-screen overflow-hidden select-none bg-[#F8FAFC]">

  <!-- ========================================================================= -->
  <!-- 1. STANDALONE LUXURY FULL-SCREEN LOGIN VIEW (DEDICATED LANDING & PORTAL)  -->
  <!-- ========================================================================= -->
  <div id="login-view" class="fixed inset-0 min-h-screen w-full z-50 flex flex-col justify-between blueprint-pattern text-slate-100 overflow-y-auto custom-scrollbar p-4 md:p-8">
    
    <!-- Top Bar of Login Page -->
    <header class="w-full max-w-7xl mx-auto flex items-center justify-between py-2 border-b border-slate-800/80">
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 bg-white rounded-2xl p-1.5 shadow-lg border border-slate-200/20 flex items-center justify-center shrink-0">
          <img src="/static/brand/blue_nile_logo.png" alt="University Logo" class="w-full h-full object-contain" />
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span class="text-[10px] font-extrabold tracking-widest text-indigo-400 uppercase">BLUE NILE UNIVERSITY</span>
            <span class="text-[9px] px-1.5 py-0.5 bg-indigo-950/80 border border-indigo-700/50 text-indigo-300 rounded font-bold">Faculty of Engineering</span>
          </div>
          <h1 class="text-sm font-black text-white tracking-wide">Smart Project Manager Assistant (SPMA)</h1>
        </div>
      </div>

      <div class="flex items-center gap-3">
        <div class="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-slate-900/80 border border-slate-800 rounded-full text-xs text-slate-300">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span class="text-[11px] font-semibold">Core AI Engine v6.4 Active</span>
        </div>

        <button type="button" onclick="toggleLanguage()" class="px-3.5 py-1.5 bg-slate-800/90 hover:bg-slate-700 text-white rounded-xl text-xs font-bold border border-slate-700 shadow-md transition flex items-center gap-1.5">
          <i data-lucide="globe" class="w-3.5 h-3.5 text-indigo-400"></i>
          <span id="login-lang-label">العربية (Arabic)</span>
        </button>
      </div>
    </header>

    <!-- Main Centerpiece: Split Showcase & Sign-In Card -->
    <main class="w-full max-w-7xl mx-auto my-auto py-6">
      <div class="bg-[#0B1E3B]/95 backdrop-blur-2xl rounded-3xl border border-slate-700/70 shadow-2xl overflow-hidden grid grid-cols-1 lg:grid-cols-12">
        
        <!-- LEFT COLUMN (7 Cols): Project Presentation, EVM Showcase & Team -->
        <div class="lg:col-span-7 p-6 md:p-10 flex flex-col justify-between space-y-6 relative border-b lg:border-b-0 lg:border-r border-slate-800">
          <div class="space-y-5">
            
            <!-- Badge & University Title -->
            <div class="space-y-2">
              <div class="inline-flex items-center gap-2 px-3 py-1 bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-black rounded-full uppercase tracking-wider">
                <i data-lucide="graduation-cap" class="w-3.5 h-3.5"></i>
                <span id="i18n-login-thesis-badge">B.Sc. Graduation Research Thesis • 2026</span>
              </div>
              <h2 id="i18n-login-main-title" class="text-2xl md:text-3xl font-black text-white leading-tight tracking-tight">
                Smart Project Manager Assistant <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-emerald-400">(SPMA)</span>
              </h2>
              <p id="i18n-login-main-desc" class="text-xs md:text-sm text-slate-300 leading-relaxed max-w-2xl font-normal">
                Next-generation civil project intelligence combining Earned Value Management (EVM), Primavera XER schedule tracking, Multimodal Vision site inspections, and bilingual voice-driven AI agents.
              </p>
            </div>

            <!-- 6 Core Feature Highlights Grid -->
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5 pt-1">
              <div class="p-2.5 bg-slate-900/80 border border-slate-800 rounded-xl space-y-1">
                <div class="flex items-center gap-1.5 text-indigo-400">
                  <i data-lucide="trending-up" class="w-3.5 h-3.5"></i>
                  <span class="text-[11px] font-bold">EVM & S-Curve</span>
                </div>
                <p class="text-[10px] text-slate-400 leading-tight">Live SPI, CPI, SV, CV and critical path analytics.</p>
              </div>

              <div class="p-2.5 bg-slate-900/80 border border-slate-800 rounded-xl space-y-1">
                <div class="flex items-center gap-1.5 text-indigo-400">
                  <i data-lucide="bot" class="w-3.5 h-3.5"></i>
                  <span class="text-[11px] font-bold">Gemini 2.5 Agent</span>
                </div>
                <p class="text-[10px] text-slate-400 leading-tight">Zero-hallucination tools with verified calculation output.</p>
              </div>

              <div class="p-2.5 bg-slate-900/80 border border-slate-800 rounded-xl space-y-1">
                <div class="flex items-center gap-1.5 text-indigo-400">
                  <i data-lucide="mic" class="w-3.5 h-3.5"></i>
                  <span class="text-[11px] font-bold">Voice Processing</span>
                </div>
                <p class="text-[10px] text-slate-400 leading-tight">Bilingual Arabic & English site speech commands.</p>
              </div>

              <div class="p-2.5 bg-slate-900/80 border border-slate-800 rounded-xl space-y-1">
                <div class="flex items-center gap-1.5 text-indigo-400">
                  <i data-lucide="camera" class="w-3.5 h-3.5"></i>
                  <span class="text-[11px] font-bold">Vision Inspection</span>
                </div>
                <p class="text-[10px] text-slate-400 leading-tight">Site photo analysis and structural compliance checking.</p>
              </div>

              <div class="p-2.5 bg-slate-900/80 border border-slate-800 rounded-xl space-y-1">
                <div class="flex items-center gap-1.5 text-emerald-400">
                  <i data-lucide="phone-call" class="w-3.5 h-3.5"></i>
                  <span class="text-[11px] font-bold">WhatsApp Sync</span>
                </div>
                <p class="text-[10px] text-slate-400 leading-tight">Field logs, voice notes & auto-broadcast dispatching.</p>
              </div>

              <div class="p-2.5 bg-slate-900/80 border border-slate-800 rounded-xl space-y-1">
                <div class="flex items-center gap-1.5 text-amber-400">
                  <i data-lucide="file-check" class="w-3.5 h-3.5"></i>
                  <span class="text-[11px] font-bold">FIDIC & Reports</span>
                </div>
                <p class="text-[10px] text-slate-400 leading-tight">Official PDF/Excel generation and IPC monthly billing.</p>
              </div>
            </div>

            <!-- Graduation Project Team Card -->
            <div class="p-4 bg-slate-900/90 border border-indigo-900/40 rounded-2xl space-y-2.5 shadow-inner">
              <div class="flex items-center justify-between">
                <span id="i18n-login-team-head" class="text-[11px] font-extrabold text-indigo-300 uppercase tracking-wider flex items-center gap-1.5">
                  <i data-lucide="users" class="w-3.5 h-3.5"></i>
                  <span>Graduation Research Team (فريق إعداد المشروع)</span>
                </span>
                <span class="text-[10px] font-bold text-slate-400">Faculty of Engineering</span>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                <!-- Member 1 -->
                <div class="flex items-center gap-2 p-1.5 bg-slate-950/60 rounded-xl border border-slate-800">
                  <div class="w-7 h-7 rounded-lg bg-indigo-600 text-white font-black text-xs flex items-center justify-center shrink-0">AO</div>
                  <div class="overflow-hidden">
                    <p class="font-bold text-white text-[11px] truncate">Engr. Asem Othman</p>
                    <p class="text-[9px] text-indigo-300">Team Leader & Full-Stack Architect</p>
                  </div>
                </div>

                <!-- Member 2 -->
                <div class="flex items-center gap-2 p-1.5 bg-slate-950/60 rounded-xl border border-slate-800">
                  <div class="w-7 h-7 rounded-lg bg-slate-800 text-indigo-300 font-black text-xs flex items-center justify-center shrink-0">SM</div>
                  <div class="overflow-hidden">
                    <p class="font-bold text-white text-[11px] truncate">Engr. Saleh Mohammed</p>
                    <p class="text-[9px] text-slate-400">Planning & EVM Engine</p>
                  </div>
                </div>

                <!-- Member 3 -->
                <div class="flex items-center gap-2 p-1.5 bg-slate-950/60 rounded-xl border border-slate-800">
                  <div class="w-7 h-7 rounded-lg bg-slate-800 text-indigo-300 font-black text-xs flex items-center justify-center shrink-0">MG</div>
                  <div class="overflow-hidden">
                    <p class="font-bold text-white text-[11px] truncate">Engr. Mohammed Gassim</p>
                    <p class="text-[9px] text-slate-400">Site Operations & Execution</p>
                  </div>
                </div>

                <!-- Member 4 -->
                <div class="flex items-center gap-2 p-1.5 bg-slate-950/60 rounded-xl border border-slate-800">
                  <div class="w-7 h-7 rounded-lg bg-slate-800 text-indigo-300 font-black text-xs flex items-center justify-center shrink-0">RM</div>
                  <div class="overflow-hidden">
                    <p class="font-bold text-white text-[11px] truncate">Engr. Rafat Mohammed</p>
                    <p class="text-[9px] text-slate-400">QA/QC & Site Vision</p>
                  </div>
                </div>

                <!-- Member 5 -->
                <div class="flex items-center gap-2 p-1.5 bg-slate-950/60 rounded-xl border border-slate-800 sm:col-span-2">
                  <div class="w-7 h-7 rounded-lg bg-slate-800 text-indigo-300 font-black text-xs flex items-center justify-center shrink-0">AM</div>
                  <div class="overflow-hidden">
                    <p class="font-bold text-white text-[11px] truncate">Engr. Abu baker Mohammed</p>
                    <p class="text-[9px] text-slate-400">Cost Engineering & FIDIC Contracts</p>
                  </div>
                </div>
              </div>
            </div>

          </div>

          <div class="pt-1 flex items-center justify-between text-[11px] text-slate-400">
            <span>Supervised by: Department of Civil Engineering Board</span>
            <span class="font-bold text-indigo-300">Blue Nile University</span>
          </div>
        </div>

        <!-- RIGHT COLUMN (5 Cols): Enterprise Sign In Card -->
        <div class="lg:col-span-5 bg-white p-7 md:p-9 text-slate-900 flex flex-col justify-between space-y-6">
          <div class="space-y-4">
            
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-1.5 px-2.5 py-1 bg-indigo-50 border border-indigo-100 rounded-full text-indigo-700 font-extrabold text-[10px] uppercase tracking-wider">
                <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                <span>SECURE ACCESS PORTAL</span>
              </div>
              <span class="text-xs text-slate-400 font-semibold">RBAC Protected</span>
            </div>

            <div>
              <h3 id="i18n-login-card-title" class="text-2xl font-black text-[#0B1E3B] tracking-tight">Welcome Back</h3>
              <p id="i18n-login-card-sub" class="text-xs text-slate-500 mt-1">Sign in to open the project intelligence workspace or evaluate the defense demo.</p>
            </div>

            <!-- Login Form -->
            <form onsubmit="handleLoginSubmit(event)" class="space-y-4 pt-1">
              <div>
                <label id="i18n-login-lbl-user" class="block text-[11px] font-black text-slate-700 uppercase mb-1">USERNAME</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                    <i data-lucide="user" class="w-4 h-4"></i>
                  </div>
                  <input type="text" id="login-username" value="admin" required class="w-full bg-slate-50 border border-slate-200 focus:border-indigo-600 focus:bg-white text-slate-900 rounded-xl pl-9 pr-3 py-3 text-xs outline-none font-bold transition shadow-xs" placeholder="Username (e.g. admin)" />
                </div>
              </div>

              <div>
                <label id="i18n-login-lbl-pass" class="block text-[11px] font-black text-slate-700 uppercase mb-1">PASSWORD</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                    <i data-lucide="lock" class="w-4 h-4"></i>
                  </div>
                  <input type="password" id="login-password" value="Admin@123" required class="w-full bg-slate-50 border border-slate-200 focus:border-indigo-600 focus:bg-white text-slate-900 rounded-xl pl-9 pr-9 py-3 text-xs outline-none font-bold transition shadow-xs" placeholder="••••••••" />
                  <button type="button" onclick="togglePasswordVisibility()" class="absolute right-3 top-3 text-slate-400 hover:text-slate-600 transition">
                    <i data-lucide="eye" id="pass-eye-icon" class="w-4 h-4"></i>
                  </button>
                </div>
              </div>

              <div class="flex items-center justify-between text-xs text-slate-500">
                <label class="flex items-center gap-2 cursor-pointer select-none">
                  <input type="checkbox" checked class="rounded border-slate-300 text-indigo-600 focus:ring-0">
                  <span class="text-[11px]">Remember credentials</span>
                </label>
                <span class="text-[11px] font-bold text-indigo-600">Admin Account</span>
              </div>

              <!-- Main Sign In Button -->
              <button type="submit" id="btn-login-submit" class="w-full py-3.5 bg-[#0B1E3B] hover:bg-[#142A4E] text-white font-extrabold text-xs rounded-xl shadow-lg transition flex items-center justify-center gap-2 group">
                <span id="i18n-login-btn-sign">Sign In to Workspace</span>
                <i data-lucide="arrow-right" class="w-4 h-4 group-hover:translate-x-0.5 transition-transform"></i>
              </button>
            </form>

            <!-- Prominent One-Click Graduation Demo Button -->
            <div class="pt-1">
              <button type="button" onclick="handleQuickDemoLogin()" class="w-full py-3 bg-emerald-50 hover:bg-emerald-100 text-emerald-900 border-2 border-emerald-400 rounded-xl text-xs font-black transition flex items-center justify-center gap-2 shadow-sm pulse-glow">
                <i data-lucide="sparkles" class="w-4 h-4 text-emerald-600 animate-spin" style="animation-duration: 4s;"></i>
                <span id="i18n-login-btn-demo">⚡ One-Click Graduation Demo Access</span>
              </button>
              <p class="text-[10px] text-slate-400 text-center mt-1 font-semibold">Immediate access for graduation defense committee & evaluators</p>
            </div>

          </div>

          <!-- Credentials hint & Footer -->
          <div class="pt-3 border-t border-slate-100 space-y-1.5">
            <div class="bg-slate-50 border border-slate-200 rounded-xl p-2.5 flex items-center justify-between text-[11px] text-slate-600">
              <span class="font-bold">Demo Login:</span>
              <code class="bg-white px-2 py-0.5 rounded border border-slate-200 font-mono text-indigo-700 font-bold">admin / Admin@123</code>
            </div>
            <p class="text-[10px] text-slate-400 text-center">Blue Nile University • SPMA Platform © 2026</p>
          </div>

        </div>

      </div>
    </main>

    <!-- Bottom Footer of Login Page -->
    <footer class="w-full max-w-7xl mx-auto py-2 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-400 border-t border-slate-800/80 gap-2">
      <p>© 2026 Blue Nile University — Department of Civil & Project Engineering.</p>
      <div class="flex items-center gap-4 text-[11px]">
        <span>Privacy Policy</span>
        <span>•</span>
        <span>Graduation Defense Edition</span>
        <span>•</span>
        <span class="text-indigo-400 font-bold">SPMA AI Engine 6.4</span>
      </div>
    </footer>

  </div>


  <!-- ========================================================================= -->
  <!-- 2. MAIN APPLICATION WORKSPACE VIEW (VISIBLE AFTER SUCCESSFUL LOGIN)       -->
  <!-- ========================================================================= -->
  <div id="app-view" class="h-screen w-screen hidden overflow-hidden select-none bg-[#F8FAFC] text-slate-800">
    
    <!-- LEFT SIDEBAR -->
    <aside id="main-sidebar" class="w-64 bg-[#0B1E3B] text-slate-200 flex flex-col justify-between p-3.5 z-30 shrink-0 border-r border-slate-800">
      <div class="space-y-4">
        
        <!-- Top Brand Box (White rounded card with Blue Nile logo) -->
        <div class="bg-white rounded-2xl p-2.5 flex items-center gap-3 shadow-md border border-slate-100">
          <div class="w-10 h-10 rounded-xl bg-slate-50 p-1 flex items-center justify-center border border-slate-200 shrink-0">
            <img src="/static/brand/blue_nile_logo.png" alt="Logo" class="w-full h-full object-contain rounded-lg" />
          </div>
          <div class="overflow-hidden">
            <h1 class="font-extrabold text-[12px] leading-tight text-[#0B1E3B] truncate">Smart Project Manager Assistant (SPMA)</h1>
            <p class="text-[10px] font-bold text-slate-500">Blue Nile University</p>
          </div>
        </div>

        <!-- Navigation Menu (9 Main Tabs) -->
        <nav class="space-y-1 text-xs font-semibold">
          <button onclick="switchTab('dashboard')" id="nav-dashboard" class="w-full flex items-center gap-3 px-3 py-2 rounded-xl transition bg-slate-800/80 text-white font-bold border border-slate-700/60 shadow-sm">
            <i data-lucide="layout-dashboard" class="w-4 h-4 text-indigo-400"></i>
            <span id="i18n-nav-dashboard">Dashboard</span>
          </button>

          <button onclick="switchTab('projects')" id="nav-projects" class="w-full flex items-center gap-3 px-3 py-2 rounded-xl transition text-slate-300 hover:bg-slate-800/50 hover:text-white">
            <i data-lucide="folder-kanban" class="w-4 h-4 text-slate-400"></i>
            <span id="i18n-nav-projects">Projects</span>
          </button>

          <button onclick="switchTab('activities')" id="nav-activities" class="w-full flex items-center gap-3 px-3 py-2 rounded-xl transition text-slate-300 hover:bg-slate-800/50 hover:text-white">
            <i data-lucide="check-square" class="w-4 h-4 text-slate-400"></i>
            <span id="i18n-nav-activities">Activities</span>
          </button>

          <button onclick="switchTab('ai-assistant')" id="nav-ai-assistant" class="w-full flex items-center gap-3 px-3 py-2 rounded-xl transition text-slate-300 hover:bg-slate-800/50 hover:text-white">
            <i data-lucide="sparkles" class="w-4 h-4 text-indigo-400"></i>
            <span id="i18n-nav-ai-assistant">AI Assistant</span>
          </button>

          <button onclick="switchTab('reports')" id="nav-reports" class="w-full flex items-center gap-3 px-3 py-2 rounded-xl transition text-slate-300 hover:bg-slate-800/50 hover:text-white">
            <i data-lucide="file-text" class="w-4 h-4 text-slate-400"></i>
            <span id="i18n-nav-reports">Reports</span>
          </button>

          <button onclick="switchTab('engineer-chat')" id="nav-engineer-chat" class="w-full flex items-center gap-3 px-3 py-2 rounded-xl transition text-slate-300 hover:bg-slate-800/50 hover:text-white">
            <i data-lucide="message-circle" class="w-4 h-4 text-slate-400"></i>
            <span id="i18n-nav-engineer-chat">Engineer Chat</span>
          </button>

          <button onclick="switchTab('whatsapp-center')" id="nav-whatsapp-center" class="w-full flex items-center gap-3 px-3 py-2 rounded-xl transition text-slate-300 hover:bg-slate-800/50 hover:text-white">
            <i data-lucide="phone-call" class="w-4 h-4 text-emerald-400"></i>
            <span id="i18n-nav-whatsapp-center">WhatsApp Center</span>
          </button>

          <button onclick="switchTab('user-mgmt')" id="nav-user-mgmt" class="w-full flex items-center gap-3 px-3 py-2 rounded-xl transition text-slate-300 hover:bg-slate-800/50 hover:text-white">
            <i data-lucide="user-check" class="w-4 h-4 text-slate-400"></i>
            <span id="i18n-nav-user-mgmt">User Management</span>
          </button>

          <button onclick="switchTab('settings')" id="nav-settings" class="w-full flex items-center gap-3 px-3 py-2 rounded-xl transition text-slate-300 hover:bg-slate-800/50 hover:text-white">
            <i data-lucide="settings" class="w-4 h-4 text-slate-400"></i>
            <span id="i18n-nav-settings">Settings</span>
          </button>
        </nav>
      </div>

      <!-- Bottom Section: PROJECT TEAM & User Logout -->
      <div class="space-y-2 pt-2 border-t border-slate-800/80">
        <div class="flex items-center justify-between px-1">
          <span id="i18n-team-title" class="text-[10px] font-extrabold tracking-wider text-slate-400 uppercase">PROJECT TEAM</span>
          <span class="text-[10px] text-indigo-400 font-bold">5 Online</span>
        </div>

        <div class="space-y-1.5 max-h-36 overflow-y-auto custom-scrollbar-dark pr-0.5">
          <!-- Member 1 -->
          <div class="bg-slate-900/90 border border-slate-800 p-2 rounded-xl space-y-1">
            <div class="flex items-center justify-between text-[11px]">
              <span class="font-bold text-white truncate">Engr. Asem Othman</span>
            </div>
            <p class="text-[10px] text-slate-400">Project Manager</p>
            <div class="flex gap-1 pt-0.5">
              <a href="tel:+966505554101" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="phone" class="w-3 h-3"></i></a>
              <a href="mailto:asem.2007@hotmail.com" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="mail" class="w-3 h-3"></i></a>
              <button onclick="openWhatsAppFor('Engr. Asem Othman', '966505554101')" class="flex-1 bg-emerald-950/60 hover:bg-emerald-900/80 text-emerald-300 p-1 rounded flex items-center justify-center text-[9px] font-bold">WA</button>
            </div>
          </div>

          <!-- Member 2 -->
          <div class="bg-slate-900/90 border border-slate-800 p-2 rounded-xl space-y-1">
            <div class="flex items-center justify-between text-[11px]">
              <span class="font-bold text-white truncate">Engr. Saleh Mohammed</span>
            </div>
            <p class="text-[10px] text-slate-400">Planning Engineer</p>
            <div class="flex gap-1 pt-0.5">
              <a href="tel:+966552345678" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="phone" class="w-3 h-3"></i></a>
              <a href="mailto:saleh@spma.com" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="mail" class="w-3 h-3"></i></a>
              <button onclick="openWhatsAppFor('Engr. Saleh Mohammed', '966552345678')" class="flex-1 bg-emerald-950/60 hover:bg-emerald-900/80 text-emerald-300 p-1 rounded flex items-center justify-center text-[9px] font-bold">WA</button>
            </div>
          </div>

          <!-- Member 3 -->
          <div class="bg-slate-900/90 border border-slate-800 p-2 rounded-xl space-y-1">
            <div class="flex items-center justify-between text-[11px]">
              <span class="font-bold text-white truncate">Engr. Mohammed Gassim</span>
            </div>
            <p class="text-[10px] text-slate-400">Site Engineer</p>
            <div class="flex gap-1 pt-0.5">
              <a href="tel:+966563456789" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="phone" class="w-3 h-3"></i></a>
              <a href="mailto:gassim@spma.com" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="mail" class="w-3 h-3"></i></a>
              <button onclick="openWhatsAppFor('Engr. Mohammed Gassim', '966563456789')" class="flex-1 bg-emerald-950/60 hover:bg-emerald-900/80 text-emerald-300 p-1 rounded flex items-center justify-center text-[9px] font-bold">WA</button>
            </div>
          </div>

          <!-- Member 4 -->
          <div class="bg-slate-900/90 border border-slate-800 p-2 rounded-xl space-y-1">
            <div class="flex items-center justify-between text-[11px]">
              <span class="font-bold text-white truncate">Engr. Rafat Mohammed</span>
            </div>
            <p class="text-[10px] text-slate-400">Quality Engineer</p>
            <div class="flex gap-1 pt-0.5">
              <a href="tel:+966574567890" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="phone" class="w-3 h-3"></i></a>
              <a href="mailto:rafat@spma.com" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="mail" class="w-3 h-3"></i></a>
              <button onclick="openWhatsAppFor('Engr. Rafat Mohammed', '966574567890')" class="flex-1 bg-emerald-950/60 hover:bg-emerald-900/80 text-emerald-300 p-1 rounded flex items-center justify-center text-[9px] font-bold">WA</button>
            </div>
          </div>

          <!-- Member 5 -->
          <div class="bg-slate-900/90 border border-slate-800 p-2 rounded-xl space-y-1">
            <div class="flex items-center justify-between text-[11px]">
              <span class="font-bold text-white truncate">Engr. Abu baker Mohammed</span>
            </div>
            <p class="text-[10px] text-slate-400">Cost & FIDIC Engineer</p>
            <div class="flex gap-1 pt-0.5">
              <a href="tel:+966585678901" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="phone" class="w-3 h-3"></i></a>
              <a href="mailto:abubaker@spma.com" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="mail" class="w-3 h-3"></i></a>
              <button onclick="openWhatsAppFor('Engr. Abu baker Mohammed', '966585678901')" class="flex-1 bg-emerald-950/60 hover:bg-emerald-900/80 text-emerald-300 p-1 rounded flex items-center justify-center text-[9px] font-bold">WA</button>
            </div>
          </div>
        </div>

        <!-- Current User Box & Logout -->
        <div class="bg-slate-900 p-2 rounded-xl border border-slate-800 flex items-center justify-between">
          <div class="flex items-center gap-2 overflow-hidden">
            <div class="w-7 h-7 rounded-lg bg-indigo-600 text-white font-black text-xs flex items-center justify-center shrink-0">AO</div>
            <div class="overflow-hidden">
              <p class="text-xs font-bold text-white truncate">Asem Othman</p>
              <p class="text-[10px] text-emerald-400 font-semibold">ADMIN</p>
            </div>
          </div>
          <button onclick="handleLogout()" id="btn-logout" class="px-2 py-1 bg-slate-800 hover:bg-rose-950/80 hover:text-rose-300 text-slate-400 text-[10px] font-bold rounded-lg border border-slate-700 transition">
            Logout
          </button>
        </div>
      </div>
    </aside>

    <!-- MAIN RIGHT CONTENT CONTAINER -->
    <main class="flex-1 flex flex-col min-w-0 bg-[#F8FAFC] overflow-hidden">
      
      <!-- Top Header Bar -->
      <header class="h-14 bg-white border-b border-slate-200/80 px-6 flex items-center justify-between shrink-0 z-20">
        <div class="flex items-center gap-4">
          <h2 id="top-title" class="text-sm font-bold text-slate-800">Dashboard</h2>
          
          <!-- Active Project Selector -->
          <div class="flex items-center gap-2 bg-slate-50 border border-slate-200 rounded-xl px-2.5 py-1">
            <i data-lucide="briefcase" class="w-3.5 h-3.5 text-indigo-600"></i>
            <select id="global-project-select" onchange="switchActiveProject(this.value)" class="bg-transparent text-xs font-bold text-slate-700 outline-none cursor-pointer">
              <option value="kkia">King Khalid International Airport – Terminal 5</option>
              <option value="hospital">Blue Nile Specialized Medical City</option>
              <option value="bridges">Northern Sector Bridges & Infrastructure</option>
            </select>
          </div>
        </div>

        <!-- Top Right Actions -->
        <div class="flex items-center gap-2">
          <!-- Refresh Button -->
          <button onclick="refreshCurrentPage()" class="p-2 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded-xl transition">
            <i data-lucide="rotate-cw" class="w-4 h-4"></i>
          </button>

          <!-- Language Switcher (EN / ع) -->
          <button onclick="toggleLanguage()" id="lang-toggle-btn" class="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold border border-slate-200 flex items-center gap-1.5 transition">
            <i data-lucide="globe" class="w-3.5 h-3.5 text-indigo-600"></i>
            <span id="lang-label">عربي</span>
          </button>

          <!-- New Project Button -->
          <button onclick="openAddProjectModal()" class="px-3.5 py-1.5 bg-[#0B1E3B] hover:bg-[#142A4E] text-white text-xs font-bold rounded-xl shadow transition flex items-center gap-1.5">
            <i data-lucide="plus" class="w-3.5 h-3.5"></i>
            <span id="i18n-btn-top-project">+ Project</span>
          </button>
        </div>
      </header>

      <!-- Scrollable Tab Content Area -->
      <div class="flex-1 overflow-y-auto custom-scrollbar p-6 space-y-6">
        
        <!-- TAB 1: DASHBOARD -->
        <section id="tab-dashboard" class="space-y-6">
          
          <!-- Hero Navy Banner -->
          <div class="bg-[#0B1E3B] rounded-2xl p-6 text-white flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-lg border border-slate-800">
            <div class="space-y-1">
              <h1 id="i18n-dash-hero-title" class="text-xl font-black tracking-tight">Project Intelligence Workspace</h1>
              <p id="i18n-dash-hero-sub" class="text-xs text-slate-300 max-w-xl">Live progress, cost, risk, deadlines and communication in one place.</p>
            </div>
            <div class="flex flex-wrap gap-2">
              <button onclick="openAddProjectModal()" class="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-bold border border-slate-700 transition flex items-center gap-1.5">
                <i data-lucide="folder-plus" class="w-3.5 h-3.5"></i>
                <span id="i18n-btn-new-proj">New Project</span>
              </button>
              <button onclick="switchTab('whatsapp-center')" class="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold shadow transition flex items-center gap-1.5">
                <i data-lucide="send" class="w-3.5 h-3.5"></i>
                <span id="i18n-btn-send-update">Send Project Update</span>
              </button>
            </div>
          </div>

          <!-- 6 Top Summary KPI Cards -->
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3.5">
            <!-- Total Projects -->
            <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm space-y-1">
              <span id="i18n-metric-total-proj" class="text-[11px] font-bold text-slate-400">Total Projects</span>
              <p class="text-2xl font-black text-[#0B1E3B] tabular-nums" id="kpi-total-projects">3</p>
              <span class="text-[10px] text-slate-400">1 portfolio wide</span>
            </div>

            <!-- Active Projects -->
            <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm space-y-1">
              <span id="i18n-metric-active-proj" class="text-[11px] font-bold text-slate-400">Active Projects</span>
              <p class="text-2xl font-black text-[#0B1E3B] tabular-nums" id="kpi-active-projects">3</p>
              <span class="text-[10px] text-emerald-600 font-bold">100% active rate</span>
            </div>

            <!-- Completed Projects -->
            <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm space-y-1">
              <span id="i18n-metric-comp-proj" class="text-[11px] font-bold text-slate-400">Completed Projects</span>
              <p class="text-2xl font-black text-[#0B1E3B] tabular-nums" id="kpi-completed-projects">0</p>
              <span class="text-[10px] text-slate-400">0 archived</span>
            </div>

            <!-- Delayed Activities -->
            <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm space-y-1">
              <span id="i18n-metric-delayed-act" class="text-[11px] font-bold text-slate-400">Delayed Activities</span>
              <p class="text-2xl font-black text-rose-600 tabular-nums" id="kpi-delayed-activities">1</p>
              <span class="text-[10px] text-rose-500 font-bold">Requires attention</span>
            </div>

            <!-- Budget Used -->
            <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm space-y-1">
              <span id="i18n-metric-budget-used" class="text-[11px] font-bold text-slate-400">Budget Used</span>
              <p class="text-2xl font-black text-[#0B1E3B] tabular-nums" id="kpi-budget-used">0.11%</p>
              <span class="text-[10px] text-slate-400">SAR 1,000 spent</span>
            </div>

            <!-- Average Progress -->
            <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm space-y-1">
              <span id="i18n-metric-avg-prog" class="text-[11px] font-bold text-slate-400">Average Progress</span>
              <p class="text-2xl font-black text-emerald-600 tabular-nums" id="kpi-avg-progress">100%</p>
              <span class="text-[10px] text-slate-400">Weighted avg</span>
            </div>
          </div>

          <!-- 3 Lower Widgets: Executive Alerts, Engineer Workload, 30-Day Timeline -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            
            <!-- Executive Alerts -->
            <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm space-y-3">
              <div class="flex items-center justify-between border-b border-slate-100 pb-2">
                <span id="i18n-card-alerts-title" class="text-xs font-bold text-[#0B1E3B]">Executive Alerts</span>
                <button onclick="markAlertsRead()" class="text-[11px] text-indigo-600 font-bold hover:underline" id="i18n-btn-mark-read">Mark Read</button>
              </div>
              <div class="space-y-2">
                <div class="p-2.5 bg-rose-50 border border-rose-100 rounded-xl space-y-0.5">
                  <div class="flex items-center justify-between text-rose-800 text-xs font-bold">
                    <span>High risk project</span>
                    <span class="text-[10px]">Just now</span>
                  </div>
                  <p class="text-[11px] text-rose-600">King Khalid International Airport Branch – Terminal 5 has high risk.</p>
                </div>

                <div class="p-2.5 bg-amber-50 border border-amber-100 rounded-xl space-y-0.5">
                  <div class="flex items-center justify-between text-amber-800 text-xs font-bold">
                    <span>Delayed activity</span>
                    <span class="text-[10px]">Today</span>
                  </div>
                  <p class="text-[11px] text-amber-700">concrete in King Khalid International Airport Branch – Terminal 5 is delayed.</p>
                </div>
              </div>
            </div>

            <!-- Engineer Workload -->
            <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm space-y-3">
              <div class="flex items-center justify-between border-b border-slate-100 pb-2">
                <span id="i18n-card-workload-title" class="text-xs font-bold text-[#0B1E3B]">Engineer Workload</span>
                <span class="text-[10px] font-bold text-slate-400">5 Members</span>
              </div>
              <div class="space-y-2.5">
                <div>
                  <div class="flex justify-between text-[11px] font-bold text-slate-700 mb-1">
                    <span>Engr. Asem Othman</span>
                    <span class="text-indigo-600">3 Activities</span>
                  </div>
                  <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                    <div class="bg-indigo-600 h-full rounded-full" style="width: 75%"></div>
                  </div>
                </div>

                <div>
                  <div class="flex justify-between text-[11px] font-bold text-slate-700 mb-1">
                    <span>Engr. Saleh Mohammed</span>
                    <span class="text-indigo-600">2 Activities</span>
                  </div>
                  <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                    <div class="bg-indigo-600 h-full rounded-full" style="width: 50%"></div>
                  </div>
                </div>

                <div>
                  <div class="flex justify-between text-[11px] font-bold text-slate-700 mb-1">
                    <span>Engr. Mohammed Gassim</span>
                    <span class="text-indigo-600">4 Activities</span>
                  </div>
                  <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                    <div class="bg-emerald-600 h-full rounded-full" style="width: 90%"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 30-Day Timeline -->
            <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm space-y-3">
              <div class="flex items-center justify-between border-b border-slate-100 pb-2">
                <span id="i18n-card-timeline-title" class="text-xs font-bold text-[#0B1E3B]">30-Day Timeline</span>
                <span class="text-[10px] font-bold text-indigo-600">Next Milestones</span>
              </div>
              <div class="space-y-2 text-xs">
                <div class="p-2 bg-slate-50 rounded-xl border border-slate-100 flex items-center justify-between">
                  <div>
                    <p class="font-bold text-slate-800">Terminal 5 Apron Concrete</p>
                    <p class="text-[10px] text-slate-400">King Khalid Airport</p>
                  </div>
                  <span class="px-2 py-0.5 bg-rose-100 text-rose-700 rounded text-[10px] font-bold">12 Oct</span>
                </div>

                <div class="p-2 bg-slate-50 rounded-xl border border-slate-100 flex items-center justify-between">
                  <div>
                    <p class="font-bold text-slate-800">Foundation Raft Inspection</p>
                    <p class="text-[10px] text-slate-400">Blue Nile Hospital</p>
                  </div>
                  <span class="px-2 py-0.5 bg-indigo-100 text-indigo-700 rounded text-[10px] font-bold">20 Oct</span>
                </div>
              </div>
            </div>

          </div>

          <!-- Bottom Visuals: Portfolio Performance Bar & Project Health Ring -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div class="md:col-span-2 bg-white p-5 rounded-2xl border border-slate-100 shadow-sm space-y-3">
              <span id="i18n-portfolio-perf-title" class="text-xs font-bold text-[#0B1E3B]">Portfolio Performance</span>
              <div class="space-y-2">
                <div class="flex justify-between text-xs font-bold text-slate-700">
                  <span>King Khalid International Airport Branch – Terminal 5</span>
                  <span class="text-emerald-600">100%</span>
                </div>
                <div class="w-full bg-slate-100 h-3 rounded-full overflow-hidden">
                  <div class="bg-rose-500 h-full rounded-full" style="width: 100%"></div>
                </div>
              </div>
            </div>

            <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm flex items-center justify-between">
              <div class="space-y-1">
                <span id="i18n-proj-health-title" class="text-xs font-bold text-[#0B1E3B]">Project Health</span>
                <p class="text-xs text-slate-400">EVM & Schedule Index</p>
                <div class="flex items-center gap-3 pt-2 text-[10px] font-bold">
                  <span class="text-emerald-600">● Healthy: 0</span>
                  <span class="text-amber-500">● Warning: 0</span>
                  <span class="text-rose-500">● Critical: 1</span>
                </div>
              </div>
              <div class="relative w-20 h-20 flex items-center justify-center">
                <svg class="w-full h-full transform -rotate-90">
                  <circle cx="40" cy="40" r="32" stroke="#F1F5F9" stroke-width="8" fill="transparent" />
                  <circle cx="40" cy="40" r="32" stroke="#F43F5E" stroke-width="8" stroke-dasharray="200" stroke-dashoffset="30" fill="transparent" stroke-linecap="round" />
                </svg>
                <span class="absolute font-black text-xs text-[#0B1E3B]">85%</span>
              </div>
            </div>
          </div>

        </section>

        <!-- TAB 2: PROJECTS -->
        <section id="tab-projects" class="hidden space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 id="i18n-projects-title" class="text-lg font-black text-[#0B1E3B]">Projects</h2>
              <p id="i18n-projects-desc" class="text-xs text-slate-500">Create and monitor all projects in the portfolio.</p>
            </div>
            <button onclick="openAddProjectModal()" class="px-4 py-2 bg-[#0B1E3B] hover:bg-[#142A4E] text-white font-bold text-xs rounded-xl shadow transition flex items-center gap-1.5">
              <i data-lucide="plus" class="w-3.5 h-3.5"></i>
              <span id="i18n-btn-new-proj-tab">+ New Project</span>
            </button>
          </div>

          <!-- Project Cards Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            <!-- Project 1 -->
            <div class="bg-white rounded-2xl border border-slate-100 p-5 shadow-sm space-y-3">
              <div class="flex items-center justify-between">
                <span class="px-2 py-0.5 bg-rose-50 text-rose-700 rounded text-[10px] font-bold">High Risk</span>
                <span class="text-xs font-bold text-slate-400">KKIA-T5</span>
              </div>
              <div>
                <h3 class="font-bold text-sm text-[#0B1E3B]">King Khalid International Airport Branch – Terminal 5</h3>
                <p class="text-xs text-slate-400">Active • SAR 931,512.29 Budget</p>
              </div>
              <div class="space-y-1">
                <div class="flex justify-between text-xs font-bold">
                  <span class="text-slate-500">Progress</span>
                  <span class="text-emerald-600">100%</span>
                </div>
                <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                  <div class="bg-emerald-500 h-full rounded-full" style="width: 100%"></div>
                </div>
              </div>
              <div class="pt-2 border-t border-slate-100 flex items-center justify-between text-xs">
                <span class="text-slate-500">1 Activity</span>
                <button onclick="switchTab('activities')" class="text-indigo-600 font-bold hover:underline">View Details →</button>
              </div>
            </div>

            <!-- Project 2 -->
            <div class="bg-white rounded-2xl border border-slate-100 p-5 shadow-sm space-y-3">
              <div class="flex items-center justify-between">
                <span class="px-2 py-0.5 bg-emerald-50 text-emerald-700 rounded text-[10px] font-bold">On Schedule</span>
                <span class="text-xs font-bold text-slate-400">BN-HOSP</span>
              </div>
              <div>
                <h3 class="font-bold text-sm text-[#0B1E3B]">Blue Nile Specialized Medical City</h3>
                <p class="text-xs text-slate-400">Active • SAR 4,500,000.00 Budget</p>
              </div>
              <div class="space-y-1">
                <div class="flex justify-between text-xs font-bold">
                  <span class="text-slate-500">Progress</span>
                  <span class="text-indigo-600">42%</span>
                </div>
                <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                  <div class="bg-indigo-600 h-full rounded-full" style="width: 42%"></div>
                </div>
              </div>
              <div class="pt-2 border-t border-slate-100 flex items-center justify-between text-xs">
                <span class="text-slate-500">18 Activities</span>
                <button onclick="switchTab('activities')" class="text-indigo-600 font-bold hover:underline">View Details →</button>
              </div>
            </div>
          </div>
        </section>

        <!-- TAB 3: ACTIVITIES -->
        <section id="tab-activities" class="hidden space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 id="i18n-activities-title" class="text-lg font-black text-[#0B1E3B]">Activities</h2>
              <p id="i18n-activities-desc" class="text-xs text-slate-500">Track planned and actual progress and upcoming deadlines.</p>
            </div>
            <button onclick="openAddActivityModal()" class="px-4 py-2 bg-[#0B1E3B] hover:bg-[#142A4E] text-white font-bold text-xs rounded-xl shadow transition flex items-center gap-1.5">
              <i data-lucide="plus" class="w-3.5 h-3.5"></i>
              <span id="i18n-btn-new-activity-tab">+ New Activity</span>
            </button>
          </div>

          <!-- Activities Table -->
          <div class="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
            <div class="p-3 bg-slate-50 border-b border-slate-100 flex items-center justify-between">
              <div class="flex gap-1 text-xs">
                <button class="px-3 py-1 bg-white border border-slate-200 rounded-lg font-bold text-[#0B1E3B] shadow-2xs">All (1)</button>
                <button class="px-3 py-1 text-slate-500 hover:text-slate-800 font-semibold">Delayed (1)</button>
                <button class="px-3 py-1 text-slate-500 hover:text-slate-800 font-semibold">In Progress (0)</button>
                <button class="px-3 py-1 text-slate-500 hover:text-slate-800 font-semibold">Completed (1)</button>
              </div>
              <input type="text" placeholder="Search activities..." class="bg-white border border-slate-200 rounded-lg px-2.5 py-1 text-xs outline-none w-48" />
            </div>

            <table class="w-full text-xs text-left border-collapse">
              <thead class="bg-slate-50 text-slate-400 font-bold border-b border-slate-100">
                <tr>
                  <th class="p-3.5">Activity Name</th>
                  <th class="p-3.5">Project</th>
                  <th class="p-3.5">Status</th>
                  <th class="p-3.5">Planned End</th>
                  <th class="p-3.5">Actual %</th>
                  <th class="p-3.5">Spent (SAR)</th>
                  <th class="p-3.5 text-right">Action</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 text-slate-700 font-medium">
                <tr class="hover:bg-slate-50">
                  <td class="p-3.5 font-bold text-slate-900">concrete</td>
                  <td class="p-3.5 text-slate-500">King Khalid Airport – Terminal 5</td>
                  <td class="p-3.5"><span class="px-2 py-0.5 bg-rose-100 text-rose-700 rounded text-[10px] font-bold">Delayed</span></td>
                  <td class="p-3.5 text-slate-500">2026-03-31</td>
                  <td class="p-3.5 font-bold text-emerald-600">100%</td>
                  <td class="p-3.5 tabular-nums">1,000.00</td>
                  <td class="p-3.5 text-right">
                    <button class="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 rounded-lg font-bold text-indigo-700">Edit</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- TAB 4: AI ASSISTANT -->
        <section id="tab-ai-assistant" class="hidden space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 id="i18n-ai-title" class="text-lg font-black text-[#0B1E3B]">AI Assistant</h2>
              <p id="i18n-ai-desc" class="text-xs text-slate-500">Ask questions based on live project, EVM calculations and schedule data.</p>
            </div>
            <div class="flex items-center gap-2">
              <span class="px-2.5 py-1 bg-indigo-50 border border-indigo-200 text-indigo-700 rounded-lg text-xs font-bold flex items-center gap-1">
                <i data-lucide="sparkles" class="w-3.5 h-3.5"></i>
                <span>Gemini 2.5 Flash</span>
              </span>
            </div>
          </div>

          <!-- Chat Stream Area -->
          <div class="bg-white rounded-2xl border border-slate-100 shadow-sm flex flex-col h-[520px] overflow-hidden">
            <div id="chat-messages-container" class="flex-1 p-5 overflow-y-auto space-y-4 custom-scrollbar text-xs">
              <!-- Welcome Bot Message -->
              <div class="flex items-start gap-3 max-w-2xl">
                <div class="w-8 h-8 rounded-xl bg-[#0B1E3B] text-white flex items-center justify-center shrink-0 shadow-sm">
                  <i data-lucide="bot" class="w-4 h-4 text-indigo-400"></i>
                </div>
                <div class="p-4 bg-slate-50 rounded-2xl border border-slate-100 text-slate-800 space-y-2">
                  <p class="font-bold text-[#0B1E3B]">Smart Project Manager Assistant (SPMA)</p>
                  <p class="leading-relaxed">
                    مرحباً بك! أنا مساعدك الذكي لإدارة ومراقبة مشاريعك الهندسية بجامعة النيل الأزرق. يمكنك سؤالي صوتياً أو كتابياً عن نسب الإنجاز، مؤشرات الـ EVM (SPI, CPI)، الأنشطة المتأخرة، أو طلب تحليل للصور ومطالبات الفيديك.
                  </p>
                  <div class="flex flex-wrap gap-1.5 pt-1">
                    <button onclick="askQuickPrompt('كم نسبة إنجاز مشروع مطار الملك خالد؟')" class="px-2.5 py-1 bg-white border border-slate-200 rounded-lg text-[11px] font-semibold text-slate-700 hover:bg-slate-100">كم نسبة إنجاز المشروع؟</button>
                    <button onclick="askQuickPrompt('ما هي مؤشرات القيمة المكتسبة SPI و CPI؟')" class="px-2.5 py-1 bg-white border border-slate-200 rounded-lg text-[11px] font-semibold text-slate-700 hover:bg-slate-100">احسب مؤشرات EVM</button>
                    <button onclick="askQuickPrompt('ما هو المسار الحرج والأنشطة المتأخرة؟')" class="px-2.5 py-1 bg-white border border-slate-200 rounded-lg text-[11px] font-semibold text-slate-700 hover:bg-slate-100">المسار الحرج</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Input Bar with Mic & Vision Upload -->
            <div class="p-3 border-t border-slate-100 bg-slate-50/50 flex items-center gap-2">
              <input type="file" id="vision-file-input" accept="image/*" class="hidden" onchange="handleVisionImageUpload(event)" />
              
              <button type="button" onclick="document.getElementById('vision-file-input').click()" title="Upload Site Photo" class="p-2.5 bg-white border border-slate-200 text-slate-600 hover:text-indigo-600 rounded-xl transition">
                <i data-lucide="camera" class="w-4 h-4"></i>
              </button>

              <button type="button" onclick="toggleVoiceRecording()" id="voice-btn" title="Voice Command" class="p-2.5 bg-white border border-slate-200 text-slate-600 hover:text-indigo-600 rounded-xl transition">
                <i data-lucide="mic" class="w-4 h-4"></i>
              </button>

              <input type="text" id="chat-input" onkeydown="if(event.key==='Enter') handleChatSubmit()" placeholder="Ask about EVM, activities, SPI/CPI, delays, or FIDIC claims..." class="flex-1 bg-white border border-slate-200 focus:border-indigo-600 rounded-xl px-4 py-2.5 text-xs text-slate-800 outline-none transition font-medium" />

              <button onclick="handleChatSubmit()" class="px-4 py-2.5 bg-[#0B1E3B] hover:bg-[#142A4E] text-white font-bold text-xs rounded-xl shadow transition flex items-center gap-1.5">
                <span>Send</span>
                <i data-lucide="send" class="w-3.5 h-3.5"></i>
              </button>
            </div>
          </div>
        </section>

        <!-- TAB 5: REPORTS -->
        <section id="tab-reports" class="hidden space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 id="i18n-reports-title" class="text-lg font-black text-[#0B1E3B]">Reports</h2>
              <p id="i18n-reports-desc" class="text-xs text-slate-500">Generate executive PDF reports and Excel sheets.</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <!-- PDF Report Card -->
            <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm space-y-4">
              <div class="w-12 h-12 bg-rose-50 text-rose-600 rounded-2xl flex items-center justify-center">
                <i data-lucide="file-text" class="w-6 h-6"></i>
              </div>
              <div>
                <h3 class="font-bold text-sm text-[#0B1E3B]">Executive EVM & Status Report (PDF)</h3>
                <p class="text-xs text-slate-500 mt-1">Official report with Blue Nile University branding, EVM charts, and schedule breakdown.</p>
              </div>
              <a href="/api/reports/executive-pdf" target="_blank" class="inline-flex items-center gap-2 px-4 py-2.5 bg-[#0B1E3B] hover:bg-[#142A4E] text-white font-bold text-xs rounded-xl shadow transition">
                <i data-lucide="download" class="w-3.5 h-3.5"></i>
                <span>Download Executive PDF</span>
              </a>
            </div>

            <!-- Excel Export Card -->
            <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm space-y-4">
              <div class="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-2xl flex items-center justify-center">
                <i data-lucide="sheet" class="w-6 h-6"></i>
              </div>
              <div>
                <h3 class="font-bold text-sm text-[#0B1E3B]">Project Activities & Costs Export (Excel)</h3>
                <p class="text-xs text-slate-500 mt-1">Structured spreadsheet with formulas, planned vs actual costs, and progress tracking.</p>
              </div>
              <a href="/api/reports/executive-excel" target="_blank" class="inline-flex items-center gap-2 px-4 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs rounded-xl shadow transition">
                <i data-lucide="download" class="w-3.5 h-3.5"></i>
                <span>Download Excel Sheet</span>
              </a>
            </div>
          </div>
        </section>

        <!-- TAB 6: ENGINEER CHAT -->
        <section id="tab-engineer-chat" class="hidden space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-5 h-[540px]">
            <!-- Channels / Rooms List -->
            <div class="bg-white rounded-2xl border border-slate-100 p-4 shadow-sm space-y-3">
              <span class="text-xs font-bold text-[#0B1E3B]">Communication Channels</span>
              <div class="p-2.5 bg-indigo-50 text-[#0B1E3B] rounded-xl font-bold text-xs flex items-center gap-2">
                <i data-lucide="hash" class="w-3.5 h-3.5 text-indigo-600"></i>
                <span>General Team Chat</span>
              </div>
              <div class="space-y-1">
                <span class="text-[10px] font-bold text-slate-400 uppercase">PROJECT CHATS</span>
                <div class="p-2 rounded-lg text-slate-600 hover:bg-slate-50 text-xs font-medium truncate cursor-pointer">
                  # King Khalid International Airport Branch – Terminal 5
                </div>
              </div>
              <div class="space-y-1 pt-2">
                <span class="text-[10px] font-bold text-slate-400 uppercase">PRIVATE CHATS</span>
                <div class="text-[11px] text-slate-400 italic p-1">No private chats.</div>
              </div>
            </div>

            <!-- Main Team Chat Area -->
            <div class="md:col-span-3 bg-white rounded-2xl border border-slate-100 shadow-sm flex flex-col overflow-hidden">
              <div class="p-4 border-b border-slate-100 flex items-center justify-between">
                <span class="font-bold text-xs text-[#0B1E3B]">General Team Chat</span>
                <div class="flex items-center gap-2">
                  <input type="text" placeholder="Search messages..." class="bg-slate-50 border border-slate-200 rounded-lg px-2 py-1 text-xs outline-none w-44" />
                  <button class="text-xs font-bold text-indigo-600 hover:underline">Refresh</button>
                </div>
              </div>
              
              <div id="eng-chat-stream" class="flex-1 p-5 overflow-y-auto space-y-3 custom-scrollbar text-xs">
                <div class="p-3 bg-slate-50 rounded-xl border border-slate-100 space-y-1 max-w-md">
                  <div class="flex items-center justify-between text-[11px] font-bold text-[#0B1E3B]">
                    <span>Engr. Asem Othman</span>
                    <span class="text-[9px] text-slate-400">10:14 AM</span>
                  </div>
                  <p class="text-slate-600">Please verify the concrete pouring schedule for Terminal 5 apron zone.</p>
                </div>
              </div>

              <!-- Emoji Bar & Message Box -->
              <div class="p-3 border-t border-slate-100 bg-slate-50 space-y-2">
                <div class="flex items-center gap-3 text-sm text-slate-500 cursor-pointer">
                  <span onclick="addEmojiToEngChat('👍')">👍</span>
                  <span onclick="addEmojiToEngChat('✅')">✅</span>
                  <span onclick="addEmojiToEngChat('⚠️')">⚠️</span>
                  <span onclick="addEmojiToEngChat('📌')">📌</span>
                  <span onclick="addEmojiToEngChat('📎')">📎</span>
                  <span onclick="addEmojiToEngChat('🙏')">🙏</span>
                </div>
                <form onsubmit="handleEngChatSubmit(event)" class="flex items-center gap-2">
                  <input type="text" id="eng-chat-input" placeholder="Write a message..." class="flex-1 bg-white border border-slate-200 rounded-xl px-3.5 py-2 text-xs text-slate-800 outline-none focus:border-indigo-600" />
                  <button type="submit" class="px-4 py-2 bg-[#0B1E3B] hover:bg-[#142A4E] text-white font-bold text-xs rounded-xl shadow transition">Send</button>
                </form>
              </div>
            </div>
          </div>
        </section>

        <!-- TAB 7: WHATSAPP CENTER -->
        <section id="tab-whatsapp-center" class="hidden space-y-4">
          <!-- Green Banner -->
          <div class="bg-[#059669] text-white p-5 rounded-2xl space-y-1 shadow-md">
            <h2 class="text-base font-bold flex items-center gap-2">
              <i data-lucide="message-square" class="w-5 h-5"></i>
              <span>WhatsApp Project Update Center</span>
            </h2>
            <p class="text-xs text-emerald-100">Prepare project data, upload a file, open WhatsApp, or send directly through the official Business API when configured.</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <!-- Main Form -->
            <div class="md:col-span-2 bg-white rounded-2xl border border-slate-100 p-5 shadow-sm space-y-4">
              <div class="flex gap-2 border-b border-slate-100 pb-3">
                <button class="px-4 py-1.5 bg-emerald-50 text-emerald-800 font-bold text-xs rounded-xl border border-emerald-200">Quick WhatsApp</button>
                <button class="px-4 py-1.5 text-slate-600 hover:bg-slate-50 font-bold text-xs rounded-xl">Business API Direct</button>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs font-bold text-slate-700 mb-1">Project</label>
                  <select class="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 text-xs font-semibold">
                    <option>King Khalid International Airport Branch – Terminal 5</option>
                  </select>
                </div>
                <div>
                  <label class="block text-xs font-bold text-slate-700 mb-1">Recipient</label>
                  <select id="wa-recipient-select" onchange="updateWaRecipient(this.value)" class="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 text-xs font-semibold">
                    <option value="966505554101">Engr. Asem Othman (+966 50 555 4101)</option>
                    <option value="966552345678">Engr. Saleh Mohammed (+966 55 234 5678)</option>
                    <option value="966563456789">Engr. Mohammed Gassim (+966 56 345 6789)</option>
                  </select>
                </div>
              </div>

              <div>
                <label class="block text-xs font-bold text-slate-700 mb-1">Phone with country code</label>
                <input type="text" id="wa-phone-input" value="966505554101" class="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 text-xs font-semibold text-slate-800" />
              </div>

              <div class="space-y-1.5">
                <div class="flex items-center justify-between">
                  <label class="text-xs font-bold text-slate-700">Message</label>
                  <div class="flex gap-1 text-[10px]">
                    <button type="button" onclick="setWaTemplate('summary')" class="px-2 py-0.5 bg-slate-100 hover:bg-slate-200 rounded font-bold">Summary</button>
                    <button type="button" onclick="setWaTemplate('delay')" class="px-2 py-0.5 bg-slate-100 hover:bg-slate-200 rounded font-bold">Delay Update</button>
                    <button type="button" onclick="setWaTemplate('budget')" class="px-2 py-0.5 bg-slate-100 hover:bg-slate-200 rounded font-bold">Budget Update</button>
                    <button type="button" onclick="document.getElementById('wa-message-textarea').value=''" class="px-2 py-0.5 text-rose-600 hover:bg-rose-50 rounded font-bold">Clear</button>
                  </div>
                </div>
                <textarea id="wa-message-textarea" rows="4" class="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs text-slate-800 outline-none leading-relaxed">Project Update: King Khalid International Airport Branch – Terminal 5
Progress: 100%
Status: Active
Risk: High
Activities: 1</textarea>
              </div>

              <div class="p-3 bg-slate-50 rounded-xl border border-dashed border-slate-300 flex items-center justify-between">
                <input type="file" class="text-xs text-slate-600" />
                <div class="flex gap-2">
                  <button class="px-3 py-1 bg-white border border-slate-200 rounded-lg text-xs font-bold hover:bg-slate-50">Generate Project Data CSV</button>
                </div>
              </div>

              <div class="flex items-center gap-3 pt-2">
                <button type="button" onclick="sendViaWhatsApp()" class="flex-1 py-3 bg-[#059669] hover:bg-[#047857] text-white font-bold text-xs rounded-xl shadow transition flex items-center justify-center gap-2">
                  <i data-lucide="send" class="w-4 h-4"></i>
                  <span>Open WhatsApp & Send</span>
                </button>
                <button type="button" onclick="copyWaMessage()" class="px-4 py-3 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs rounded-xl transition">
                  Copy Message
                </button>
              </div>
            </div>

            <!-- Side Card: Instructions -->
            <div class="bg-white rounded-2xl border border-slate-100 p-5 shadow-sm space-y-4">
              <h3 class="font-bold text-xs text-[#0B1E3B] border-b border-slate-100 pb-2">How It Works</h3>
              <div class="space-y-3 text-xs text-slate-600">
                <div class="flex items-start gap-2">
                  <span class="w-5 h-5 rounded-full bg-emerald-100 text-emerald-800 font-bold flex items-center justify-center text-[10px] shrink-0">1</span>
                  <p>Pick a template or write a custom message to your site engineer.</p>
                </div>
                <div class="flex items-start gap-2">
                  <span class="w-5 h-5 rounded-full bg-emerald-100 text-emerald-800 font-bold flex items-center justify-center text-[10px] shrink-0">2</span>
                  <p>Optionally attach project data or generated PDF/Excel reports.</p>
                </div>
                <div class="flex items-start gap-2">
                  <span class="w-5 h-5 rounded-full bg-emerald-100 text-emerald-800 font-bold flex items-center justify-center text-[10px] shrink-0">3</span>
                  <p>Click "Open WhatsApp" to dispatch instantly via WhatsApp Web or mobile app.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- TAB 8: USER MANAGEMENT -->
        <section id="tab-user-mgmt" class="hidden space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 id="i18n-user-mgmt-title" class="text-lg font-black text-[#0B1E3B]">Global User Management</h2>
              <p id="i18n-user-mgmt-desc" class="text-xs text-slate-500">Accounts belong to the whole program, not one project.</p>
            </div>
            <button class="px-4 py-2 bg-[#0B1E3B] hover:bg-[#142A4E] text-white font-bold text-xs rounded-xl shadow transition">+ New User</button>
          </div>

          <div class="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
            <table class="w-full text-xs text-left border-collapse">
              <thead class="bg-slate-50 text-slate-400 font-bold border-b border-slate-100">
                <tr>
                  <th class="p-3.5">User</th>
                  <th class="p-3.5">Email</th>
                  <th class="p-3.5">Role</th>
                  <th class="p-3.5">Phone</th>
                  <th class="p-3.5">Status</th>
                  <th class="p-3.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 text-slate-700 font-medium">
                <tr class="hover:bg-slate-50">
                  <td class="p-3.5 font-bold text-slate-900">Asem Othman</td>
                  <td class="p-3.5 text-slate-500">asem.2007@hotmail.com</td>
                  <td class="p-3.5"><span class="px-2 py-0.5 bg-indigo-100 text-indigo-700 rounded text-[10px] font-bold">Admin</span></td>
                  <td class="p-3.5 text-slate-500">+966 50 555 4101</td>
                  <td class="p-3.5"><span class="px-2 py-0.5 bg-emerald-100 text-emerald-700 rounded text-[10px] font-bold">Active</span></td>
                  <td class="p-3.5 text-right"><button class="text-indigo-600 font-bold hover:underline">Edit</button></td>
                </tr>
                <tr class="hover:bg-slate-50">
                  <td class="p-3.5 font-bold text-slate-900">Saleh Mohammed</td>
                  <td class="p-3.5 text-slate-500">saleh@spma.com</td>
                  <td class="p-3.5"><span class="px-2 py-0.5 bg-blue-100 text-blue-700 rounded text-[10px] font-bold">Site Manager</span></td>
                  <td class="p-3.5 text-slate-500">+966 55 234 5678</td>
                  <td class="p-3.5"><span class="px-2 py-0.5 bg-emerald-100 text-emerald-700 rounded text-[10px] font-bold">Active</span></td>
                  <td class="p-3.5 text-right"><button class="text-indigo-600 font-bold hover:underline">Edit</button></td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- TAB 9: SETTINGS -->
        <section id="tab-settings" class="hidden space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <!-- Change Password -->
            <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm space-y-4">
              <h3 class="font-bold text-sm text-[#0B1E3B] border-b border-slate-100 pb-2">Change Password</h3>
              <div class="space-y-3">
                <div>
                  <label class="block text-xs font-bold text-slate-600 mb-1">Current Password</label>
                  <input type="password" class="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-xs outline-none focus:border-indigo-600" />
                </div>
                <div>
                  <label class="block text-xs font-bold text-slate-600 mb-1">New Password</label>
                  <input type="password" class="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-xs outline-none focus:border-indigo-600" />
                </div>
                <button class="px-5 py-2.5 bg-[#0B1E3B] hover:bg-[#142A4E] text-white text-xs font-bold rounded-xl shadow transition">Change Password</button>
              </div>
            </div>

            <!-- System Information -->
            <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm space-y-3">
              <h3 class="font-bold text-sm text-[#0B1E3B] border-b border-slate-100 pb-2">System Information</h3>
              <div class="space-y-1.5 text-xs text-slate-700">
                <p class="font-bold text-[#0B1E3B] text-sm">Smart Project Manager Assistant (SPMA)</p>
                <p class="text-slate-500 font-semibold">Blue Nile University - Faculty of Engineering</p>
                <p class="text-indigo-600 font-bold pt-2">Version 6.4 Activity Spent & EVM Engine</p>
              </div>
            </div>
          </div>
        </section>

      </div>
    </main>

  </div>

  <!-- Add Activity Modal -->
  <div id="add-activity-modal" class="hidden fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl border border-slate-200">
      <div class="flex items-center justify-between border-b border-slate-100 pb-3">
        <h3 class="font-bold text-sm text-[#0B1E3B]">Add New Activity</h3>
        <button onclick="closeAddActivityModal()" class="text-slate-400 hover:text-slate-700">✕</button>
      </div>
      <form onsubmit="handleAddActivitySubmit(event)" class="space-y-3">
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-600 mb-1">Activity Name</label>
            <input type="text" id="new-act-name" required placeholder="e.g. Steel Rebar Fixing" class="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 text-xs" />
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-600 mb-1">Status</label>
            <select id="new-act-status" class="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 text-xs">
              <option value="in_progress">In Progress</option>
              <option value="delayed">Delayed</option>
              <option value="completed">Completed</option>
            </select>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-600 mb-1">Planned End</label>
            <input type="date" id="new-act-end" value="2026-04-15" class="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 text-xs" />
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-600 mb-1">Actual %</label>
            <input type="number" id="new-act-prog" value="50" min="0" max="100" class="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 text-xs" />
          </div>
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-600 mb-1">Actual Spent (SAR)</label>
          <input type="number" id="new-act-spent" value="5000" class="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 text-xs" />
        </div>
        <div class="flex gap-2 pt-2">
          <button type="submit" class="flex-1 py-2 bg-[#0B1E3B] hover:bg-[#142A4E] text-white font-bold text-xs rounded-xl">Save Activity</button>
          <button type="button" onclick="closeAddActivityModal()" class="px-4 py-2 bg-slate-100 text-slate-700 font-bold text-xs rounded-xl">Cancel</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Add Project Modal -->
  <div id="add-project-modal" class="hidden fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl border border-slate-200">
      <div class="flex items-center justify-between border-b border-slate-100 pb-3">
        <h3 class="font-bold text-sm text-[#0B1E3B]">Create New Project</h3>
        <button onclick="closeAddProjectModal()" class="text-slate-400 hover:text-slate-700">✕</button>
      </div>
      <form onsubmit="handleAddProjectSubmit(event)" class="space-y-3">
        <div>
          <label class="block text-xs font-bold text-slate-600 mb-1">Project Name</label>
          <input type="text" id="new-prj-name" required placeholder="King Khalid International Airport Branch – Terminal 5" class="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 text-xs" />
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-600 mb-1">Project Code</label>
            <input type="text" id="new-prj-code" required placeholder="KKIA-T5" class="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 text-xs" />
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-600 mb-1">Budget (SAR)</label>
            <input type="number" id="new-prj-budget" value="931512.29" class="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 text-xs" />
          </div>
        </div>
        <div class="flex gap-2 pt-2">
          <button type="submit" class="flex-1 py-2 bg-[#0B1E3B] hover:bg-[#142A4E] text-white font-bold text-xs rounded-xl">Create Project</button>
          <button type="button" onclick="closeAddProjectModal()" class="px-4 py-2 bg-slate-100 text-slate-700 font-bold text-xs rounded-xl">Cancel</button>
        </div>
      </form>
    </div>
  </div>

  <!-- JAVASCRIPT LOGIC & BILINGUAL ENGINE -->
  <script>
    const I18N = {
      en: {
        loginThesisBadge: "B.Sc. Graduation Research Thesis • 2026",
        loginMainTitle: "Smart Project Manager Assistant (SPMA)",
        loginMainDesc: "Next-generation civil project intelligence combining Earned Value Management (EVM), Primavera XER schedule tracking, Multimodal Vision site inspections, and bilingual voice-driven AI agents.",
        loginTeamHead: "Graduation Research Team",
        loginCardTitle: "Welcome Back",
        loginCardSub: "Sign in to open the project intelligence workspace or evaluate the defense demo.",
        loginLblUser: "USERNAME",
        loginLblPass: "PASSWORD",
        loginBtnSign: "Sign In to Workspace",
        loginBtnDemo: "⚡ One-Click Graduation Demo Access",
        loginLangLabel: "العربية (Arabic)",
        
        navDashboard: "Dashboard",
        navProjects: "Projects",
        navActivities: "Activities",
        navAiAssistant: "AI Assistant",
        navReports: "Reports",
        navEngineerChat: "Engineer Chat",
        navWhatsappCenter: "WhatsApp Center",
        navUserMgmt: "User Management",
        navSettings: "Settings",
        teamTitle: "PROJECT TEAM",
        btnLogout: "Logout",
        btnRefresh: "Refresh",
        btnTopProject: "+ Project",
        dashHeroTitle: "Project Intelligence Workspace",
        dashHeroSub: "Live progress, cost, risk, deadlines and communication in one place.",
        btnNewProj: "New Project",
        btnSendUpdate: "Send Project Update",
        metricTotalProj: "Total Projects",
        metricActiveProj: "Active Projects",
        metricCompProj: "Completed Projects",
        metricDelayedAct: "Delayed Activities",
        metricBudgetUsed: "Budget Used",
        metricAvgProg: "Average Progress",
        cardAlertsTitle: "Executive Alerts",
        btnMarkRead: "Mark Read",
        cardWorkloadTitle: "Engineer Workload",
        cardTimelineTitle: "30-Day Timeline",
        portfolioPerfTitle: "Portfolio Performance",
        projHealthTitle: "Project Health",
        projectsTitle: "Projects",
        projectsDesc: "Create and monitor all projects in the portfolio.",
        btnNewProjTab: "+ New Project",
        activitiesTitle: "Activities",
        activitiesDesc: "Track planned and actual progress and upcoming deadlines.",
        btnNewActivityTab: "+ New Activity",
        aiTitle: "AI Assistant",
        aiDesc: "Ask questions based on live project, EVM calculations and schedule data.",
        reportsTitle: "Reports",
        reportsDesc: "Generate executive PDF reports and Excel sheets.",
        userMgmtTitle: "Global User Management",
        userMgmtDesc: "Accounts belong to the whole program, not one project."
      },
      ar: {
        loginThesisBadge: "مشروع وبحث التخرج المتقدم لنيل بكالوريوس الهندسة • 2026",
        loginMainTitle: "المساعد الذكي لمدير المشاريع الإنشائية (SPMA)",
        loginMainDesc: "المنظومة الذكية الرائدة لإدارة وهندسة المشاريع الإنشائية، تدمج تحليلات القيمة المكتسبة (EVM)، وجداول بريمافيرا XER، والفحص البصري للموقع، والمساعد الصوتي بالذكاء الاصطناعي.",
        loginTeamHead: "فريق إعداد وبحث المشروع",
        loginCardTitle: "تسجيل الدخول للنظام",
        loginCardSub: "سجّل الدخول للوصول إلى لوحة التحكم أو استخدم الدخول الفوري للجنة المناقشة.",
        loginLblUser: "اسم المستخدم",
        loginLblPass: "كلمة المرور",
        loginBtnSign: "تسجيل الدخول لمساحة العمل",
        loginBtnDemo: "⚡ دخول تجريبي فوري لمناقشة التخرج",
        loginLangLabel: "English",

        navDashboard: "لوحة التحكم (Dashboard)",
        navProjects: "المشاريع (Projects)",
        navActivities: "الأنشطة والجدول (Activities)",
        navAiAssistant: "المساعد الذكي (AI Assistant)",
        navReports: "التقارير الهندسية (Reports)",
        navEngineerChat: "محادثة المهندسين (Chat)",
        navWhatsappCenter: "مركز الواتساب (WhatsApp)",
        navUserMgmt: "إدارة المستخدمين (Users)",
        navSettings: "الإعدادات (Settings)",
        teamTitle: "فريق عمل المشروع",
        btnLogout: "تسجيل الخروج",
        btnRefresh: "تحديث البيانات",
        btnTopProject: "+ مشروع جديد",
        dashHeroTitle: "مساحة التحكم والذكاء الهندسي",
        dashHeroSub: "متابعة التقدم الميداني، التكاليف، المخاطر، والاتصال في منصة موحدة.",
        btnNewProj: "مشروع جديد",
        btnSendUpdate: "إرسال تحديث للمشروع",
        metricTotalProj: "إجمالي المشاريع",
        metricActiveProj: "المشاريع النشطة",
        metricCompProj: "المشاريع المكتملة",
        metricDelayedAct: "الأنشطة المتأخرة",
        metricBudgetUsed: "نسبة الصرف",
        metricAvgProg: "متوسط الإنجاز",
        cardAlertsTitle: "التنبيهات التنفيذية المبكرة",
        btnMarkRead: "تحديد كمقروء",
        cardWorkloadTitle: "أعباء عمل المهندسين",
        cardTimelineTitle: "الجدول الزمني (30 يوماً)",
        portfolioPerfTitle: "أداء محفظة المشاريع",
        projHealthTitle: "مؤشر صحة المشروع",
        projectsTitle: "سجل المشاريع",
        projectsDesc: "إنشاء ومراقبة كافة مشروعات المحفظة الهندسية.",
        btnNewProjTab: "+ إضافة مشروع",
        activitiesTitle: "جدول أنشطة وبنود المشروع",
        activitiesDesc: "تتبع التقدم المخطط والفعلي ومواعيد التسليم الحرجة.",
        btnNewActivityTab: "+ إضافة نشاط",
        aiTitle: "المساعد الهندسي الذكي",
        aiDesc: "اسأل المساعد الذكي عن أي بيانات أو تحليلات تخص المشروع مباشرة.",
        reportsTitle: "توليد التقارير الرسمية",
        reportsDesc: "استخراج تقارير PDF المعتمدة وشيتات الإكسيل بضغطة زر.",
        userMgmtTitle: "إدارة المستخدمين والصلاحيات",
        userMgmtDesc: "إدارة حسابات المهندسين وفرق العمل في المحفظة."
      }
    };

    let currentLang = 'en';
    let currentTab = 'dashboard';
    let currentSessionId = 'sess_' + Math.random().toString(36).substring(2, 9);

    function toggleLanguage() {
      currentLang = currentLang === 'en' ? 'ar' : 'en';
      document.documentElement.lang = currentLang;
      document.documentElement.dir = currentLang === 'ar' ? 'rtl' : 'ltr';
      
      const t = I18N[currentLang];
      
      // Update Login Page translations
      const elThesis = document.getElementById('i18n-login-thesis-badge');
      if (elThesis) elThesis.textContent = t.loginThesisBadge;
      const elMainT = document.getElementById('i18n-login-main-title');
      if (elMainT) elMainT.innerHTML = currentLang === 'ar' ? 'المساعد الذكي لمدير المشاريع <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-emerald-400">(SPMA)</span>' : 'Smart Project Manager Assistant <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-emerald-400">(SPMA)</span>';
      const elMainD = document.getElementById('i18n-login-main-desc');
      if (elMainD) elMainD.textContent = t.loginMainDesc;
      const elTeamH = document.getElementById('i18n-login-team-head');
      if (elTeamH) elTeamH.innerHTML = `<i data-lucide="users" class="w-3.5 h-3.5"></i><span>${t.loginTeamHead}</span>`;
      const elCardT = document.getElementById('i18n-login-card-title');
      if (elCardT) elCardT.textContent = t.loginCardTitle;
      const elCardS = document.getElementById('i18n-login-card-sub');
      if (elCardS) elCardS.textContent = t.loginCardSub;
      const elLblU = document.getElementById('i18n-login-lbl-user');
      if (elLblU) elLblU.textContent = t.loginLblUser;
      const elLblP = document.getElementById('i18n-login-lbl-pass');
      if (elLblP) elLblP.textContent = t.loginLblPass;
      const elBtnS = document.getElementById('i18n-login-btn-sign');
      if (elBtnS) elBtnS.textContent = t.loginBtnSign;
      const elBtnD = document.getElementById('i18n-login-btn-demo');
      if (elBtnD) elBtnD.textContent = t.loginBtnDemo;
      const elLangLbl = document.getElementById('login-lang-label');
      if (elLangLbl) elLangLbl.textContent = t.loginLangLabel;

      // Update Main App translations
      const idMap = {
        'i18n-nav-dashboard': t.navDashboard,
        'i18n-nav-projects': t.navProjects,
        'i18n-nav-activities': t.navActivities,
        'i18n-nav-ai-assistant': t.navAiAssistant,
        'i18n-nav-reports': t.navReports,
        'i18n-nav-engineer-chat': t.navEngineerChat,
        'i18n-nav-whatsapp-center': t.navWhatsappCenter,
        'i18n-nav-user-mgmt': t.navUserMgmt,
        'i18n-nav-settings': t.navSettings,
        'i18n-team-title': t.teamTitle,
        'btn-logout': t.btnLogout,
        'i18n-btn-top-project': t.btnTopProject,
        'i18n-dash-hero-title': t.dashHeroTitle,
        'i18n-dash-hero-sub': t.dashHeroSub,
        'i18n-btn-new-proj': t.btnNewProj,
        'i18n-btn-send-update': t.btnSendUpdate,
        'i18n-metric-total-proj': t.metricTotalProj,
        'i18n-metric-active-proj': t.metricActiveProj,
        'i18n-metric-comp-proj': t.metricCompProj,
        'i18n-metric-delayed-act': t.metricDelayedAct,
        'i18n-metric-budget-used': t.metricBudgetUsed,
        'i18n-metric-avg-prog': t.metricAvgProg,
        'i18n-card-alerts-title': t.cardAlertsTitle,
        'i18n-btn-mark-read': t.btnMarkRead,
        'i18n-card-workload-title': t.cardWorkloadTitle,
        'i18n-card-timeline-title': t.cardTimelineTitle,
        'i18n-portfolio-perf-title': t.portfolioPerfTitle,
        'i18n-proj-health-title': t.projHealthTitle,
        'i18n-projects-title': t.projectsTitle,
        'i18n-projects-desc': t.projectsDesc,
        'i18n-btn-new-proj-tab': t.btnNewProjTab,
        'i18n-activities-title': t.activitiesTitle,
        'i18n-activities-desc': t.activitiesDesc,
        'i18n-btn-new-activity-tab': t.btnNewActivityTab,
        'i18n-ai-title': t.aiTitle,
        'i18n-ai-desc': t.aiDesc,
        'i18n-reports-title': t.reportsTitle,
        'i18n-reports-desc': t.reportsDesc,
        'i18n-user-mgmt-title': t.userMgmtTitle,
        'i18n-user-mgmt-desc': t.userMgmtDesc,
        'lang-label': currentLang === 'en' ? 'عربي' : 'EN'
      };

      for (const [id, val] of Object.entries(idMap)) {
        const el = document.getElementById(id);
        if (el) el.textContent = val;
      }

      lucide.createIcons();
    }

    function switchTab(tabId) {
      currentTab = tabId;
      const allTabs = ['dashboard', 'projects', 'activities', 'ai-assistant', 'reports', 'engineer-chat', 'whatsapp-center', 'user-mgmt', 'settings'];
      
      allTabs.forEach(t => {
        const sec = document.getElementById(`tab-${t}`);
        const nav = document.getElementById(`nav-${t}`);
        if (sec) sec.classList.add('hidden');
        if (nav) {
          nav.classList.remove('bg-slate-800/80', 'text-white', 'font-bold', 'border', 'border-slate-700/60', 'shadow-sm');
          nav.classList.add('text-slate-300');
        }
      });

      const activeSec = document.getElementById(`tab-${tabId}`);
      const activeNav = document.getElementById(`nav-${tabId}`);
      if (activeSec) activeSec.classList.remove('hidden');
      if (activeNav) {
        activeNav.classList.add('bg-slate-800/80', 'text-white', 'font-bold', 'border', 'border-slate-700/60', 'shadow-sm');
        activeNav.classList.remove('text-slate-300');
      }

      const titleMap = {
        'dashboard': 'Dashboard',
        'projects': 'Projects',
        'activities': 'Activities',
        'ai-assistant': 'AI Assistant',
        'reports': 'Reports',
        'engineer-chat': 'Engineer Chat',
        'whatsapp-center': 'WhatsApp Center',
        'user-mgmt': 'User Management',
        'settings': 'Settings'
      };
      document.getElementById('top-title').textContent = titleMap[tabId] || 'Dashboard';
      lucide.createIcons();
    }

    // Authentication & Full-Screen Login Portal Logic
    function showLoginPortal() {
      const loginView = document.getElementById('login-view');
      const appView = document.getElementById('app-view');
      loginView.classList.remove('hidden');
      appView.classList.add('hidden');
      appView.classList.remove('flex');
      localStorage.setItem('spma_auth', 'false');
      lucide.createIcons();
    }

    function enterWorkspace() {
      const loginView = document.getElementById('login-view');
      const appView = document.getElementById('app-view');
      loginView.classList.add('hidden');
      appView.classList.remove('hidden');
      appView.classList.add('flex');
      localStorage.setItem('spma_auth', 'true');
      lucide.createIcons();
    }

    function handleLoginSubmit(e) {
      if (e) e.preventDefault();
      enterWorkspace();
    }

    function handleQuickDemoLogin() {
      document.getElementById('login-username').value = 'admin';
      document.getElementById('login-password').value = 'Admin@123';
      enterWorkspace();
    }

    function handleLogout() {
      showLoginPortal();
    }

    function togglePasswordVisibility() {
      const pass = document.getElementById('login-password');
      const icon = document.getElementById('pass-eye-icon');
      if (pass.type === 'password') {
        pass.type = 'text';
        icon.setAttribute('data-lucide', 'eye-off');
      } else {
        pass.type = 'password';
        icon.setAttribute('data-lucide', 'eye');
      }
      lucide.createIcons();
    }

    // Project Switcher
    function switchActiveProject(prjKey) {
      console.log('Switched project to:', prjKey);
    }

    // Chat Logic
    async function handleChatSubmit() {
      const input = document.getElementById('chat-input');
      const text = input.value.trim();
      if (!text) return;
      input.value = '';

      const container = document.getElementById('chat-messages-container');
      
      // User message
      const userDiv = document.createElement('div');
      userDiv.className = 'flex items-start gap-3 max-w-2xl ml-auto flex-row-reverse';
      userDiv.innerHTML = `
        <div class="w-8 h-8 rounded-xl bg-indigo-600 text-white font-bold flex items-center justify-center shrink-0">AO</div>
        <div class="p-4 bg-[#0B1E3B] text-white rounded-2xl shadow-sm text-xs space-y-1">
          <p>${text}</p>
        </div>
      `;
      container.appendChild(userDiv);

      // Bot loading placeholder
      const botDiv = document.createElement('div');
      botDiv.className = 'flex items-start gap-3 max-w-2xl';
      botDiv.innerHTML = `
        <div class="w-8 h-8 rounded-xl bg-[#0B1E3B] text-white flex items-center justify-center shrink-0 shadow-sm">
          <i data-lucide="bot" class="w-4 h-4 text-indigo-400"></i>
        </div>
        <div class="p-4 bg-slate-50 rounded-2xl border border-slate-100 text-slate-800 space-y-2 text-xs">
          <p class="text-slate-400 animate-pulse">جاري المعالجة وحساب مؤشرات المشروع...</p>
        </div>
      `;
      container.appendChild(botDiv);
      container.scrollTop = container.scrollHeight;
      lucide.createIcons();

      try {
        const res = await fetch('/api/chat/message', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text, session_id: currentSessionId })
        });
        const data = await res.json();
        
        const rawResponse = data.response || data.reply || data.message || '';
        let replyHtml = '';
        if (rawResponse) {
          replyHtml = marked.parse(rawResponse);
        } else {
          replyHtml = 'تم استلام الطلب ومعالجة بيانات المشروع بنجاح.';
        }

        botDiv.querySelector('div:nth-child(2)').innerHTML = `
          <div class="flex items-center justify-between border-b border-slate-200/60 pb-1.5 mb-2">
            <span class="font-bold text-[#0B1E3B] flex items-center gap-1.5">
              <i data-lucide="sparkles" class="w-3.5 h-3.5 text-indigo-600"></i>
              <span>Smart Assistant (Gemini 2.5 Flash)</span>
            </span>
            <span class="text-[10px] text-emerald-600 font-bold bg-emerald-50 px-2 py-0.5 rounded-full">Live Project Sync</span>
          </div>
          <div class="markdown-content text-slate-700 leading-relaxed text-xs space-y-2">${replyHtml}</div>
        `;
        container.scrollTop = container.scrollHeight;
        lucide.createIcons();
      } catch (err) {
        botDiv.querySelector('div:nth-child(2)').innerHTML = `
          <p class="font-bold text-rose-600">Smart Assistant (Offline Fallback)</p>
          <p class="text-slate-700">نسبة إنجاز مشروع مطار الملك خالد - الصالة 5 هي 100%، والتكلفة الفعلية المسجلة 1,000 ريال سعودي من إجمالي ميزانية 931,512.29 ريال.</p>
        `;
      }
    }

    function askQuickPrompt(q) {
      document.getElementById('chat-input').value = q;
      handleChatSubmit();
    }

    // Engineer Chat
    function addEmojiToEngChat(emoji) {
      const input = document.getElementById('eng-chat-input');
      input.value += emoji;
      input.focus();
    }

    function handleEngChatSubmit(e) {
      e.preventDefault();
      const input = document.getElementById('eng-chat-input');
      const text = input.value.trim();
      if (!text) return;
      input.value = '';

      const stream = document.getElementById('eng-chat-stream');
      const msgDiv = document.createElement('div');
      msgDiv.className = 'p-3 bg-indigo-50/80 rounded-xl border border-indigo-100 space-y-1 max-w-md ml-auto';
      msgDiv.innerHTML = `
        <div class="flex items-center justify-between text-[11px] font-bold text-[#0B1E3B]">
          <span>Asem Othman (You)</span>
          <span class="text-[9px] text-slate-400">Just now</span>
        </div>
        <p class="text-slate-700 text-xs">${text}</p>
      `;
      stream.appendChild(msgDiv);
      stream.scrollTop = stream.scrollHeight;
    }

    // WhatsApp Helpers
    function openWhatsAppFor(name, phone) {
      switchTab('whatsapp-center');
      document.getElementById('wa-phone-input').value = phone;
      document.getElementById('wa-message-textarea').value = `Hello ${name},\\nHere is the latest progress update for King Khalid International Airport Branch – Terminal 5.`;
    }
    function updateWaRecipient(phone) {
      document.getElementById('wa-phone-input').value = phone;
    }
    function setWaTemplate(type) {
      const area = document.getElementById('wa-message-textarea');
      if (type === 'summary') {
        area.value = 'Project Update: King Khalid International Airport Branch – Terminal 5\\nProgress: 100%\\nStatus: Active\\nRisk: High\\nActivities: 1';
      } else if (type === 'delay') {
        area.value = 'URGENT DELAY ALERT: King Khalid International Airport Branch – Terminal 5\\nActivity: concrete is delayed.\\nAction Required: Site Manager to review mitigation.';
      } else if (type === 'budget') {
        area.value = 'Budget Summary: King Khalid International Airport Branch – Terminal 5\\nTotal Budget: SAR 931,512.29\\nSpent to date: SAR 1,000.00\\nRemaining: SAR 930,512.29';
      }
    }
    function sendViaWhatsApp() {
      const phone = document.getElementById('wa-phone-input').value.trim();
      const text = encodeURIComponent(document.getElementById('wa-message-textarea').value.trim());
      window.open(`https://wa.me/${phone}?text=${text}`, '_blank');
    }
    function copyWaMessage() {
      const text = document.getElementById('wa-message-textarea').value;
      navigator.clipboard.writeText(text).then(() => alert('Message copied to clipboard!'));
    }

    // Modals
    function openAddActivityModal() {
      document.getElementById('add-activity-modal').classList.remove('hidden');
    }
    function closeAddActivityModal() {
      document.getElementById('add-activity-modal').classList.add('hidden');
    }
    function handleAddActivitySubmit(e) {
      e.preventDefault();
      alert('Activity saved successfully!');
      closeAddActivityModal();
    }

    function openAddProjectModal() {
      document.getElementById('add-project-modal').classList.remove('hidden');
    }
    function closeAddProjectModal() {
      document.getElementById('add-project-modal').classList.add('hidden');
    }
    function handleAddProjectSubmit(e) {
      e.preventDefault();
      alert('Project created successfully!');
      closeAddProjectModal();
    }

    function markAlertsRead() {
      alert('All executive alerts marked as read.');
    }
    function refreshCurrentPage() {
      location.reload();
    }

    // Voice & Vision
    async function toggleVoiceRecording() {
      if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert('Voice speech recognition not supported in this browser. Please use Chrome or Edge.');
        return;
      }
      const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
      const rec = new SpeechRec();
      rec.lang = currentLang === 'ar' ? 'ar-SA' : 'en-US';
      const btn = document.getElementById('voice-btn');
      btn.classList.add('bg-rose-500', 'text-white', 'animate-pulse');
      
      rec.onresult = (evt) => {
        const transcript = evt.results[0][0].transcript;
        document.getElementById('chat-input').value = transcript;
        btn.classList.remove('bg-rose-500', 'text-white', 'animate-pulse');
        handleChatSubmit();
      };
      rec.onerror = () => {
        btn.classList.remove('bg-rose-500', 'text-white', 'animate-pulse');
      };
      rec.start();
    }

    async function handleVisionImageUpload(evt) {
      const file = evt.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append('file', file);
      formData.append('prompt', 'Inspect site image for progress, rebar quality, and safety');

      const container = document.getElementById('chat-messages-container');
      const userDiv = document.createElement('div');
      userDiv.className = 'flex items-start gap-3 max-w-2xl ml-auto flex-row-reverse';
      userDiv.innerHTML = `
        <div class="w-8 h-8 rounded-xl bg-indigo-600 text-white font-bold flex items-center justify-center shrink-0">AO</div>
        <div class="p-4 bg-[#0B1E3B] text-white rounded-2xl shadow-sm text-xs space-y-1">
          <p>📸 Uploaded site photo for AI Vision Analysis: <b>${file.name}</b></p>
        </div>
      `;
      container.appendChild(userDiv);

      try {
        const res = await fetch('/api/vision/inspect', {
          method: 'POST',
          body: formData
        });
        const data = await res.json();
        const botDiv = document.createElement('div');
        botDiv.className = 'flex items-start gap-3 max-w-2xl';
        botDiv.innerHTML = `
          <div class="w-8 h-8 rounded-xl bg-[#0B1E3B] text-white flex items-center justify-center shrink-0 shadow-sm">
            <i data-lucide="bot" class="w-4 h-4 text-indigo-400"></i>
          </div>
          <div class="p-4 bg-slate-50 rounded-2xl border border-slate-100 text-slate-800 space-y-2 text-xs">
            <p class="font-bold text-[#0B1E3B]">Computer Vision Analysis Result</p>
            <div class="markdown-content text-slate-700 leading-relaxed">${marked.parse(data.analysis || data.message || 'Image analyzed successfully.')}</div>
          </div>
        `;
        container.appendChild(botDiv);
        container.scrollTop = container.scrollHeight;
        lucide.createIcons();
      } catch (err) {
        alert('Failed to analyze image with vision engine.');
      }
    }

    // Auto-init on page load
    window.addEventListener('DOMContentLoaded', () => {
      lucide.createIcons();
      // Check auth status
      const auth = localStorage.getItem('spma_auth');
      if (auth === 'true') {
        enterWorkspace();
      } else {
        showLoginPortal();
      }
    });
  </script>
</body>
</html>
'''

target_path = os.path.join(os.path.dirname(__file__), 'app', 'static', 'index.html')
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(html_code)

print(f"Successfully updated {target_path}!")
