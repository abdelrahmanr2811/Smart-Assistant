import os

# Complete Pixel-Perfect Enterprise SaaS SPMA Web Application Generator
# Featuring Full Dark/Light Theme Engine, Arabic/English i18n, Lucide Icons, Full Modals, and API Integrations

html_content = r'''<!DOCTYPE html>
<html lang="en" dir="ltr" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>Smart Project Manager Assistant (SPMA) - Blue Nile University</title>
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              50: '#F0F5FF',
              100: '#E5EDFF',
              500: '#3B82F6',
              600: '#2563EB',
              800: '#1E3A8A',
              900: '#0B1E3B',
              950: '#071326',
            }
          }
        }
      }
    }
  </script>

  <!-- Marked Markdown Parser & Lucide Icons -->
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <script src="https://unpkg.com/lucide@latest"></script>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    :root {
      --bg-dark-primary: #071326;
      --bg-dark-card: #0B1E3B;
      --bg-dark-sub: #0E2447;
      --border-dark: #1E3A66;
    }

    select option {
      background-color: #0B1E3B !important;
      color: #F8FAFC !important;
    }
    html:not(.dark) select option {
      background-color: #FFFFFF !important;
      color: #0F172A !important;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      transition: background-color 0.2s ease, color 0.2s ease;
    }
    
    html[dir="rtl"] body {
      font-family: 'Cairo', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .custom-scrollbar::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: transparent;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: #94A3B8;
      border-radius: 4px;
    }
    .dark .custom-scrollbar::-webkit-scrollbar-thumb {
      background: #1E3A66;
    }

    .custom-scrollbar-dark::-webkit-scrollbar {
      width: 4px;
    }
    .custom-scrollbar-dark::-webkit-scrollbar-track {
      background: transparent;
    }
    .custom-scrollbar-dark::-webkit-scrollbar-thumb {
      background: #1E3A66;
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
      border: 1px solid rgba(148, 163, 184, 0.2);
      padding: 6px 10px;
    }
    .markdown-content th {
      background: rgba(148, 163, 184, 0.1);
      font-weight: 700;
    }

    .blueprint-pattern {
      background-color: #F8FAFC;
      background-image: 
        radial-gradient(rgba(99, 102, 241, 0.15) 1px, transparent 0),
        linear-gradient(to right, rgba(148, 163, 184, 0.15) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(148, 163, 184, 0.15) 1px, transparent 1px);
      background-size: 24px 24px, 48px 48px, 48px 48px;
      transition: background-color 0.3s ease;
    }
    html.dark .blueprint-pattern {
      background-color: #061124;
      background-image: 
        radial-gradient(rgba(59, 130, 246, 0.15) 1px, transparent 0),
        linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
    }
    .pulse-glow {
      box-shadow: 0 0 25px rgba(16, 185, 129, 0.35);
    }
    .modal-overlay {
      background-color: rgba(7, 19, 38, 0.8);
      backdrop-filter: blur(8px);
    }

    /* Mobile Drawer Responsive Styles & RTL/LTR Safety */
    @media (max-width: 767px) {
      #main-sidebar {
        position: fixed !important;
        top: 0 !important;
        bottom: 0 !important;
        z-index: 50 !important;
        width: 18rem !important;
        max-width: 85vw !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7) !important;
        transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
      }
      html[dir="ltr"] #main-sidebar {
        left: 0 !important;
        right: auto !important;
        transform: translateX(-100%);
      }
      html[dir="rtl"] #main-sidebar {
        right: 0 !important;
        left: auto !important;
        transform: translateX(100%);
      }
      html[dir="ltr"] #main-sidebar.mobile-open,
      html[dir="rtl"] #main-sidebar.mobile-open {
        transform: translateX(0) !important;
      }
    }
    @media (min-width: 768px) {
      #main-sidebar {
        position: static !important;
        transform: none !important;
      }
    }

    /* Safe Area Inset Support for Mobile Notch & Gesture Bar */
    #mobile-bottom-nav {
      padding-bottom: calc(0.35rem + env(safe-area-inset-bottom, 0px));
    }
  </style>
  <link rel="manifest" href="/static/manifest.json">
  <meta name="theme-color" content="#0B1E3B">
</head>
<body class="h-screen w-screen overflow-hidden select-none bg-[#F8FAFC] dark:bg-[#071326] text-slate-800 dark:text-slate-100">

  <!-- ========================================================================= -->
  <!-- 1. STANDALONE LUXURY FULL-SCREEN LOGIN VIEW (LANDING PORTAL)               -->
  <!-- ========================================================================= -->
  <div id="login-view" class="fixed inset-0 min-h-screen w-full z-50 flex flex-col justify-between blueprint-pattern text-slate-800 dark:text-slate-100 overflow-y-auto custom-scrollbar p-4 md:p-8 transition-colors">
    
    <!-- Top Bar of Login Page -->
    <header class="w-full max-w-7xl mx-auto flex items-center justify-between py-3 border-b border-slate-200 dark:border-slate-800/80 transition-colors">
      <div class="flex items-center gap-3">
        <div class="w-12 h-12 bg-white rounded-2xl p-1.5 shadow-xl border border-slate-200 dark:border-slate-200/20 flex items-center justify-center shrink-0">
          <img src="/static/brand/blue_nile_logo.png" alt="University Logo" class="w-full h-full object-contain" />
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span class="text-[10px] font-black tracking-widest text-indigo-600 dark:text-indigo-400 uppercase">BLUE NILE UNIVERSITY</span>
            <span class="text-[9px] px-2 py-0.5 bg-indigo-50 dark:bg-indigo-950/90 border border-indigo-200 dark:border-indigo-700/60 text-indigo-700 dark:text-indigo-300 rounded-full font-extrabold">Faculty of Engineering</span>
          </div>
          <h1 class="text-base font-black text-slate-900 dark:text-white tracking-wide">Smart Project Manager Assistant (SPMA)</h1>
        </div>
      </div>

      <div class="flex items-center gap-2.5">
        <div class="hidden sm:flex items-center gap-2 px-3.5 py-1.5 bg-white dark:bg-slate-900/90 border border-slate-200 dark:border-slate-800 rounded-full text-xs text-slate-700 dark:text-slate-300 shadow-sm">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="text-[11px] font-bold">Core AI Engine v6.4 Active</span>
        </div>

        <!-- Theme Toggle (Dark / Light Mode) on Login Page -->
        <button type="button" onclick="toggleTheme()" id="login-theme-toggle-btn" title="Toggle Theme (Dark / Light)" class="p-2.5 bg-white dark:bg-slate-800/90 hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 shadow-md transition flex items-center justify-center cursor-pointer">
          <i data-lucide="sun" id="login-theme-icon" class="w-4 h-4 text-amber-400"></i>
        </button>

        <!-- Language Switcher on Login Page -->
        <button type="button" onclick="toggleLanguage()" class="px-4 py-2 bg-white dark:bg-slate-800/90 hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-800 dark:text-white rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 shadow-md transition flex items-center gap-2 cursor-pointer">
          <i data-lucide="globe" class="w-4 h-4 text-indigo-600 dark:text-indigo-400"></i>
          <span id="login-lang-label">العربية (Arabic)</span>
        </button>
      </div>
    </header>

    <!-- Main Centerpiece: Split Showcase & Sign-In Card -->
    <main class="w-full max-w-7xl mx-auto my-auto py-6">
      <div class="bg-white/95 dark:bg-[#0B1E3B]/95 backdrop-blur-2xl rounded-3xl border border-slate-200 dark:border-slate-700/70 shadow-2xl overflow-hidden grid grid-cols-1 lg:grid-cols-12 transition-colors">
        
        <!-- LEFT COLUMN (7 Cols): Project Presentation, EVM Showcase & Team -->
        <div class="lg:col-span-7 order-2 lg:order-1 p-5 sm:p-7 md:p-10 flex flex-col justify-between space-y-6 relative border-t lg:border-t-0 lg:border-r border-slate-200 dark:border-slate-800">
          <div class="space-y-5">
            
            <!-- Badge & University Title -->
            <div class="space-y-2">
              <div class="inline-flex items-center gap-2 px-3.5 py-1 bg-indigo-50 dark:bg-indigo-500/10 border border-indigo-200 dark:border-indigo-500/30 text-indigo-700 dark:text-indigo-300 text-xs font-black rounded-full uppercase tracking-wider">
                <i data-lucide="graduation-cap" class="w-4 h-4"></i>
                <span id="i18n-login-thesis-badge">B.Sc. Graduation Research Thesis • 2026</span>
              </div>
              <h2 id="i18n-login-main-title" class="text-2xl md:text-3xl font-black text-slate-900 dark:text-white leading-tight tracking-tight">
                Smart Project Manager Assistant <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-500 to-emerald-500 dark:from-indigo-400 dark:to-emerald-400">(SPMA)</span>
              </h2>
              <p id="i18n-login-main-desc" class="text-xs md:text-sm text-slate-600 dark:text-slate-300 leading-relaxed max-w-2xl font-normal">
                Next-generation civil project intelligence combining Earned Value Management (EVM), Primavera XER schedule tracking, Multimodal Vision site inspections, and bilingual voice-driven AI agents.
              </p>
            </div>

            <!-- 6 Core Feature Highlights Grid -->
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 pt-1">
              <div class="p-3 bg-slate-50 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 hover:border-indigo-500/40 rounded-2xl space-y-1 transition">
                <div class="flex items-center gap-2 text-indigo-600 dark:text-indigo-400">
                  <i data-lucide="trending-up" class="w-4 h-4"></i>
                  <span class="text-xs font-bold">EVM & S-Curve</span>
                </div>
                <p class="text-[10px] text-slate-500 dark:text-slate-400 leading-tight">Live SPI, CPI, SV, CV and critical path analytics.</p>
              </div>

              <div class="p-3 bg-slate-50 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 hover:border-indigo-500/40 rounded-2xl space-y-1 transition">
                <div class="flex items-center gap-2 text-indigo-600 dark:text-indigo-400">
                  <i data-lucide="bot" class="w-4 h-4"></i>
                  <span class="text-xs font-bold">Gemini 2.5 Agent</span>
                </div>
                <p class="text-[10px] text-slate-500 dark:text-slate-400 leading-tight">Zero-hallucination grounded project computations.</p>
              </div>

              <div class="p-3 bg-slate-50 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 hover:border-indigo-500/40 rounded-2xl space-y-1 transition">
                <div class="flex items-center gap-2 text-indigo-600 dark:text-indigo-400">
                  <i data-lucide="mic" class="w-4 h-4"></i>
                  <span class="text-xs font-bold">Voice Processing</span>
                </div>
                <p class="text-[10px] text-slate-500 dark:text-slate-400 leading-tight">Bilingual Arabic & English site speech commands.</p>
              </div>

              <div class="p-3 bg-slate-50 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 hover:border-indigo-500/40 rounded-2xl space-y-1 transition">
                <div class="flex items-center gap-2 text-indigo-600 dark:text-indigo-400">
                  <i data-lucide="camera" class="w-4 h-4"></i>
                  <span class="text-xs font-bold">Vision Inspection</span>
                </div>
                <p class="text-[10px] text-slate-500 dark:text-slate-400 leading-tight">Site photo analysis and structural compliance checking.</p>
              </div>

              <div class="p-3 bg-slate-50 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 hover:border-emerald-500/40 rounded-2xl space-y-1 transition">
                <div class="flex items-center gap-2 text-emerald-600 dark:text-emerald-400">
                  <i data-lucide="phone-call" class="w-4 h-4"></i>
                  <span class="text-xs font-bold">WhatsApp Sync</span>
                </div>
                <p class="text-[10px] text-slate-500 dark:text-slate-400 leading-tight">Field logs, voice notes & auto-broadcast dispatching.</p>
              </div>

              <div class="p-3 bg-slate-50 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 hover:border-amber-500/40 rounded-2xl space-y-1 transition">
                <div class="flex items-center gap-2 text-amber-600 dark:text-amber-400">
                  <i data-lucide="file-check" class="w-4 h-4"></i>
                  <span class="text-xs font-bold">FIDIC & Reports</span>
                </div>
                <p class="text-[10px] text-slate-500 dark:text-slate-400 leading-tight">Official PDF/Excel generation and IPC monthly billing.</p>
              </div>
            </div>

            <!-- Graduation Project Team Card -->
            <div class="p-4 bg-slate-50 dark:bg-slate-900/90 border border-indigo-100 dark:border-indigo-900/40 rounded-2xl space-y-3 shadow-inner transition-colors">
              <div class="flex items-center justify-between">
                <span id="i18n-login-team-head" class="text-xs font-extrabold text-indigo-700 dark:text-indigo-300 uppercase tracking-wider flex items-center gap-2">
                  <i data-lucide="users" class="w-4 h-4"></i>
                  <span>Graduation Research Team (فريق إعداد وبحث المشروع)</span>
                </span>
                <span class="text-[10px] font-bold text-slate-500 dark:text-slate-400">Faculty of Engineering</span>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                <!-- Member 1: Mohammed Gassim -->
                <div class="flex items-center gap-2.5 p-2 bg-white dark:bg-slate-950/60 rounded-xl border border-slate-200 dark:border-slate-800 shadow-2xs">
                  <div class="w-8 h-8 rounded-xl bg-indigo-600 text-white font-black text-xs flex items-center justify-center shrink-0 shadow">MG</div>
                  <div class="overflow-hidden">
                    <p class="font-bold text-slate-900 dark:text-white text-[11px] truncate">Engr. Mohammed Gassim</p>
                    <p class="text-[9px] text-indigo-600 dark:text-indigo-300">Site Operations & Execution</p>
                  </div>
                </div>

                <!-- Member 2: Asem Othman -->
                <div class="flex items-center gap-2.5 p-2 bg-white dark:bg-slate-950/60 rounded-xl border border-slate-200 dark:border-slate-800 shadow-2xs">
                  <div class="w-8 h-8 rounded-xl bg-slate-100 dark:bg-slate-800 text-indigo-700 dark:text-indigo-300 font-black text-xs flex items-center justify-center shrink-0">AO</div>
                  <div class="overflow-hidden">
                    <p class="font-bold text-slate-900 dark:text-white text-[11px] truncate">Engr. Asem Othman</p>
                    <p class="text-[9px] text-slate-500 dark:text-slate-400">Team Leader & Full-Stack Architect</p>
                  </div>
                </div>

                <!-- Member 3: Saleh Mohammed -->
                <div class="flex items-center gap-2.5 p-2 bg-white dark:bg-slate-950/60 rounded-xl border border-slate-200 dark:border-slate-800 shadow-2xs">
                  <div class="w-8 h-8 rounded-xl bg-slate-100 dark:bg-slate-800 text-indigo-700 dark:text-indigo-300 font-black text-xs flex items-center justify-center shrink-0">SM</div>
                  <div class="overflow-hidden">
                    <p class="font-bold text-slate-900 dark:text-white text-[11px] truncate">Engr. Saleh Mohammed</p>
                    <p class="text-[9px] text-slate-500 dark:text-slate-400">Planning & EVM Engine</p>
                  </div>
                </div>

                <!-- Member 4: Rafat Mohammed -->
                <div class="flex items-center gap-2.5 p-2 bg-white dark:bg-slate-950/60 rounded-xl border border-slate-200 dark:border-slate-800 shadow-2xs">
                  <div class="w-8 h-8 rounded-xl bg-slate-100 dark:bg-slate-800 text-indigo-700 dark:text-indigo-300 font-black text-xs flex items-center justify-center shrink-0">RM</div>
                  <div class="overflow-hidden">
                    <p class="font-bold text-slate-900 dark:text-white text-[11px] truncate">Engr. Rafat Mohammed</p>
                    <p class="text-[9px] text-slate-500 dark:text-slate-400">QA/QC & Site Vision</p>
                  </div>
                </div>

                <!-- Member 5: Abu baker Mohammed -->
                <div class="flex items-center gap-2.5 p-2 bg-white dark:bg-slate-950/60 rounded-xl border border-slate-200 dark:border-slate-800 shadow-2xs sm:col-span-2">
                  <div class="w-8 h-8 rounded-xl bg-slate-100 dark:bg-slate-800 text-indigo-700 dark:text-indigo-300 font-black text-xs flex items-center justify-center shrink-0">AM</div>
                  <div class="overflow-hidden">
                    <p class="font-bold text-slate-900 dark:text-white text-[11px] truncate">Engr. Abu baker Mohammed</p>
                    <p class="text-[9px] text-slate-500 dark:text-slate-400">Cost Engineering & FIDIC Contracts</p>
                  </div>
                </div>
              </div>
            </div>

          </div>

          <div class="pt-1 flex items-center justify-between text-[11px] text-slate-500 dark:text-slate-400">
            <span>Supervised by: Dr. Alhadi Al Nazeer</span>
            <span class="font-bold text-indigo-600 dark:text-indigo-300">Blue Nile University</span>
          </div>
        </div>

        <!-- RIGHT COLUMN (5 Cols): Enterprise Sign In Card -->
        <div class="lg:col-span-5 order-1 lg:order-2 bg-white dark:bg-[#0E2447] p-5 sm:p-7 md:p-9 text-slate-900 dark:text-slate-100 flex flex-col justify-between space-y-6">
          <div class="space-y-4">
            
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-1.5 px-3 py-1 bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-100 dark:border-indigo-800 rounded-full text-indigo-700 dark:text-indigo-300 font-extrabold text-[10px] uppercase tracking-wider">
                <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                <span>SECURE ACCESS PORTAL</span>
              </div>
              <span class="text-xs text-slate-400 font-semibold">RBAC Protected</span>
            </div>

            <div>
              <h3 id="i18n-login-card-title" class="text-2xl font-black text-[#0B1E3B] dark:text-white tracking-tight">Welcome Back</h3>
              <p id="i18n-login-card-sub" class="text-xs text-slate-500 dark:text-slate-300 mt-1">Sign in with your authorized credentials to access the project intelligence workspace.</p>
            </div>

            <!-- Login Form -->
            <form onsubmit="handleLoginSubmit(event)" class="space-y-4 pt-1">
              <div>
                <label id="i18n-login-lbl-user" class="block text-[11px] font-black text-slate-700 dark:text-slate-300 uppercase mb-1">USERNAME / EMAIL</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                    <i data-lucide="user" class="w-4 h-4"></i>
                  </div>
                  <input type="text" id="login-username" value="" required class="w-full bg-slate-50 dark:bg-[#132F5C] border border-slate-200 dark:border-[#1E3A66] focus:border-indigo-600 focus:bg-white dark:focus:bg-[#16386D] text-slate-900 dark:text-white rounded-xl pl-9 pr-3 py-3 text-xs outline-none font-bold transition shadow-xs" placeholder="Username or email (e.g. asem.othman@company.com)" />
                </div>
              </div>

              <div>
                <label id="i18n-login-lbl-pass" class="block text-[11px] font-black text-slate-700 dark:text-slate-300 uppercase mb-1">PASSWORD</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                    <i data-lucide="lock" class="w-4 h-4"></i>
                  </div>
                  <input type="password" id="login-password" value="" required class="w-full bg-slate-50 dark:bg-[#132F5C] border border-slate-200 dark:border-[#1E3A66] focus:border-indigo-600 focus:bg-white dark:focus:bg-[#16386D] text-slate-900 dark:text-white rounded-xl pl-9 pr-9 py-3 text-xs outline-none font-bold transition shadow-xs" placeholder="••••••••" />
                  <button type="button" onclick="togglePasswordVisibility()" class="absolute right-3 top-3 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition">
                    <i data-lucide="eye" id="pass-eye-icon" class="w-4 h-4"></i>
                  </button>
                </div>
              </div>

              <div class="flex items-center justify-between text-xs text-slate-500 dark:text-slate-300">
                <label class="flex items-center gap-2 cursor-pointer select-none">
                  <input type="checkbox" checked class="rounded border-slate-300 text-indigo-600 focus:ring-0">
                  <span class="text-[11px]">Remember credentials</span>
                </label>
                <button type="button" onclick="openResetPasswordModal()" class="text-[11px] font-bold text-indigo-600 dark:text-indigo-400 hover:underline cursor-pointer flex items-center gap-1" id="i18n-login-forgot-pass">
                  <i data-lucide="key-round" class="w-3.5 h-3.5"></i>
                  <span>Forgot / Reset Password?</span>
                </button>
              </div>

              <!-- Main Sign In Button -->
              <button type="submit" id="btn-login-submit" class="w-full py-3.5 bg-[#0B1E3B] hover:bg-[#142A4E] text-white font-extrabold text-xs rounded-xl shadow-lg transition flex items-center justify-center gap-2 group border border-slate-700">
                <span id="i18n-login-btn-sign">Sign In to Workspace</span>
                <i data-lucide="arrow-right" class="w-4 h-4 group-hover:translate-x-0.5 transition-transform"></i>
              </button>
            </form>
          </div>

          <!-- Enterprise Platform Footer -->
          <div class="pt-3 border-t border-slate-100 dark:border-slate-800">
            <p class="text-[11px] text-slate-400 text-center font-medium">Smart Project Manager Assistant (SPMA) • Enterprise Edition © 2026</p>
          </div>

        </div>

      </div>
    </main>

    <!-- Bottom Footer of Login Page -->
    <footer class="w-full max-w-7xl mx-auto py-2 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 dark:text-slate-400 border-t border-slate-200 dark:border-slate-800/80 gap-2 transition-colors">
      <p>© 2026 Blue Nile University — Department of Civil & Project Engineering.</p>
      <div class="flex items-center gap-4 text-[11px]">
        <span>Privacy Policy</span>
        <span>•</span>
        <span>Graduation Defense Edition</span>
        <span>•</span>
        <span class="text-indigo-600 dark:text-indigo-400 font-bold">SPMA AI Engine 6.4</span>
      </div>
    </footer>

  </div>


  <!-- ========================================================================= -->
  <!-- 2. MAIN APPLICATION WORKSPACE VIEW (VISIBLE AFTER SUCCESSFUL LOGIN)       -->
  <!-- ========================================================================= -->
  <div id="app-view" class="h-screen w-screen hidden overflow-hidden select-none bg-[#F8FAFC] dark:bg-[#071326] text-slate-800 dark:text-slate-100">
    
    <!-- LEFT SIDEBAR (Always deep navy as per signature design) -->
    <aside id="main-sidebar" class="w-72 bg-[#0B1E3B] text-slate-200 flex flex-col p-3.5 z-30 shrink-0 border-r border-slate-800/80 shadow-xl h-full overflow-hidden">
      
      <!-- Top Brand Box (White rounded card with Blue Nile logo) -->
      <div class="bg-white dark:bg-[#0E2447] rounded-2xl p-2.5 flex items-center justify-between gap-2 shadow-md border border-slate-100 dark:border-slate-800 shrink-0 mb-3">
        <div class="flex items-center gap-2.5 min-w-0">
          <div class="w-11 h-11 rounded-xl bg-white p-0.5 flex items-center justify-center border border-slate-200 dark:border-slate-700 shrink-0 shadow-xs">
            <img src="/static/brand/blue_nile_logo.png" alt="Blue Nile Logo" class="w-full h-full object-contain rounded-lg" />
          </div>
          <div class="flex-1 min-w-0">
            <h1 id="sidebar-brand-title" class="font-black text-[12px] leading-snug text-[#0B1E3B] dark:text-white tracking-tight whitespace-normal">
              Smart Project Manager (SPMA)
            </h1>
            <p id="sidebar-brand-sub" class="text-[10px] font-bold text-indigo-600 dark:text-indigo-400 mt-0.5">
              Blue Nile University
            </p>
          </div>
        </div>
        <!-- Close button for mobile drawer -->
        <button onclick="closeMobileSidebar()" class="md:hidden p-1.5 text-slate-400 hover:text-slate-700 dark:hover:text-white rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition cursor-pointer" aria-label="Close drawer">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>

      <!-- Scrollable Sidebar Body (Rolling Nav + Project Team without gap) -->
      <div class="flex-1 overflow-y-auto custom-scrollbar-dark pr-1 space-y-4">
        
        <!-- Navigation Menu (9 Main Tabs) -->
        <nav class="space-y-1 text-xs font-semibold">
          <button onclick="switchTab('dashboard')" id="nav-dashboard" class="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl transition bg-slate-800/80 text-white font-bold border border-slate-700/60 shadow-sm cursor-pointer">
            <i data-lucide="layout-dashboard" class="w-4 h-4 text-indigo-400"></i>
            <span id="i18n-nav-dashboard">Dashboard</span>
          </button>

          <button onclick="switchTab('projects')" id="nav-projects" class="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl transition text-slate-300 hover:bg-slate-800/50 hover:text-white cursor-pointer">
            <i data-lucide="folder-kanban" class="w-4 h-4 text-slate-400"></i>
            <span id="i18n-nav-projects">Projects</span>
          </button>

          <button onclick="switchTab('activities')" id="nav-activities" class="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl transition text-slate-300 hover:bg-slate-800/50 hover:text-white cursor-pointer">
            <i data-lucide="check-square" class="w-4 h-4 text-slate-400"></i>
            <span id="i18n-nav-activities">Activities</span>
          </button>

          <button onclick="switchTab('ai-assistant')" id="nav-ai-assistant" class="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl transition text-slate-300 hover:bg-slate-800/50 hover:text-white cursor-pointer">
            <i data-lucide="sparkles" class="w-4 h-4 text-indigo-400"></i>
            <span id="i18n-nav-ai-assistant">AI Assistant</span>
          </button>

          <button onclick="switchTab('reports')" id="nav-reports" class="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl transition text-slate-300 hover:bg-slate-800/50 hover:text-white cursor-pointer">
            <i data-lucide="file-text" class="w-4 h-4 text-slate-400"></i>
            <span id="i18n-nav-reports">Reports</span>
          </button>

          <button onclick="switchTab('engineer-chat')" id="nav-engineer-chat" class="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl transition text-slate-300 hover:bg-slate-800/50 hover:text-white cursor-pointer relative">
            <i data-lucide="message-circle" class="w-4 h-4 text-slate-400"></i>
            <span id="i18n-nav-engineer-chat">Engineer Chat</span>
            <span id="chat-unread-badge" class="hidden ml-auto bg-rose-500 text-white text-[10px] font-black px-1.5 py-0.5 rounded-full shadow-xs animate-pulse">0</span>
          </button>

          <button onclick="switchTab('whatsapp-center')" id="nav-whatsapp-center" class="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl transition text-slate-300 hover:bg-slate-800/50 hover:text-white cursor-pointer">
            <i data-lucide="phone-call" class="w-4 h-4 text-emerald-400"></i>
            <span id="i18n-nav-whatsapp-center">WhatsApp Center</span>
          </button>

          <button onclick="switchTab('user-mgmt')" id="nav-user-mgmt" class="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl transition text-slate-300 hover:bg-slate-800/50 hover:text-white cursor-pointer">
            <i data-lucide="user-check" class="w-4 h-4 text-slate-400"></i>
            <span id="i18n-nav-user-mgmt">User Management</span>
          </button>

          <button onclick="switchTab('settings')" id="nav-settings" class="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl transition text-slate-300 hover:bg-slate-800/50 hover:text-white cursor-pointer">
            <i data-lucide="settings" class="w-4 h-4 text-slate-400"></i>
            <span id="i18n-nav-settings">Settings</span>
          </button>
        </nav>

        <!-- Project Team Section (Directly flows below navigation, no dead space, smooth rolling scroll) -->
        <div class="space-y-2 pt-3 border-t border-slate-800/80">
          <div class="flex items-center justify-between px-1">
            <span id="i18n-team-title" class="text-[10px] font-extrabold tracking-wider text-slate-400 uppercase">PROJECT TEAM</span>
            <span class="text-[10px] text-emerald-400 font-bold flex items-center gap-1">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              <span id="sidebar-online-count">5 Online</span>
            </span>
          </div>

          <div class="space-y-1.5" id="sidebar-team-container">
            <!-- Member 1: Mohammed Gassim -->
            <div class="bg-slate-900/90 border border-slate-800 p-2 rounded-xl space-y-1">
              <div class="flex items-center justify-between text-[11px]">
                <span class="font-bold text-white truncate">Engr. Mohammed Gassim</span>
              </div>
              <p class="text-[10px] text-slate-400">Site Operations & Execution</p>
              <div class="flex gap-1 pt-0.5">
                <a href="tel:+966563456789" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="phone" class="w-3 h-3"></i></a>
                <a href="mailto:gassim@spma.com" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="mail" class="w-3 h-3"></i></a>
                <button onclick="openWhatsAppFor('Engr. Mohammed Gassim', '966563456789')" class="flex-1 bg-emerald-950/60 hover:bg-emerald-900/80 text-emerald-300 p-1 rounded flex items-center justify-center text-[9px] font-bold">WA</button>
              </div>
            </div>

            <!-- Member 2: Asem Othman -->
            <div class="bg-slate-900/90 border border-slate-800 p-2 rounded-xl space-y-1">
              <div class="flex items-center justify-between text-[11px]">
                <span class="font-bold text-white truncate">Engr. Asem Othman</span>
              </div>
              <p class="text-[10px] text-slate-400">Team Leader & Full-Stack Architect</p>
              <div class="flex gap-1 pt-0.5">
                <a href="tel:+966505554101" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="phone" class="w-3 h-3"></i></a>
                <a href="mailto:asem.2007@hotmail.com" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="mail" class="w-3 h-3"></i></a>
                <button onclick="openWhatsAppFor('Engr. Asem Othman', '966505554101')" class="flex-1 bg-emerald-950/60 hover:bg-emerald-900/80 text-emerald-300 p-1 rounded flex items-center justify-center text-[9px] font-bold">WA</button>
              </div>
            </div>

            <!-- Member 3: Saleh Mohammed -->
            <div class="bg-slate-900/90 border border-slate-800 p-2 rounded-xl space-y-1">
              <div class="flex items-center justify-between text-[11px]">
                <span class="font-bold text-white truncate">Engr. Saleh Mohammed</span>
              </div>
              <p class="text-[10px] text-slate-400">Planning & EVM Engine</p>
              <div class="flex gap-1 pt-0.5">
                <a href="tel:+966552345678" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="phone" class="w-3 h-3"></i></a>
                <a href="mailto:saleh@spma.com" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="mail" class="w-3 h-3"></i></a>
                <button onclick="openWhatsAppFor('Engr. Saleh Mohammed', '966552345678')" class="flex-1 bg-emerald-950/60 hover:bg-emerald-900/80 text-emerald-300 p-1 rounded flex items-center justify-center text-[9px] font-bold">WA</button>
              </div>
            </div>

            <!-- Member 4: Rafat Mohammed -->
            <div class="bg-slate-900/90 border border-slate-800 p-2 rounded-xl space-y-1">
              <div class="flex items-center justify-between text-[11px]">
                <span class="font-bold text-white truncate">Engr. Rafat Mohammed</span>
              </div>
              <p class="text-[10px] text-slate-400">QA/QC & Site Vision</p>
              <div class="flex gap-1 pt-0.5">
                <a href="tel:+966574567890" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="phone" class="w-3 h-3"></i></a>
                <a href="mailto:rafat@spma.com" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="mail" class="w-3 h-3"></i></a>
                <button onclick="openWhatsAppFor('Engr. Rafat Mohammed', '966574567890')" class="flex-1 bg-emerald-950/60 hover:bg-emerald-900/80 text-emerald-300 p-1 rounded flex items-center justify-center text-[9px] font-bold">WA</button>
              </div>
            </div>

            <!-- Member 5: Abu baker Mohammed -->
            <div class="bg-slate-900/90 border border-slate-800 p-2 rounded-xl space-y-1">
              <div class="flex items-center justify-between text-[11px]">
                <span class="font-bold text-white truncate">Engr. Abu baker Mohammed</span>
              </div>
              <p class="text-[10px] text-slate-400">Cost Engineering & FIDIC Contracts</p>
              <div class="flex gap-1 pt-0.5">
                <a href="tel:+966585678901" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="phone" class="w-3 h-3"></i></a>
                <a href="mailto:abubaker@spma.com" class="flex-1 bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 p-1 rounded flex items-center justify-center text-[10px]"><i data-lucide="mail" class="w-3 h-3"></i></a>
                <button onclick="openWhatsAppFor('Engr. Abu baker Mohammed', '966585678901')" class="flex-1 bg-emerald-950/60 hover:bg-emerald-900/80 text-emerald-300 p-1 rounded flex items-center justify-center text-[9px] font-bold">WA</button>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Pinned Current User Box & Logout -->
      <div class="shrink-0 pt-2.5 mt-1 border-t border-slate-800/80">
        <div class="bg-slate-900 p-2.5 rounded-2xl border border-slate-800 flex items-center justify-between shadow-inner">
          <div class="flex items-center gap-2.5 overflow-hidden">
            <div id="sidebar-user-avatar" class="w-8 h-8 rounded-xl bg-indigo-600 text-white font-black text-xs flex items-center justify-center shrink-0 shadow">AO</div>
            <div class="overflow-hidden">
              <p id="sidebar-user-name" class="text-xs font-bold text-white truncate">Asem Othman</p>
              <p id="sidebar-user-role" class="text-[10px] text-emerald-400 font-bold">ADMIN</p>
            </div>
          </div>
          <button onclick="handleLogout()" id="btn-logout" class="px-2.5 py-1 bg-slate-800 hover:bg-rose-950/80 hover:text-rose-300 text-slate-300 text-[10px] font-bold rounded-lg border border-slate-700 transition cursor-pointer">
            Logout
          </button>
        </div>
      </div>

    </aside>

    <!-- Mobile Sidebar Dark Backdrop Overlay -->
    <div id="sidebar-backdrop" onclick="closeMobileSidebar()" class="fixed inset-0 bg-black/60 backdrop-blur-xs z-40 hidden md:hidden transition-opacity"></div>

    <!-- MAIN RIGHT CONTENT CONTAINER -->
    <main class="flex-1 flex flex-col min-w-0 bg-[#F8FAFC] dark:bg-[#071326] overflow-hidden">
      
      <!-- Top Header Bar -->
      <header class="h-16 bg-white/90 dark:bg-[#0B1E3B]/90 backdrop-blur-md border-b border-slate-200/80 dark:border-slate-800/80 px-3 sm:px-6 flex items-center justify-between shrink-0 z-20 transition-colors shadow-xs">
        <div class="flex items-center gap-2 sm:gap-4">
          <!-- Mobile Hamburger Toggle -->
          <button onclick="toggleMobileSidebar()" class="md:hidden p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition cursor-pointer" aria-label="Toggle Navigation Menu">
            <i data-lucide="menu" class="w-5 h-5"></i>
          </button>

          <h2 id="top-title" class="text-sm sm:text-base font-extrabold text-slate-800 dark:text-white tracking-tight truncate max-w-[110px] sm:max-w-none">Dashboard</h2>
          
          <!-- Search Bar / Command Palette -->
          <div class="relative hidden lg:block">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
              <i data-lucide="search" class="w-4 h-4"></i>
            </div>
            <input type="text" id="global-search-input" onkeyup="handleGlobalSearch(event)" placeholder="Search projects or type a command..." class="w-52 xl:w-64 bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700/80 text-slate-800 dark:text-slate-100 rounded-xl pl-9 pr-3 py-2 text-xs outline-none focus:border-indigo-500 transition-all font-medium shadow-2xs" />
          </div>

          <!-- Active Project Selector Dropdown -->
          <div class="flex items-center gap-1 sm:gap-2 bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700/80 rounded-xl px-2 sm:px-3 py-1.5 shadow-2xs max-w-[130px] sm:max-w-none">
            <i data-lucide="briefcase" class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-indigo-600 dark:text-indigo-400 shrink-0"></i>
            <select id="global-project-select" onchange="switchActiveProject(this.value)" class="bg-transparent text-[11px] sm:text-xs font-bold text-slate-700 dark:text-slate-200 outline-none cursor-pointer truncate w-full">
              <option value="kkia">King Khalid International Airport – Terminal 5</option>
              <option value="hospital">Blue Nile Specialized Medical City</option>
              <option value="bridges">Northern Sector Bridges & Infrastructure</option>
            </select>
          </div>
        </div>

        <!-- Top Right Actions -->
        <div class="flex items-center gap-1 sm:gap-2 relative">
          <!-- Refresh Button with Spin Effect -->
          <button onclick="refreshCurrentPage()" title="Refresh Data" class="p-1.5 sm:p-2 text-slate-500 dark:text-slate-300 hover:text-slate-800 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl transition cursor-pointer">
            <i data-lucide="rotate-cw" id="refresh-icon" class="w-4 h-4"></i>
          </button>

          <!-- Theme Toggle (Dark / Light Mode) -->
          <button onclick="toggleTheme()" id="theme-toggle-btn" title="Toggle Theme (Dark / Light)" class="p-1.5 sm:p-2 text-slate-500 dark:text-slate-300 hover:text-slate-800 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl transition cursor-pointer">
            <i data-lucide="sun" id="theme-icon" class="w-4 h-4 text-amber-400"></i>
          </button>

          <!-- Notifications Diamond Badge Popover -->
          <div class="relative">
            <button onclick="toggleNotificationsPopover()" id="notif-btn" class="px-2 sm:px-3 py-1.5 bg-slate-100 dark:bg-[#0E2447] hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 flex items-center gap-1 sm:gap-1.5 transition cursor-pointer">
              <span class="text-rose-500 font-black">♦</span>
              <span id="notif-badge-count" class="font-bold">2</span>
            </button>

            <!-- Floating Notifications Dropdown Popover -->
            <div id="notifications-popover" class="hidden absolute right-0 mt-2 w-72 sm:w-80 bg-white dark:bg-[#0B1E3B] rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-700 p-4 z-50 space-y-3">
              <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-2">
                <span class="text-xs font-bold text-slate-900 dark:text-white flex items-center gap-1.5">
                  <i data-lucide="bell" class="w-4 h-4 text-indigo-500"></i>
                  <span>Project Notifications</span>
                </span>
                <button onclick="markAlertsRead()" class="text-[10px] font-bold text-indigo-600 dark:text-indigo-400 hover:underline">Mark all read</button>
              </div>

              <div class="space-y-2 text-xs" id="notif-list-container">
                <div class="p-2.5 bg-rose-50 dark:bg-rose-950/40 border border-rose-100 dark:border-rose-900/50 rounded-xl space-y-0.5">
                  <div class="flex items-center justify-between text-rose-800 dark:text-rose-300 font-bold text-[11px]">
                    <span>High Risk Warning</span>
                    <span class="text-[9px] text-slate-400">Just now</span>
                  </div>
                  <p class="text-[10px] text-rose-600 dark:text-rose-400">KKIA Terminal 5 critical path requires mitigation plan.</p>
                </div>

                <div class="p-2.5 bg-amber-50 dark:bg-amber-950/40 border border-amber-100 dark:border-amber-900/50 rounded-xl space-y-0.5">
                  <div class="flex items-center justify-between text-amber-800 dark:text-amber-300 font-bold text-[11px]">
                    <span>Delayed Activity Alert</span>
                    <span class="text-[9px] text-slate-400">Today</span>
                  </div>
                  <p class="text-[10px] text-amber-700 dark:text-amber-400">concrete activity has 14-day schedule variance.</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Language Switcher Pill (EN / ع) -->
          <button onclick="toggleLanguage()" id="lang-toggle-btn" class="px-2.5 sm:px-3.5 py-1.5 bg-slate-100 dark:bg-[#0E2447] hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 flex items-center gap-1 sm:gap-1.5 transition cursor-pointer">
            <i data-lucide="globe" class="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400"></i>
            <span id="lang-label">عربي</span>
          </button>

          <!-- Primary + Project Action Button -->
          <button onclick="openAddProjectModal()" class="px-2.5 sm:px-4 py-2 bg-[#0B1E3B] dark:bg-indigo-600 hover:bg-[#142A4E] dark:hover:bg-indigo-700 text-white text-xs font-extrabold rounded-xl shadow transition flex items-center gap-1.5 cursor-pointer">
            <i data-lucide="plus" class="w-4 h-4"></i>
            <span id="i18n-btn-top-project" class="hidden sm:inline">Project</span>
          </button>
        </div>
      </header>

      <!-- Scrollable Tab Content Area -->
      <div class="flex-1 overflow-y-auto custom-scrollbar p-3.5 sm:p-5 md:p-6 pb-24 md:pb-6 space-y-4 sm:space-y-6">
        
        <!-- ========================================================================= -->
        <!-- TAB 1: DASHBOARD                                                          -->
        <!-- ========================================================================= -->
        <section id="tab-dashboard" class="space-y-6">
          
          <!-- Hero Navy Banner -->
          <div class="bg-gradient-to-r from-[#0B1E3B] via-[#0E2447] to-[#132F5C] rounded-3xl p-6 text-white flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl border border-slate-700/60">
            <div class="space-y-1.5">
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 bg-indigo-500/20 border border-indigo-400/40 text-indigo-300 rounded-full text-[10px] font-black uppercase tracking-wider">Enterprise Intelligence</span>
                <span class="text-[11px] text-emerald-400 font-bold">● Active Tracking</span>
              </div>
              <h1 id="i18n-dash-hero-title" class="text-xl md:text-2xl font-black tracking-tight">Project Intelligence Workspace</h1>
              <p id="i18n-dash-hero-sub" class="text-xs text-slate-300 max-w-xl">Live progress, cost, risk, deadlines and communication in one place.</p>
            </div>
            <div class="flex flex-wrap gap-2.5">
              <button onclick="openAddProjectModal()" class="px-4 py-2.5 bg-slate-800/90 hover:bg-slate-700 text-white rounded-xl text-xs font-bold border border-slate-700 transition flex items-center gap-2 shadow-sm">
                <i data-lucide="folder-plus" class="w-4 h-4"></i>
                <span id="i18n-btn-new-proj">New Project</span>
              </button>
              <button onclick="switchTab('whatsapp-center')" class="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold shadow transition flex items-center gap-2">
                <i data-lucide="send" class="w-4 h-4"></i>
                <span id="i18n-btn-send-update">Send Project Update</span>
              </button>
            </div>
          </div>

          <!-- 6 Top Summary KPI Cards (Centered and Harmonious) -->
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <!-- Total Projects -->
            <div class="bg-white dark:bg-[#0B1E3B] p-4 sm:p-5 rounded-2xl border border-slate-100 dark:border-slate-800 shadow-sm flex flex-col items-center justify-center text-center space-y-2 hover:shadow-md transition">
              <div class="flex items-center justify-center gap-2">
                <div class="w-7 h-7 rounded-xl bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 flex items-center justify-center shrink-0">
                  <i data-lucide="folder" class="w-3.5 h-3.5"></i>
                </div>
                <span id="i18n-metric-total-proj" class="text-xs sm:text-[13px] font-extrabold text-slate-500 dark:text-slate-300">Total Projects</span>
              </div>
              <p class="text-3xl sm:text-4xl font-black text-[#0B1E3B] dark:text-white tabular-nums tracking-tight leading-none text-center" id="kpi-total-projects">3</p>
              <span class="text-xs text-slate-500 dark:text-slate-400 block font-bold text-center">1 portfolio wide</span>
            </div>

            <!-- Active Projects -->
            <div class="bg-white dark:bg-[#0B1E3B] p-4 sm:p-5 rounded-2xl border border-slate-100 dark:border-slate-800 shadow-sm flex flex-col items-center justify-center text-center space-y-2 hover:shadow-md transition">
              <div class="flex items-center justify-center gap-2">
                <div class="w-7 h-7 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 flex items-center justify-center shrink-0">
                  <i data-lucide="activity" class="w-3.5 h-3.5"></i>
                </div>
                <span id="i18n-metric-active-proj" class="text-xs sm:text-[13px] font-extrabold text-slate-500 dark:text-slate-300">Active Projects</span>
              </div>
              <p class="text-3xl sm:text-4xl font-black text-[#0B1E3B] dark:text-white tabular-nums tracking-tight leading-none text-center" id="kpi-active-projects">3</p>
              <span class="text-xs text-emerald-600 dark:text-emerald-400 font-bold block text-center">100% active rate</span>
            </div>

            <!-- Completed Projects -->
            <div class="bg-white dark:bg-[#0B1E3B] p-4 sm:p-5 rounded-2xl border border-slate-100 dark:border-slate-800 shadow-sm flex flex-col items-center justify-center text-center space-y-2 hover:shadow-md transition">
              <div class="flex items-center justify-center gap-2">
                <div class="w-7 h-7 rounded-xl bg-teal-50 dark:bg-teal-950/60 text-teal-600 dark:text-teal-400 flex items-center justify-center shrink-0">
                  <i data-lucide="check-circle-2" class="w-3.5 h-3.5"></i>
                </div>
                <span id="i18n-metric-comp-proj" class="text-xs sm:text-[13px] font-extrabold text-slate-500 dark:text-slate-300">Completed Projects</span>
              </div>
              <p class="text-3xl sm:text-4xl font-black text-[#0B1E3B] dark:text-white tabular-nums tracking-tight leading-none text-center" id="kpi-completed-projects">0</p>
              <span class="text-xs text-slate-500 dark:text-slate-400 block font-bold text-center">0 archived</span>
            </div>

            <!-- Delayed Activities -->
            <div class="bg-white dark:bg-[#0B1E3B] p-4 sm:p-5 rounded-2xl border border-slate-100 dark:border-slate-800 shadow-sm flex flex-col items-center justify-center text-center space-y-2 hover:shadow-md transition">
              <div class="flex items-center justify-center gap-2">
                <div class="w-7 h-7 rounded-xl bg-rose-50 dark:bg-rose-950/60 text-rose-600 dark:text-rose-400 flex items-center justify-center shrink-0">
                  <i data-lucide="alert-triangle" class="w-3.5 h-3.5"></i>
                </div>
                <span id="i18n-metric-delayed-act" class="text-xs sm:text-[13px] font-extrabold text-slate-500 dark:text-slate-300">Delayed Activities</span>
              </div>
              <p class="text-3xl sm:text-4xl font-black text-rose-600 tabular-nums tracking-tight leading-none text-center" id="kpi-delayed-activities">1</p>
              <span class="text-xs text-rose-500 font-bold block text-center">Requires attention</span>
            </div>

            <!-- Budget Used -->
            <div class="bg-white dark:bg-[#0B1E3B] p-4 sm:p-5 rounded-2xl border border-slate-100 dark:border-slate-800 shadow-sm flex flex-col items-center justify-center text-center space-y-2 hover:shadow-md transition">
              <div class="flex items-center justify-center gap-2">
                <div class="w-7 h-7 rounded-xl bg-amber-50 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400 flex items-center justify-center shrink-0">
                  <i data-lucide="dollar-sign" class="w-3.5 h-3.5"></i>
                </div>
                <span id="i18n-metric-budget-used" class="text-xs sm:text-[13px] font-extrabold text-slate-500 dark:text-slate-300">Budget Used</span>
              </div>
              <p class="text-3xl sm:text-4xl font-black text-[#0B1E3B] dark:text-white tabular-nums tracking-tight leading-none text-center" id="kpi-budget-used">0.11%</p>
              <span class="text-xs text-slate-500 dark:text-slate-400 block font-bold text-center">SAR 1,000 spent</span>
            </div>

            <!-- Average Progress -->
            <div class="bg-white dark:bg-[#0B1E3B] p-4 sm:p-5 rounded-2xl border border-slate-100 dark:border-slate-800 shadow-sm flex flex-col items-center justify-center text-center space-y-2 hover:shadow-md transition">
              <div class="flex items-center justify-center gap-2">
                <div class="w-7 h-7 rounded-xl bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 flex items-center justify-center shrink-0">
                  <i data-lucide="pie-chart" class="w-3.5 h-3.5"></i>
                </div>
                <span id="i18n-metric-avg-prog" class="text-xs sm:text-[13px] font-extrabold text-slate-500 dark:text-slate-300">Average Progress</span>
              </div>
              <p class="text-3xl sm:text-4xl font-black text-emerald-600 dark:text-emerald-400 tabular-nums tracking-tight leading-none text-center" id="kpi-avg-progress">100%</p>
              <span class="text-xs text-slate-500 dark:text-slate-400 block font-bold text-center">Weighted avg</span>
            </div>
          </div>

          <!-- 3 Lower Widgets: Executive Alerts, Engineer Workload, 30-Day Timeline -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            <!-- Executive Alerts -->
            <div class="bg-white dark:bg-[#0B1E3B] p-5 rounded-2xl border border-slate-100 dark:border-slate-800 shadow-sm space-y-3 flex flex-col justify-between">
              <div class="space-y-3">
                <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-2.5">
                  <span id="i18n-card-alerts-title" class="text-xs font-extrabold text-[#0B1E3B] dark:text-white flex items-center gap-2">
                    <i data-lucide="shield-alert" class="w-4 h-4 text-rose-500"></i>
                    <span>Executive Alerts</span>
                  </span>
                  <button onclick="markAlertsRead()" class="text-[11px] text-indigo-600 dark:text-indigo-400 font-bold hover:underline" id="i18n-btn-mark-read">Mark Read</button>
                </div>
                <div class="space-y-2.5" id="dash-alerts-container">
                  <div class="p-3 bg-rose-50 dark:bg-rose-950/40 border border-rose-100 dark:border-rose-900/40 rounded-xl space-y-1">
                    <div class="flex items-center justify-between text-rose-800 dark:text-rose-300 text-xs font-bold">
                      <span>High risk project</span>
                      <span class="text-[10px] text-rose-400 font-semibold">Just now</span>
                    </div>
                    <p class="text-[11px] text-rose-600 dark:text-rose-400 leading-relaxed">King Khalid International Airport Branch – Terminal 5 has high risk.</p>
                  </div>

                  <div class="p-3 bg-amber-50 dark:bg-amber-950/40 border border-amber-100 dark:border-amber-900/40 rounded-xl space-y-1">
                    <div class="flex items-center justify-between text-amber-800 dark:text-amber-300 text-xs font-bold">
                      <span>Delayed activity</span>
                      <span class="text-[10px] text-amber-400 font-semibold">Today</span>
                    </div>
                    <p class="text-[11px] text-amber-700 dark:text-amber-400 leading-relaxed">concrete in King Khalid International Airport Branch – Terminal 5 is delayed.</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Engineer Workload -->
            <div class="bg-white dark:bg-[#0B1E3B] p-5 rounded-2xl border border-slate-100 dark:border-slate-800 shadow-sm space-y-3">
              <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-2.5">
                <span id="i18n-card-workload-title" class="text-xs font-extrabold text-[#0B1E3B] dark:text-white flex items-center gap-2">
                  <i data-lucide="users-round" class="w-4 h-4 text-indigo-500"></i>
                  <span>Engineer Workload</span>
                </span>
                <span class="text-[10px] font-bold text-slate-400 bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded-md" id="dash-workload-badge">5 Members</span>
              </div>
              <div class="space-y-3" id="dash-workload-container">
                <div>
                  <div class="flex justify-between text-[11px] font-bold text-slate-700 dark:text-slate-300 mb-1">
                    <span>Engr. Asem Othman</span>
                    <span class="text-indigo-600 dark:text-indigo-400">3 Activities</span>
                  </div>
                  <div class="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div class="bg-indigo-600 h-full rounded-full" style="width: 75%"></div>
                  </div>
                </div>

                <div>
                  <div class="flex justify-between text-[11px] font-bold text-slate-700 dark:text-slate-300 mb-1">
                    <span>Engr. Saleh Mohammed</span>
                    <span class="text-indigo-600 dark:text-indigo-400">2 Activities</span>
                  </div>
                  <div class="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div class="bg-indigo-600 h-full rounded-full" style="width: 50%"></div>
                  </div>
                </div>

                <div>
                  <div class="flex justify-between text-[11px] font-bold text-slate-700 dark:text-slate-300 mb-1">
                    <span>Engr. Mohammed Gassim</span>
                    <span class="text-emerald-600 dark:text-emerald-400">4 Activities</span>
                  </div>
                  <div class="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div class="bg-emerald-600 h-full rounded-full" style="width: 90%"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 30-Day Timeline -->
            <div class="bg-white dark:bg-[#0B1E3B] p-5 rounded-2xl border border-slate-100 dark:border-slate-800 shadow-sm space-y-3">
              <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-2.5">
                <span id="i18n-card-timeline-title" class="text-xs font-extrabold text-[#0B1E3B] dark:text-white flex items-center gap-2">
                  <i data-lucide="calendar" class="w-4 h-4 text-emerald-500"></i>
                  <span>30-Day Timeline</span>
                </span>
                <span class="text-[10px] font-bold text-indigo-600 dark:text-indigo-400" id="dash-timeline-badge">Next Milestones</span>
              </div>
              <div class="space-y-2.5 text-xs" id="dash-timeline-container">
                <div class="p-2.5 bg-slate-50 dark:bg-[#0E2447] rounded-xl border border-slate-100 dark:border-slate-800 flex items-center justify-between">
                  <div>
                    <p class="font-bold text-slate-800 dark:text-slate-200">Terminal 5 Apron Concrete</p>
                    <p class="text-[10px] text-slate-400">King Khalid Airport</p>
                  </div>
                  <span class="px-2.5 py-1 bg-rose-100 dark:bg-rose-950 text-rose-700 dark:text-rose-300 rounded-lg text-[10px] font-extrabold">12 Oct</span>
                </div>

                <div class="p-2.5 bg-slate-50 dark:bg-[#0E2447] rounded-xl border border-slate-100 dark:border-slate-800 flex items-center justify-between">
                  <div>
                    <p class="font-bold text-slate-800 dark:text-slate-200">Foundation Raft Inspection</p>
                    <p class="text-[10px] text-slate-400">Blue Nile Hospital</p>
                  </div>
                  <span class="px-2.5 py-1 bg-indigo-100 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 rounded-lg text-[10px] font-extrabold">20 Oct</span>
                </div>
              </div>
            </div>

          </div>

          <!-- Bottom Visuals: Portfolio Performance Bar & Project Health Ring -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="md:col-span-2 bg-white dark:bg-[#0B1E3B] p-5 rounded-2xl border border-slate-100 dark:border-slate-800 shadow-sm space-y-3">
              <span id="i18n-portfolio-perf-title" class="text-xs font-extrabold text-[#0B1E3B] dark:text-white flex items-center gap-2">
                <i data-lucide="bar-chart-3" class="w-4 h-4 text-indigo-500"></i>
                <span>Portfolio Performance</span>
              </span>
              <div class="space-y-2 pt-1" id="dash-portfolio-container">
                <div class="flex justify-between text-xs font-bold text-slate-700 dark:text-slate-300">
                  <span>King Khalid International Airport Branch – Terminal 5</span>
                  <span class="text-emerald-600 dark:text-emerald-400">100%</span>
                </div>
                <div class="w-full bg-slate-100 dark:bg-slate-800 h-3 rounded-full overflow-hidden">
                  <div class="bg-rose-500 h-full rounded-full" style="width: 100%"></div>
                </div>
              </div>
            </div>

            <div class="bg-white dark:bg-[#0B1E3B] p-5 rounded-2xl border border-slate-100 dark:border-slate-800 shadow-sm flex items-center justify-between" id="dash-health-container">
              <div class="space-y-1.5">
                <span id="i18n-proj-health-title" class="text-xs font-extrabold text-[#0B1E3B] dark:text-white flex items-center gap-2">
                  <i data-lucide="heart-pulse" class="w-4 h-4 text-rose-500"></i>
                  <span>Project Health</span>
                </span>
                <p class="text-xs text-slate-400">EVM & Schedule Index</p>
                <div class="flex items-center gap-3 pt-2 text-[10px] font-bold">
                  <span class="text-emerald-600 dark:text-emerald-400">● Healthy: 0</span>
                  <span class="text-amber-500">● Warning: 0</span>
                  <span class="text-rose-500">● Critical: 1</span>
                </div>
              </div>
              <div class="relative w-20 h-20 flex items-center justify-center">
                <svg class="w-full h-full transform -rotate-90">
                  <circle cx="40" cy="40" r="32" stroke="currentColor" class="text-slate-100 dark:text-slate-800" stroke-width="8" fill="transparent" />
                  <circle cx="40" cy="40" r="32" stroke="#F43F5E" stroke-width="8" stroke-dasharray="200" stroke-dashoffset="30" fill="transparent" stroke-linecap="round" />
                </svg>
                <span class="absolute font-black text-xs text-[#0B1E3B] dark:text-white">85%</span>
              </div>
            </div>
          </div>

        </section>

        <!-- ========================================================================= -->
        <!-- TAB 2: PROJECTS                                                           -->
        <!-- ========================================================================= -->
        <section id="tab-projects" class="hidden space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 id="i18n-projects-title" class="text-lg font-black text-[#0B1E3B] dark:text-white">Projects</h2>
              <p id="i18n-projects-desc" class="text-xs text-slate-500 dark:text-slate-400">Create and monitor all projects in the portfolio.</p>
            </div>
            <button onclick="openAddProjectModal()" class="px-4 py-2.5 bg-[#0B1E3B] dark:bg-indigo-600 hover:bg-[#142A4E] dark:hover:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow transition flex items-center gap-2">
              <i data-lucide="plus" class="w-4 h-4"></i>
              <span id="i18n-btn-new-proj-tab">New Project</span>
            </button>
          </div>

          <!-- Project Cards Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5" id="projects-container">
            <!-- Project 1 -->
            <div class="bg-white dark:bg-[#0B1E3B] rounded-2xl border border-slate-100 dark:border-slate-800 p-5 shadow-sm space-y-3">
              <div class="flex items-center justify-between">
                <span class="px-2.5 py-1 bg-rose-50 dark:bg-rose-950/60 text-rose-700 dark:text-rose-300 rounded-lg text-[10px] font-bold">High Risk</span>
                <span class="text-xs font-bold text-slate-400 font-mono">KKIA-T5</span>
              </div>
              <div>
                <h3 class="font-bold text-sm text-[#0B1E3B] dark:text-white">King Khalid International Airport Branch – Terminal 5</h3>
                <p class="text-xs text-slate-400 mt-0.5">Active • SAR 931,512.29 Budget</p>
              </div>
              <div class="space-y-1">
                <div class="flex justify-between text-xs font-bold">
                  <span class="text-slate-500 dark:text-slate-400">Progress</span>
                  <span class="text-emerald-600 dark:text-emerald-400">100%</span>
                </div>
                <div class="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div class="bg-emerald-500 h-full rounded-full" style="width: 100%"></div>
                </div>
              </div>
              <div class="pt-2 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs">
                <span class="text-slate-500 dark:text-slate-400">1 Activity</span>
                <button onclick="openWorkspaceModal('kkia')" class="text-indigo-600 dark:text-indigo-400 font-bold hover:underline flex items-center gap-1">
                  <span>Workspace</span>
                  <i data-lucide="arrow-up-right" class="w-3.5 h-3.5"></i>
                </button>
              </div>
            </div>

            <!-- Project 2 -->
            <div class="bg-white dark:bg-[#0B1E3B] rounded-2xl border border-slate-100 dark:border-slate-800 p-5 shadow-sm space-y-3">
              <div class="flex items-center justify-between">
                <span class="px-2.5 py-1 bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 rounded-lg text-[10px] font-bold">On Schedule</span>
                <span class="text-xs font-bold text-slate-400 font-mono">BN-HOSP</span>
              </div>
              <div>
                <h3 class="font-bold text-sm text-[#0B1E3B] dark:text-white">Blue Nile Specialized Medical City</h3>
                <p class="text-xs text-slate-400 mt-0.5">Active • SAR 4,500,000.00 Budget</p>
              </div>
              <div class="space-y-1">
                <div class="flex justify-between text-xs font-bold">
                  <span class="text-slate-500 dark:text-slate-400">Progress</span>
                  <span class="text-indigo-600 dark:text-indigo-400">42%</span>
                </div>
                <div class="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div class="bg-indigo-600 h-full rounded-full" style="width: 42%"></div>
                </div>
              </div>
              <div class="pt-2 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs">
                <span class="text-slate-500 dark:text-slate-400">18 Activities</span>
                <button onclick="openWorkspaceModal('hospital')" class="text-indigo-600 dark:text-indigo-400 font-bold hover:underline flex items-center gap-1">
                  <span>Workspace</span>
                  <i data-lucide="arrow-up-right" class="w-3.5 h-3.5"></i>
                </button>
              </div>
            </div>

            <!-- Project 3 -->
            <div class="bg-white dark:bg-[#0B1E3B] rounded-2xl border border-slate-100 dark:border-slate-800 p-5 shadow-sm space-y-3">
              <div class="flex items-center justify-between">
                <span class="px-2.5 py-1 bg-indigo-50 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 rounded-lg text-[10px] font-bold">Planning Phase</span>
                <span class="text-xs font-bold text-slate-400 font-mono">BN-BRIDGES</span>
              </div>
              <div>
                <h3 class="font-bold text-sm text-[#0B1E3B] dark:text-white">Northern Sector Bridges & Infrastructure</h3>
                <p class="text-xs text-slate-400 mt-0.5">Active • SAR 12,200,000.00 Budget</p>
              </div>
              <div class="space-y-1">
                <div class="flex justify-between text-xs font-bold">
                  <span class="text-slate-500 dark:text-slate-400">Progress</span>
                  <span class="text-indigo-600 dark:text-indigo-400">15%</span>
                </div>
                <div class="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div class="bg-indigo-500 h-full rounded-full" style="width: 15%"></div>
                </div>
              </div>
              <div class="pt-2 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs">
                <span class="text-slate-500 dark:text-slate-400">6 Activities</span>
                <button onclick="openWorkspaceModal('bridges')" class="text-indigo-600 dark:text-indigo-400 font-bold hover:underline flex items-center gap-1">
                  <span>Workspace</span>
                  <i data-lucide="arrow-up-right" class="w-3.5 h-3.5"></i>
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- ========================================================================= -->
        <!-- TAB 3: ACTIVITIES                                                         -->
        <!-- ========================================================================= -->
        <section id="tab-activities" class="hidden space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 id="i18n-activities-title" class="text-lg font-black text-[#0B1E3B] dark:text-white">Activities</h2>
              <p id="i18n-activities-desc" class="text-xs text-slate-500 dark:text-slate-400">Track planned and actual progress and upcoming deadlines.</p>
            </div>
            <button onclick="openAddActivityModal()" class="px-4 py-2.5 bg-[#0B1E3B] dark:bg-indigo-600 hover:bg-[#142A4E] dark:hover:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow transition flex items-center gap-2">
              <i data-lucide="plus" class="w-4 h-4"></i>
              <span id="i18n-btn-new-activity-tab">New Activity</span>
            </button>
          </div>

          <!-- Activities Table Container -->
          <div class="bg-white dark:bg-[#0B1E3B] rounded-2xl border border-slate-100 dark:border-slate-800 shadow-sm overflow-hidden">
            <div class="p-3.5 bg-slate-50 dark:bg-[#0E2447] border-b border-slate-100 dark:border-slate-800 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
              <div class="flex flex-wrap gap-1 text-xs" id="act-filter-tabs">
                <button id="act-tab-all" onclick="filterActivitiesByStatus('all')" class="px-3.5 py-1.5 bg-white dark:bg-[#0B1E3B] border border-slate-200 dark:border-slate-700 rounded-xl font-bold text-[#0B1E3B] dark:text-white shadow-2xs">All (0)</button>
                <button id="act-tab-delayed" onclick="filterActivitiesByStatus('delayed')" class="px-3.5 py-1.5 text-slate-500 dark:text-slate-400 hover:text-slate-800 font-semibold rounded-xl">Delayed (0)</button>
                <button id="act-tab-in_progress" onclick="filterActivitiesByStatus('in_progress')" class="px-3.5 py-1.5 text-slate-500 dark:text-slate-400 hover:text-slate-800 font-semibold rounded-xl">In Progress (0)</button>
                <button id="act-tab-completed" onclick="filterActivitiesByStatus('completed')" class="px-3.5 py-1.5 text-slate-500 dark:text-slate-400 hover:text-slate-800 font-semibold rounded-xl">Completed (0)</button>
              </div>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-2.5 flex items-center pointer-events-none text-slate-400">
                  <i data-lucide="search" class="w-3.5 h-3.5"></i>
                </div>
                <input type="text" id="act-search-input" onkeyup="filterActivitiesTable()" placeholder="Search activities..." class="bg-white dark:bg-[#0B1E3B] border border-slate-200 dark:border-slate-700 rounded-xl pl-8 pr-3 py-1.5 text-xs outline-none w-full sm:w-56 text-slate-800 dark:text-slate-100 font-medium" />
              </div>
            </div>

            <div class="overflow-x-auto">
              <table class="w-full text-xs text-left border-collapse" id="activities-table">
                <thead class="bg-slate-50 dark:bg-[#0E2447] text-slate-400 font-bold border-b border-slate-100 dark:border-slate-800">
                  <tr>
                    <th class="p-3.5">Activity Name</th>
                    <th class="p-3.5">Project</th>
                    <th class="p-3.5">Owner</th>
                    <th class="p-3.5">Status</th>
                    <th class="p-3.5">Planned End</th>
                    <th class="p-3.5">Actual %</th>
                    <th class="p-3.5">Spent (SAR)</th>
                    <th class="p-3.5 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100 dark:divide-slate-800 text-slate-700 dark:text-slate-200 font-medium" id="activities-tbody">
                  <tr class="hover:bg-slate-50 dark:hover:bg-[#0E2447]">
                    <td class="p-3.5 font-bold text-slate-900 dark:text-white">concrete</td>
                    <td class="p-3.5 text-slate-500 dark:text-slate-400">King Khalid Airport – Terminal 5</td>
                    <td class="p-3.5 text-slate-500 dark:text-slate-400">Engr. Asem Othman</td>
                    <td class="p-3.5"><span class="px-2 py-0.5 bg-rose-100 dark:bg-rose-950 text-rose-700 dark:text-rose-300 rounded text-[10px] font-bold">Delayed</span></td>
                    <td class="p-3.5 text-slate-500 dark:text-slate-400">2026-03-31</td>
                    <td class="p-3.5 font-bold text-emerald-600 dark:text-emerald-400">100%</td>
                    <td class="p-3.5 tabular-nums">1,000.00</td>
                    <td class="p-3.5 text-right">
                      <div class="flex items-center justify-end gap-2">
                        <button onclick="openEditActivityModal('concrete', 'King Khalid Airport – Terminal 5', '2026-03-31', 100, 1000, 'delayed')" class="px-2.5 py-1 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 rounded-lg font-bold text-indigo-700 dark:text-indigo-300">Edit</button>
                        <button onclick="deleteActivityRow(this)" class="px-2.5 py-1 bg-rose-50 dark:bg-rose-950 hover:bg-rose-100 text-rose-600 rounded-lg font-bold">Delete</button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- ========================================================================= -->
        <!-- TAB 4: AI ASSISTANT                                                       -->
        <!-- ========================================================================= -->
        <section id="tab-ai-assistant" class="hidden space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 id="i18n-ai-title" class="text-lg font-black text-[#0B1E3B] dark:text-white">AI Assistant</h2>
              <p id="i18n-ai-desc" class="text-xs text-slate-500 dark:text-slate-400">Ask questions based on live project, EVM calculations and schedule data.</p>
            </div>
            <div class="flex items-center gap-2">
              <span id="ai-active-project-pill" class="px-3 py-1.5 bg-slate-100 dark:bg-[#132F5C] border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 rounded-xl text-xs font-bold flex items-center gap-1.5 shadow-2xs">
                <i data-lucide="briefcase" class="w-3.5 h-3.5 text-indigo-500"></i>
                <span id="ai-active-project-name">King Khalid International Airport – Terminal 5</span>
              </span>
              <span class="px-3 py-1.5 bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200 dark:border-indigo-800 text-indigo-700 dark:text-indigo-300 rounded-xl text-xs font-extrabold flex items-center gap-1.5 shadow-2xs">
                <i data-lucide="sparkles" class="w-4 h-4 text-indigo-500 animate-pulse"></i>
                <span id="ai-model-badge-text">Gemini 3.7 Flash Grounded</span>
              </span>
            </div>
          </div>

          <!-- Chat Stream Area -->
          <div class="bg-white dark:bg-[#0B1E3B] rounded-2xl border border-slate-100 dark:border-slate-800 shadow-sm flex flex-col h-[560px] overflow-hidden">
            <div id="chat-messages-container" class="flex-1 p-5 overflow-y-auto space-y-4 custom-scrollbar text-xs">
              <!-- Welcome Bot Message -->
              <div class="flex items-start gap-3 max-w-2xl">
                <div class="w-9 h-9 rounded-2xl bg-[#0B1E3B] dark:bg-indigo-600 text-white flex items-center justify-center shrink-0 shadow-md">
                  <i data-lucide="bot" class="w-4 h-4 text-indigo-400 dark:text-white"></i>
                </div>
                <div class="p-4 bg-slate-50 dark:bg-[#0E2447] rounded-2xl border border-slate-100 dark:border-slate-800 text-slate-800 dark:text-slate-100 space-y-2.5">
                  <p id="i18n-chat-welcome-title" class="font-extrabold text-[#0B1E3B] dark:text-indigo-300">Smart Project Manager Assistant (SPMA)</p>
                  <p id="i18n-chat-welcome-desc" class="leading-relaxed">
                    Welcome! I am your AI Project Controls Partner for managing and monitoring engineering projects across the Saudi Mega-Projects Portfolio. You can ask me via voice or text about completion progress, EVM indices (SPI, CPI), delayed critical activities, site photo inspection, or FIDIC contractual claims.
                  </p>
                  <div id="chat-quick-prompts" class="flex flex-wrap gap-2 pt-1">
                    <button id="i18n-chat-prompt-1" onclick="handlePromptClick(1)" class="px-3 py-1.5 bg-white dark:bg-[#132F5C] border border-slate-200 dark:border-slate-700 rounded-xl text-[11px] font-bold text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700 transition">Project Progress %</button>
                    <button id="i18n-chat-prompt-2" onclick="handlePromptClick(2)" class="px-3 py-1.5 bg-white dark:bg-[#132F5C] border border-slate-200 dark:border-slate-700 rounded-xl text-[11px] font-bold text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700 transition">Calculate EVM (SPI/CPI)</button>
                    <button id="i18n-chat-prompt-3" onclick="handlePromptClick(3)" class="px-3 py-1.5 bg-white dark:bg-[#132F5C] border border-slate-200 dark:border-slate-700 rounded-xl text-[11px] font-bold text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700 transition">Critical Path & Delays</button>
                    <button id="i18n-chat-prompt-4" onclick="handlePromptClick(4)" class="px-3 py-1.5 bg-white dark:bg-[#132F5C] border border-slate-200 dark:border-slate-700 rounded-xl text-[11px] font-bold text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700 transition">FIDIC Claim Notice</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Input Bar with Mic & Vision Upload -->
            <div class="p-3.5 border-t border-slate-100 dark:border-slate-800 bg-slate-50/60 dark:bg-[#0E2447] flex items-center gap-2.5">
              <input type="file" id="vision-file-input" accept="image/*" class="hidden" onchange="handleVisionImageUpload(event)" />
              
              <button type="button" onclick="document.getElementById('vision-file-input').click()" title="Upload Site Photo for AI Vision Inspection" class="p-3 bg-white dark:bg-[#132F5C] border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:text-indigo-600 rounded-xl transition shadow-2xs">
                <i data-lucide="camera" class="w-4 h-4"></i>
              </button>

              <button type="button" onclick="toggleVoiceRecording()" id="voice-btn" title="Voice Speech Recognition" class="p-3 bg-white dark:bg-[#132F5C] border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:text-indigo-600 rounded-xl transition shadow-2xs">
                <i data-lucide="mic" class="w-4 h-4"></i>
              </button>

              <input type="text" id="chat-input" onkeydown="if(event.key==='Enter') handleChatSubmit()" placeholder="Ask about EVM, activities, SPI/CPI, delays, or FIDIC claims..." class="flex-1 bg-white dark:bg-[#132F5C] border border-slate-200 dark:border-slate-700 focus:border-indigo-600 rounded-xl px-4 py-2.5 text-xs text-slate-800 dark:text-slate-100 outline-none transition font-medium shadow-2xs" />

              <button onclick="handleChatSubmit()" class="px-5 py-2.5 bg-[#0B1E3B] dark:bg-indigo-600 hover:bg-[#142A4E] dark:hover:bg-indigo-700 text-white font-extrabold text-xs rounded-xl shadow transition flex items-center gap-2">
                <span id="i18n-chat-btn-send">Send</span>
                <i data-lucide="send" class="w-4 h-4"></i>
              </button>
            </div>
          </div>
        </section>

        <!-- ========================================================================= -->
        <!-- TAB 5: REPORTS                                                            -->
        <!-- ========================================================================= -->
        <section id="tab-reports" class="hidden space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 id="i18n-reports-title" class="text-lg font-black text-[#0B1E3B] dark:text-white">Reports</h2>
              <p id="i18n-reports-desc" class="text-xs text-slate-500 dark:text-slate-400">Generate executive PDF reports and Excel sheets.</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- PDF Report Card -->
            <div class="bg-white dark:bg-[#0B1E3B] p-6 rounded-3xl border border-slate-100 dark:border-slate-800 shadow-sm space-y-4">
              <div class="w-12 h-12 bg-rose-50 dark:bg-rose-950 text-rose-600 dark:text-rose-400 rounded-2xl flex items-center justify-center">
                <i data-lucide="file-text" class="w-6 h-6"></i>
              </div>
              <div>
                <h3 class="font-extrabold text-base text-[#0B1E3B] dark:text-white">Executive EVM & Status Report (PDF)</h3>
                <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 leading-relaxed">Official report with Blue Nile University branding, EVM charts, and schedule breakdown.</p>
              </div>
              <a href="/api/v1/reports/export/pdf" id="btn-export-pdf" target="_blank" class="inline-flex items-center gap-2 px-5 py-3 bg-[#0B1E3B] dark:bg-indigo-600 hover:bg-[#142A4E] dark:hover:bg-indigo-700 text-white font-extrabold text-xs rounded-xl shadow transition">
                <i data-lucide="download" class="w-4 h-4"></i>
                <span>Download Executive PDF</span>
              </a>
            </div>

            <!-- Excel Export Card -->
            <div class="bg-white dark:bg-[#0B1E3B] p-6 rounded-3xl border border-slate-100 dark:border-slate-800 shadow-sm space-y-4">
              <div class="w-12 h-12 bg-emerald-50 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 rounded-2xl flex items-center justify-center">
                <i data-lucide="sheet" class="w-6 h-6"></i>
              </div>
              <div>
                <h3 class="font-extrabold text-base text-[#0B1E3B] dark:text-white">Project Activities & Costs Export (Excel)</h3>
                <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 leading-relaxed">Structured spreadsheet with formulas, planned vs actual costs, and progress tracking.</p>
              </div>
              <a href="/api/v1/reports/export/excel" id="btn-export-excel" target="_blank" class="inline-flex items-center gap-2 px-5 py-3 bg-emerald-700 hover:bg-emerald-800 text-white font-extrabold text-xs rounded-xl shadow transition">
                <i data-lucide="download" class="w-4 h-4"></i>
                <span>Download Excel Sheet</span>
              </a>
            </div>
          </div>
        </section>

        <!-- ========================================================================= -->
        <!-- TAB 6: ENGINEER CHAT                                                      -->
        <!-- ========================================================================= -->
        <section id="tab-engineer-chat" class="hidden space-y-4">
          <div class="flex flex-col md:grid md:grid-cols-4 gap-4 md:gap-6 min-h-[560px] md:h-[620px]">
            <!-- Channels / Rooms List -->
            <div class="bg-white dark:bg-[#0B1E3B] rounded-2xl border border-slate-100 dark:border-slate-800 p-3 sm:p-4 shadow-sm space-y-2 sm:space-y-3">
              <span class="text-xs font-extrabold text-[#0B1E3B] dark:text-white block" id="i18n-chat-channels-title">Communication Channels</span>
              <div class="flex md:flex-col gap-2 overflow-x-auto pb-1 md:pb-0">
                <div id="channel-btn-general" onclick="switchEngChatChannel('general')" class="p-2.5 sm:p-3 bg-indigo-50 dark:bg-[#0E2447] text-[#0B1E3B] dark:text-indigo-300 rounded-xl font-bold text-xs flex items-center justify-between shadow-2xs cursor-pointer border border-indigo-200 dark:border-indigo-800 transition shrink-0 md:shrink min-w-[140px] md:min-w-0">
                  <div class="flex items-center gap-2">
                    <i data-lucide="hash" class="w-4 h-4 text-indigo-600 dark:text-indigo-400"></i>
                    <span id="i18n-channel-general">General Team Chat</span>
                  </div>
                  <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                </div>
                <div id="channel-btn-kkia-t5" onclick="switchEngChatChannel('kkia-t5')" class="p-2.5 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 text-xs font-medium truncate cursor-pointer flex items-center justify-between border border-transparent transition shrink-0 md:shrink min-w-[140px] md:min-w-0">
                  <div class="flex items-center gap-2">
                    <i data-lucide="folder" class="w-3.5 h-3.5 text-slate-400"></i>
                    <span># KKIA Terminal 5</span>
                  </div>
                </div>
              </div>
              <div class="hidden md:block space-y-1 pt-2">
                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">PROJECT TEAM</span>
                <div class="text-[11px] text-slate-400 p-1 space-y-1">
                  <div class="flex items-center gap-2 text-xs text-slate-600 dark:text-slate-300">
                    <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                    <span class="font-medium">6 Engineers Connected</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Main Team Chat Area -->
            <div class="flex-1 md:col-span-3 bg-white dark:bg-[#0B1E3B] rounded-2xl border border-slate-100 dark:border-slate-800 shadow-sm flex flex-col h-[480px] md:h-full overflow-hidden">
              <div class="p-3 sm:p-4 border-b border-slate-100 dark:border-slate-800 flex flex-wrap items-center justify-between gap-2">
                <div class="flex items-center gap-2">
                  <div class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></div>
                  <span id="eng-chat-title" class="font-extrabold text-xs text-[#0B1E3B] dark:text-white">General Team Chat</span>
                  <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 font-bold border border-emerald-200 dark:border-emerald-800">Live Sync</span>
                </div>
                <div class="flex items-center gap-2">
                  <input type="text" id="eng-chat-search" oninput="filterEngChatMessages(this.value)" placeholder="Search messages..." class="bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 rounded-xl px-2.5 py-1 text-xs outline-none w-32 sm:w-44 text-slate-800 dark:text-slate-100 font-medium" />
                  <button onclick="loadEngChatMessages(true)" class="text-xs font-bold text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1 cursor-pointer">
                    <i data-lucide="refresh-cw" class="w-3 h-3"></i>
                    <span>Refresh</span>
                  </button>
                </div>
              </div>
              
              <div id="eng-chat-stream" class="flex-1 p-3.5 sm:p-5 overflow-y-auto space-y-3 sm:space-y-4 custom-scrollbar text-xs">
                <!-- Messages populated dynamically via loadEngChatMessages -->
              </div>

              <!-- Emoji Bar & Message Box -->
              <div class="p-3 sm:p-3.5 border-t border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-[#0E2447] space-y-2">
                <div class="flex items-center gap-2.5 sm:gap-3 text-sm text-slate-500 dark:text-slate-300 cursor-pointer select-none overflow-x-auto pb-0.5">
                  <span onclick="addEmojiToEngChat('👍')">👍</span>
                  <span onclick="addEmojiToEngChat('✅')">✅</span>
                  <span onclick="addEmojiToEngChat('⚠️')">⚠️</span>
                  <span onclick="addEmojiToEngChat('📌')">📌</span>
                  <span onclick="addEmojiToEngChat('📎')">📎</span>
                  <span onclick="addEmojiToEngChat('🙏')">🙏</span>
                  <span onclick="addEmojiToEngChat('🚀')">🚀</span>
                  <span onclick="addEmojiToEngChat('👏')">👏</span>
                </div>
                <form onsubmit="handleEngChatSubmit(event)" class="flex items-center gap-1.5 sm:gap-2">
                  <input type="text" id="eng-chat-input" placeholder="Write a message..." class="flex-1 min-w-0 bg-white dark:bg-[#132F5C] border border-slate-200 dark:border-slate-700 rounded-xl px-3 sm:px-4 py-2 sm:py-2.5 text-xs text-slate-800 dark:text-slate-100 outline-none focus:border-indigo-600 font-medium" />
                  <button type="submit" class="px-3.5 sm:px-5 py-2 sm:py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow transition flex items-center gap-1.5 shrink-0 cursor-pointer">
                    <span>Send</span>
                    <i data-lucide="send" class="w-3.5 h-3.5"></i>
                  </button>
                </form>
              </div>
            </div>
          </div>
        </section>

        <!-- ========================================================================= -->
        <!-- TAB 7: WHATSAPP CENTER                                                    -->
        <!-- ========================================================================= -->
        <section id="tab-whatsapp-center" class="hidden space-y-4">
          <!-- Green Banner -->
          <div class="bg-gradient-to-r from-[#059669] to-[#047857] text-white p-6 rounded-3xl space-y-1.5 shadow-lg">
            <h2 class="text-base font-extrabold flex items-center gap-2">
              <i data-lucide="message-square" class="w-5 h-5"></i>
              <span>WhatsApp Project Update Center</span>
            </h2>
            <p class="text-xs text-emerald-100">Prepare project data, upload a file, open WhatsApp, or send directly through the official Business API when configured.</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Main Form -->
            <div class="md:col-span-2 bg-white dark:bg-[#0B1E3B] rounded-2xl border border-slate-100 dark:border-slate-800 p-6 shadow-sm space-y-4">
              <div class="flex gap-2 border-b border-slate-100 dark:border-slate-800 pb-3">
                <button class="px-4 py-2 bg-emerald-50 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 font-extrabold text-xs rounded-xl border border-emerald-200 dark:border-emerald-800">Quick WhatsApp</button>
                <button class="px-4 py-2 text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 font-bold text-xs rounded-xl">Business API Direct</button>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Project</label>
                  <select class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 rounded-xl p-2.5 text-xs font-semibold text-slate-800 dark:text-slate-200">
                    <option>King Khalid International Airport Branch – Terminal 5</option>
                  </select>
                </div>
                <div>
                  <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Recipient</label>
                  <select id="wa-recipient-select" onchange="updateWaRecipient(this.value)" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 rounded-xl p-2.5 text-xs font-semibold text-slate-800 dark:text-slate-200">
                    <option value="966505554101">Engr. Asem Othman (+966 50 555 4101)</option>
                    <option value="966552345678">Engr. Saleh Mohammed (+966 55 234 5678)</option>
                    <option value="966563456789">Engr. Mohammed Gassim (+966 56 345 6789)</option>
                    <option value="966574567890">Engr. Rafat Mohammed (+966 57 456 7890)</option>
                    <option value="966585678901">Engr. Abu baker Mohammed (+966 58 567 8901)</option>
                  </select>
                </div>
              </div>

              <div>
                <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Phone with country code</label>
                <input type="text" id="wa-phone-input" value="966505554101" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 rounded-xl p-2.5 text-xs font-semibold text-slate-800 dark:text-slate-200" />
              </div>

              <div class="space-y-1.5">
                <div class="flex items-center justify-between">
                  <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Message</label>
                  <div class="flex gap-1.5 text-[10px]">
                    <button type="button" onclick="setWaTemplate('summary')" class="px-2.5 py-1 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 rounded-lg font-bold">Summary</button>
                    <button type="button" onclick="setWaTemplate('delay')" class="px-2.5 py-1 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 rounded-lg font-bold">Delay Update</button>
                    <button type="button" onclick="setWaTemplate('budget')" class="px-2.5 py-1 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 rounded-lg font-bold">Budget Update</button>
                    <button type="button" onclick="document.getElementById('wa-message-textarea').value=''" class="px-2.5 py-1 text-rose-600 hover:bg-rose-50 rounded-lg font-bold">Clear</button>
                  </div>
                </div>
                <textarea id="wa-message-textarea" rows="4" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 rounded-xl p-3 text-xs text-slate-800 dark:text-slate-200 outline-none leading-relaxed">Project Update: King Khalid International Airport Branch – Terminal 5
Progress: 100%
Status: Active
Risk: High
Activities: 1</textarea>
              </div>

              <div class="p-3 bg-slate-50 dark:bg-[#0E2447] rounded-xl border border-dashed border-slate-300 dark:border-slate-700 flex items-center justify-between">
                <input type="file" class="text-xs text-slate-600 dark:text-slate-400" />
                <div class="flex gap-2">
                  <button onclick="generateDataCsv()" class="px-3.5 py-1.5 bg-white dark:bg-[#132F5C] border border-slate-200 dark:border-slate-700 rounded-xl text-xs font-bold hover:bg-slate-50">Generate Project Data CSV</button>
                </div>
              </div>

              <div class="flex items-center gap-3 pt-2">
                <button type="button" onclick="sendViaWhatsApp()" class="flex-1 py-3.5 bg-[#059669] hover:bg-[#047857] text-white font-extrabold text-xs rounded-xl shadow transition flex items-center justify-center gap-2">
                  <i data-lucide="send" class="w-4 h-4"></i>
                  <span>Open WhatsApp & Send</span>
                </button>
                <button type="button" onclick="copyWaMessage()" class="px-5 py-3.5 bg-slate-100 dark:bg-[#0E2447] hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold text-xs rounded-xl transition">
                  Copy Message
                </button>
              </div>
            </div>

            <!-- Side Card: Instructions -->
            <div class="bg-white dark:bg-[#0B1E3B] rounded-2xl border border-slate-100 dark:border-slate-800 p-6 shadow-sm space-y-4">
              <h3 class="font-extrabold text-xs text-[#0B1E3B] dark:text-white border-b border-slate-100 dark:border-slate-800 pb-2.5">How It Works</h3>
              <div class="space-y-3.5 text-xs text-slate-600 dark:text-slate-300">
                <div class="flex items-start gap-2.5">
                  <span class="w-6 h-6 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 font-extrabold flex items-center justify-center text-xs shrink-0">1</span>
                  <p>Pick a template or write a custom message to your site engineer.</p>
                </div>
                <div class="flex items-start gap-2.5">
                  <span class="w-6 h-6 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 font-extrabold flex items-center justify-center text-xs shrink-0">2</span>
                  <p>Optionally attach project data or generated PDF/Excel reports.</p>
                </div>
                <div class="flex items-start gap-2.5">
                  <span class="w-6 h-6 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 font-extrabold flex items-center justify-center text-xs shrink-0">3</span>
                  <p>Click "Open WhatsApp" to dispatch instantly via WhatsApp Web or mobile app.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- ========================================================================= -->
        <!-- TAB 8: USER MANAGEMENT                                                    -->
        <!-- ========================================================================= -->
        <section id="tab-user-mgmt" class="hidden space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 id="i18n-user-mgmt-title" class="text-lg font-black text-[#0B1E3B] dark:text-white">Global User Management</h2>
              <p id="i18n-user-mgmt-desc" class="text-xs text-slate-500 dark:text-slate-400">Accounts belong to the whole program, not one project.</p>
            </div>
            <button onclick="openCreateUserModal()" class="px-4 py-2.5 bg-[#0B1E3B] dark:bg-indigo-600 hover:bg-[#142A4E] dark:hover:bg-indigo-700 text-white font-extrabold text-xs rounded-xl shadow transition flex items-center gap-2">
              <i data-lucide="user-plus" class="w-4 h-4"></i>
              <span>+ New User</span>
            </button>
          </div>

          <div class="bg-white dark:bg-[#0B1E3B] rounded-2xl border border-slate-100 dark:border-slate-800 shadow-sm overflow-hidden">
            <div class="overflow-x-auto">
              <table class="w-full text-xs text-left border-collapse min-w-[620px]" id="users-table">
                <thead class="bg-slate-50 dark:bg-[#0E2447] text-slate-400 font-bold border-b border-slate-100 dark:border-slate-800">
                  <tr>
                    <th class="p-3.5">User</th>
                    <th class="p-3.5">Email</th>
                    <th class="p-3.5">Role</th>
                    <th class="p-3.5">Phone</th>
                    <th class="p-3.5">Status</th>
                    <th class="p-3.5 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody id="users-tbody" class="divide-y divide-slate-100 dark:divide-slate-800 text-slate-700 dark:text-slate-200 font-medium">
                  <tr><td colspan="6" class="p-6 text-center text-slate-400">Loading user accounts...</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- ========================================================================= -->
        <!-- TAB 9: SETTINGS                                                           -->
        <!-- ========================================================================= -->
        <section id="tab-settings" class="hidden space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- AI Engine & Gemini API Key Settings -->
            <div class="bg-white dark:bg-[#0B1E3B] p-6 rounded-3xl border border-slate-100 dark:border-slate-800 shadow-sm space-y-4">
              <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-2.5">
                <div class="flex items-center gap-2.5">
                  <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-600 to-indigo-400 flex items-center justify-center text-white shadow-sm">
                    <i data-lucide="sparkles" class="w-4 h-4"></i>
                  </div>
                  <div>
                    <h3 id="i18n-settings-ai-title" class="font-extrabold text-sm text-[#0B1E3B] dark:text-white">Google Gemini AI Configuration</h3>
                    <p id="i18n-settings-ai-sub" class="text-[11px] text-slate-400 font-medium">Configure Gemini API key, model selection & live health test</p>
                  </div>
                </div>
                <span id="gemini-status-badge" class="px-2.5 py-1 rounded-full text-[10px] font-black bg-emerald-100 dark:bg-emerald-950/80 text-emerald-700 dark:text-emerald-300 flex items-center gap-1.5 shadow-xs">
                  <span id="gemini-status-dot" class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                  <span id="gemini-status-text">Active</span>
                </span>
              </div>

              <div class="space-y-3.5">
                <!-- Gemini API Key Input Field -->
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <label id="i18n-settings-lbl-key" class="block text-xs font-bold text-slate-700 dark:text-slate-300">
                      Google Gemini API Key
                    </label>
                    <a href="https://aistudio.google.com/app/apikey" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 text-[11px] font-bold text-indigo-600 dark:text-indigo-400 hover:underline">
                      <i data-lucide="external-link" class="w-3 h-3"></i>
                      <span id="i18n-settings-get-key">Get Key from Google AI Studio</span>
                    </a>
                  </div>
                  <div class="relative flex items-center">
                    <input 
                      type="password" 
                      id="settings-gemini-key" 
                      placeholder="Enter Gemini API key (e.g. AIzaSy...)" 
                      autocomplete="off"
                      spellcheck="false"
                      class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 rounded-xl py-2.5 pl-3 pr-20 text-xs font-mono font-medium text-slate-800 dark:text-white outline-none focus:border-indigo-600 focus:ring-1 focus:ring-indigo-600/30 transition"
                    />
                    <div class="absolute right-1.5 flex items-center gap-1">
                      <button 
                        type="button" 
                        onclick="toggleGeminiKeyVisibility()" 
                        title="Show/Hide API Key"
                        class="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700/60 transition">
                        <i id="gemini-key-eye-icon" data-lucide="eye" class="w-4 h-4"></i>
                      </button>
                      <button 
                        type="button" 
                        onclick="copyGeminiKey()" 
                        title="Copy Key to Clipboard"
                        class="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700/60 transition">
                        <i id="gemini-key-copy-icon" data-lucide="copy" class="w-4 h-4"></i>
                      </button>
                    </div>
                  </div>
                  <p id="i18n-settings-key-hint" class="text-[10px] text-slate-400 mt-1 font-medium">
                    The API key is securely stored in backend/.env for agentic reasoning and visual site inspections.
                  </p>
                </div>

                <!-- Primary Model Select -->
                <div>
                  <label id="i18n-settings-lbl-model" class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">
                    Default Gemini Model
                  </label>
                  <select id="settings-gemini-model" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 rounded-xl p-2.5 text-xs font-bold text-slate-800 dark:text-white outline-none focus:border-indigo-600">
                    <option value="gemini-3.7-flash" selected>Google Gemini 3.7 Flash (Active Default • Hybrid Reasoning)</option>
                    <option value="gemini-3.8-flash">Google Gemini 3.8 Flash (Latest Grounded Multimodal Model)</option>
                    <option value="gemini-2.5-flash">Google Gemini 2.5 Flash (Fast Execution)</option>
                    <option value="gemini-2.5-pro">Google Gemini 2.5 Pro (Deep Engineering Analysis)</option>
                    <option value="gemini-1.5-flash">Google Gemini 1.5 Flash (Lightweight & High Quota)</option>
                  </select>
                </div>

                <!-- Live Health & Latency Status Banner -->
                <div id="gemini-ping-banner" class="p-3 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-xl flex items-center justify-between transition-colors">
                  <div class="flex items-center gap-2">
                    <span id="gemini-ping-dot" class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                    <span id="gemini-ping-status" class="text-xs font-bold text-emerald-800 dark:text-emerald-300">Gemini API Status: Operational (200 OK)</span>
                  </div>
                  <span id="gemini-ping-latency" class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 dark:bg-emerald-900/60 text-emerald-700 dark:text-emerald-300">Ready</span>
                </div>

                <!-- Feedback Toast -->
                <div id="gemini-feedback-msg" class="hidden text-xs font-bold p-3 rounded-xl transition-all"></div>

                <!-- Action Buttons: Save & Test Connection -->
                <div class="flex flex-wrap items-center gap-3 pt-1">
                  <button 
                    type="button" 
                    id="btn-save-gemini" 
                    onclick="saveGeminiApiKey()" 
                    class="px-5 py-2.5 bg-[#0B1E3B] dark:bg-indigo-600 hover:bg-[#142A4E] dark:hover:bg-indigo-700 text-white text-xs font-extrabold rounded-xl shadow transition flex items-center gap-2">
                    <i id="btn-save-gemini-icon" data-lucide="save" class="w-4 h-4"></i>
                    <span id="i18n-settings-btn-save">Save API Key</span>
                  </button>
                  <button 
                    type="button" 
                    id="btn-test-gemini" 
                    onclick="testGeminiApiConnection()" 
                    class="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-extrabold rounded-xl shadow transition flex items-center gap-2">
                    <i id="btn-test-gemini-icon" data-lucide="activity" class="w-4 h-4"></i>
                    <span id="i18n-settings-btn-test">Test Connection</span>
                  </button>
                </div>
              </div>
            </div>

            <!-- Change Password -->
            <div class="bg-white dark:bg-[#0B1E3B] p-6 rounded-3xl border border-slate-100 dark:border-slate-800 shadow-sm space-y-4">
              <h3 class="font-extrabold text-sm text-[#0B1E3B] dark:text-white border-b border-slate-100 dark:border-slate-800 pb-2.5">Security & Password</h3>
              <div class="space-y-3">
                <div>
                  <label class="block text-xs font-bold text-slate-600 dark:text-slate-400 mb-1">Current Password</label>
                  <input type="password" placeholder="••••••••" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 rounded-xl p-3 text-xs outline-none focus:border-indigo-600 text-slate-800 dark:text-white font-medium" />
                </div>
                <div>
                  <label class="block text-xs font-bold text-slate-600 dark:text-slate-400 mb-1">New Password</label>
                  <input type="password" placeholder="••••••••" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 rounded-xl p-3 text-xs outline-none focus:border-indigo-600 text-slate-800 dark:text-white font-medium" />
                </div>
                <button onclick="alert('Password updated successfully!')" class="px-5 py-2.5 bg-[#0B1E3B] dark:bg-indigo-600 hover:bg-[#142A4E] text-white text-xs font-bold rounded-xl shadow transition">Change Password</button>
              </div>
            </div>

            <!-- System Information -->
            <div class="md:col-span-2 bg-white dark:bg-[#0B1E3B] p-6 rounded-3xl border border-slate-100 dark:border-slate-800 shadow-sm space-y-3">
              <h3 class="font-extrabold text-sm text-[#0B1E3B] dark:text-white border-b border-slate-100 dark:border-slate-800 pb-2.5">Academic & System Information</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-slate-700 dark:text-slate-300">
                <div class="space-y-1">
                  <p class="font-bold text-[#0B1E3B] dark:text-indigo-300 text-sm">Smart Project Manager Assistant (SPMA)</p>
                  <p class="text-slate-500 dark:text-slate-400 font-semibold">Blue Nile University - Faculty of Engineering</p>
                  <p class="text-indigo-600 dark:text-indigo-400 font-bold pt-1">B.Sc. Civil Engineering Graduation Thesis 2026</p>
                </div>
                <div class="p-3.5 bg-slate-50 dark:bg-[#0E2447] rounded-2xl border border-slate-200 dark:border-slate-700 space-y-1 text-[11px]">
                  <p><span class="font-bold">Backend Architecture:</span> FastAPI Python + ChromaDB Vector RAG</p>
                  <p><span class="font-bold">EVM Engine:</span> Integrated S-Curve & Critical Path Tracker</p>
                  <p><span class="font-bold">Vision & Voice:</span> Google Gemini Multimodal Reasoning & Web Speech</p>
                </div>
              </div>
            </div>
          </div>
        </section>

      </div>

      <!-- Mobile Bottom Navigation Bar (Visible only on mobile md:hidden) -->
      <nav id="mobile-bottom-nav" class="md:hidden fixed bottom-0 inset-x-0 z-30 bg-white/95 dark:bg-[#0B1E3B]/95 backdrop-blur-lg border-t border-slate-200/90 dark:border-slate-800/90 shadow-2xl px-2 py-1 flex items-center justify-around select-none">
        
        <!-- 1. Dashboard -->
        <button onclick="switchTab('dashboard')" id="mob-nav-dashboard" class="flex flex-col items-center justify-center py-1 px-2 rounded-xl transition text-indigo-600 dark:text-indigo-400 font-bold cursor-pointer">
          <i data-lucide="layout-dashboard" class="w-5 h-5"></i>
          <span class="text-[10px] mt-0.5" id="i18n-mob-nav-dash">Home</span>
        </button>

        <!-- 2. Projects -->
        <button onclick="switchTab('projects')" id="mob-nav-projects" class="flex flex-col items-center justify-center py-1 px-2 rounded-xl transition text-slate-500 dark:text-slate-400 hover:text-indigo-600 font-medium cursor-pointer">
          <i data-lucide="briefcase" class="w-5 h-5"></i>
          <span class="text-[10px] mt-0.5" id="i18n-mob-nav-proj">Projects</span>
        </button>

        <!-- 3. Activities -->
        <button onclick="switchTab('activities')" id="mob-nav-activities" class="flex flex-col items-center justify-center py-1 px-2 rounded-xl transition text-slate-500 dark:text-slate-400 hover:text-indigo-600 font-medium cursor-pointer">
          <i data-lucide="calendar-check-2" class="w-5 h-5"></i>
          <span class="text-[10px] mt-0.5" id="i18n-mob-nav-act">Activities</span>
        </button>

        <!-- 4. Engineer Chat -->
        <button onclick="switchTab('engineer-chat')" id="mob-nav-engineer-chat" class="relative flex flex-col items-center justify-center py-1 px-2 rounded-xl transition text-slate-500 dark:text-slate-400 hover:text-indigo-600 font-medium cursor-pointer">
          <i data-lucide="message-square" class="w-5 h-5"></i>
          <span id="mob-chat-badge" class="hidden absolute -top-0.5 right-1.5 px-1.5 py-0.2 bg-rose-500 text-white rounded-full text-[9px] font-black leading-none animate-pulse">0</span>
          <span class="text-[10px] mt-0.5" id="i18n-mob-nav-chat">Chat</span>
        </button>

        <!-- 5. More / Menu -->
        <button onclick="toggleMobileSidebar()" id="mob-nav-more" class="flex flex-col items-center justify-center py-1 px-2 rounded-xl transition text-slate-500 dark:text-slate-400 hover:text-indigo-600 font-medium cursor-pointer">
          <i data-lucide="menu" class="w-5 h-5"></i>
          <span class="text-[10px] mt-0.5" id="i18n-mob-nav-more">More</span>
        </button>

      </nav>

    </main>

  </div>

  <!-- ========================================================================= -->
  <!-- 3. INTERACTIVE MODALS                                                     -->
  <!-- ========================================================================= -->

  <!-- Add Activity Modal -->
  <div id="add-activity-modal" class="hidden fixed inset-0 modal-overlay z-[70] flex items-center justify-center p-3 sm:p-4">
    <div class="bg-white dark:bg-[#0B1E3B] rounded-3xl max-w-lg w-full p-4 sm:p-6 space-y-4 shadow-2xl border border-slate-200 dark:border-slate-700 max-h-[92vh] overflow-y-auto custom-scrollbar">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
        <h3 class="font-extrabold text-sm text-[#0B1E3B] dark:text-white">Add New Activity</h3>
        <button onclick="closeAddActivityModal()" class="w-7 h-7 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 flex items-center justify-center cursor-pointer">✕</button>
      </div>
      <form onsubmit="handleAddActivitySubmit(event)" class="space-y-3">
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Activity Name</label>
            <input type="text" id="new-act-name" required placeholder="e.g. Steel Rebar Fixing" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs outline-none focus:border-indigo-600" />
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Status</label>
            <select id="new-act-status" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs font-semibold">
              <option value="in_progress">In Progress</option>
              <option value="delayed">Delayed</option>
              <option value="completed">Completed</option>
            </select>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Planned End Date</label>
            <input type="date" id="new-act-end" value="2026-04-15" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs font-semibold" />
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Actual %</label>
            <input type="number" id="new-act-prog" value="50" min="0" max="100" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs font-bold text-indigo-600" />
          </div>
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Actual Spent (SAR)</label>
          <input type="number" id="new-act-spent" value="5000" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs font-bold" />
        </div>
        <div class="flex gap-2 pt-2">
          <button type="submit" class="flex-1 py-3 bg-[#0B1E3B] dark:bg-indigo-600 hover:bg-[#142A4E] text-white font-extrabold text-xs rounded-xl shadow transition cursor-pointer">Save Activity</button>
          <button type="button" onclick="closeAddActivityModal()" class="px-5 py-3 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold text-xs rounded-xl cursor-pointer">Cancel</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Edit Activity Modal -->
  <div id="edit-activity-modal" class="hidden fixed inset-0 modal-overlay z-[70] flex items-center justify-center p-3 sm:p-4">
    <div class="bg-white dark:bg-[#0B1E3B] rounded-3xl max-w-lg w-full p-4 sm:p-6 space-y-4 shadow-2xl border border-slate-200 dark:border-slate-700 max-h-[92vh] overflow-y-auto custom-scrollbar">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
        <h3 class="font-extrabold text-sm text-[#0B1E3B] dark:text-white">Edit Activity Progress</h3>
        <button onclick="closeEditActivityModal()" class="w-7 h-7 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 flex items-center justify-center cursor-pointer">✕</button>
      </div>
      <form onsubmit="handleEditActivitySubmit(event)" class="space-y-3">
        <div>
          <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Activity Name</label>
          <input type="text" id="edit-act-name" readonly class="w-full bg-slate-100 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs font-bold" />
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Status</label>
            <select id="edit-act-status" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs font-semibold">
              <option value="in_progress">In Progress</option>
              <option value="delayed">Delayed</option>
              <option value="completed">Completed</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Planned End Date</label>
            <input type="date" id="edit-act-end" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs font-semibold" />
          </div>
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Actual %</label>
            <input type="number" id="edit-act-prog" min="0" max="100" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs font-bold text-indigo-600" />
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Actual Spent (SAR)</label>
            <input type="number" id="edit-act-spent" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs font-bold" />
          </div>
        </div>
        <div class="flex gap-2 pt-2">
          <button type="submit" class="flex-1 py-3 bg-[#0B1E3B] dark:bg-indigo-600 hover:bg-[#142A4E] text-white font-extrabold text-xs rounded-xl shadow transition">Update Activity</button>
          <button type="button" onclick="closeEditActivityModal()" class="px-5 py-3 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold text-xs rounded-xl">Cancel</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Add Project Modal -->
  <div id="add-project-modal" class="hidden fixed inset-0 modal-overlay z-[70] flex items-center justify-center p-3 sm:p-4">
    <div class="bg-white dark:bg-[#0B1E3B] rounded-3xl max-w-lg w-full p-4 sm:p-6 space-y-4 shadow-2xl border border-slate-200 dark:border-slate-700 max-h-[92vh] overflow-y-auto custom-scrollbar">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
        <h3 class="font-extrabold text-sm text-[#0B1E3B] dark:text-white">Create New Project</h3>
        <button onclick="closeAddProjectModal()" class="w-7 h-7 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 flex items-center justify-center cursor-pointer">✕</button>
      </div>
      <form onsubmit="handleAddProjectSubmit(event)" class="space-y-3">
        <div>
          <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Project Name</label>
          <input type="text" id="new-prj-name" required placeholder="King Khalid International Airport Branch – Terminal 5" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs outline-none focus:border-indigo-600 font-medium" />
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Project Code</label>
            <input type="text" id="new-prj-code" required placeholder="KKIA-T5" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs font-mono font-bold" />
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Budget (SAR)</label>
            <input type="number" id="new-prj-budget" value="931512.29" step="any" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs font-bold" />
          </div>
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Description</label>
          <textarea id="new-prj-desc" rows="2" placeholder="Project scope, Primavera XER mapping and milestones..." class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs outline-none font-medium"></textarea>
        </div>
        <div class="flex gap-2 pt-2">
          <button type="submit" class="flex-1 py-3 bg-[#0B1E3B] dark:bg-indigo-600 hover:bg-[#142A4E] text-white font-extrabold text-xs rounded-xl shadow transition">Create Project</button>
          <button type="button" onclick="closeAddProjectModal()" class="px-5 py-3 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold text-xs rounded-xl">Cancel</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Project Workspace Modal (Detailed EVM, Health Gauge & Breakdown) -->
  <div id="workspace-modal" class="hidden fixed inset-0 modal-overlay z-50 flex items-center justify-center p-4">
    <div class="bg-white dark:bg-[#0B1E3B] rounded-3xl max-w-3xl w-full p-6 space-y-5 shadow-2xl border border-slate-200 dark:border-slate-700 max-h-[90vh] overflow-y-auto custom-scrollbar">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl bg-indigo-600 text-white font-black flex items-center justify-center shadow">KK</div>
          <div>
            <h3 class="font-extrabold text-sm text-[#0B1E3B] dark:text-white" id="ws-modal-title">King Khalid International Airport Branch – Terminal 5</h3>
            <p class="text-xs text-slate-400 font-medium">Project Code: <span id="ws-modal-code" class="font-mono text-indigo-400 font-bold">KKIA-T5</span> • Active Workspace</p>
          </div>
        </div>
        <button onclick="closeWorkspaceModal()" class="w-8 h-8 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-400 hover:text-slate-700 dark:hover:text-white flex items-center justify-center">✕</button>
      </div>

      <!-- Top Row: Circular Gauge + Financial Summary -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div class="bg-slate-50 dark:bg-[#0E2447] p-4 rounded-2xl border border-slate-100 dark:border-slate-800 flex flex-col items-center justify-center text-center space-y-1">
          <div class="relative w-20 h-20 flex items-center justify-center">
            <svg class="w-full h-full transform -rotate-90">
              <circle cx="40" cy="40" r="32" stroke="currentColor" class="text-slate-200 dark:text-slate-700" stroke-width="8" fill="transparent" />
              <circle id="ws-modal-circle" cx="40" cy="40" r="32" stroke="#10B981" stroke-width="8" stroke-dasharray="200" stroke-dashoffset="0" fill="transparent" stroke-linecap="round" />
            </svg>
            <span id="ws-modal-pct" class="absolute font-black text-sm text-[#0B1E3B] dark:text-white">100%</span>
          </div>
          <span class="text-xs font-bold text-slate-700 dark:text-slate-300">Completion Rate</span>
          <span class="text-[10px] text-emerald-600 dark:text-emerald-400 font-bold">● Active Status</span>
        </div>

        <div class="bg-slate-50 dark:bg-[#0E2447] p-4 rounded-2xl border border-slate-100 dark:border-slate-800 space-y-2">
          <span class="text-[11px] font-bold text-slate-400 uppercase">Budget Overview</span>
          <p id="ws-modal-total-budget" class="text-lg font-black text-[#0B1E3B] dark:text-white tabular-nums">SAR 931,512.29</p>
          <div class="space-y-1 text-xs">
            <div class="flex justify-between text-slate-500 dark:text-slate-400">
              <span>Actual Spent:</span>
              <span id="ws-modal-spent" class="font-bold text-slate-800 dark:text-slate-200">SAR 1,000.00</span>
            </div>
            <div class="flex justify-between text-slate-500 dark:text-slate-400">
              <span>Remaining:</span>
              <span id="ws-modal-remaining" class="font-bold text-emerald-600 dark:text-emerald-400">SAR 930,512.29</span>
            </div>
          </div>
        </div>

        <div class="bg-slate-50 dark:bg-[#0E2447] p-4 rounded-2xl border border-slate-100 dark:border-slate-800 space-y-2">
          <span class="text-[11px] font-bold text-slate-400 uppercase">EVM Indices</span>
          <div class="grid grid-cols-2 gap-2 pt-1 text-center">
            <div class="p-2 bg-white dark:bg-[#132F5C] rounded-xl border border-slate-200 dark:border-slate-700">
              <span class="text-[10px] text-slate-400 block font-bold">SPI</span>
              <span id="ws-modal-spi" class="text-sm font-black text-emerald-600">1.00</span>
            </div>
            <div class="p-2 bg-white dark:bg-[#132F5C] rounded-xl border border-slate-200 dark:border-slate-700">
              <span class="text-[10px] text-slate-400 block font-bold">CPI</span>
              <span id="ws-modal-cpi" class="text-sm font-black text-emerald-600">1.00</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Activities List in Workspace -->
      <div class="space-y-2">
        <div class="flex items-center justify-between">
          <span id="ws-modal-act-header" class="text-xs font-bold text-[#0B1E3B] dark:text-white">Project Activities</span>
          <button onclick="openAddActivityModal()" class="text-xs font-bold text-indigo-600 dark:text-indigo-400 hover:underline">+ Add Item</button>
        </div>
        <div id="ws-modal-activities-list" class="space-y-2">
          <!-- Dynamic activity rows populated by JS -->
        </div>
      </div>

      <div class="flex justify-end pt-2 border-t border-slate-100 dark:border-slate-800">
        <button onclick="closeWorkspaceModal()" class="px-5 py-2.5 bg-[#0B1E3B] dark:bg-indigo-600 hover:bg-[#142A4E] text-white font-bold text-xs rounded-xl shadow">Close Workspace</button>
      </div>
    </div>
  </div>

  <!-- Create User Modal -->
  <div id="create-user-modal" class="hidden fixed inset-0 modal-overlay z-[70] flex items-center justify-center p-3 sm:p-4">
    <div class="bg-white dark:bg-[#0B1E3B] rounded-3xl max-w-md w-full p-4 sm:p-6 space-y-4 shadow-2xl border border-slate-200 dark:border-slate-700 max-h-[92vh] overflow-y-auto custom-scrollbar">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
        <h3 class="font-extrabold text-sm text-[#0B1E3B] dark:text-white">Create New User</h3>
        <button onclick="closeCreateUserModal()" class="w-7 h-7 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 flex items-center justify-center cursor-pointer">✕</button>
      </div>
      <form onsubmit="handleCreateUserSubmit(event)" class="space-y-3">
        <div>
          <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Full Name</label>
          <input type="text" id="new-user-name" required placeholder="Engr. Khalid Ali" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs outline-none focus:border-indigo-600 font-medium" />
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Email</label>
          <input type="email" id="new-user-email" required placeholder="khalid@company.com" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs outline-none focus:border-indigo-600 font-medium" />
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Role</label>
            <select id="new-user-role" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs font-semibold">
              <option value="PROJECT_DIRECTOR">Project Director / Manager</option>
              <option value="SITE_MANAGER">Site Manager</option>
              <option value="PLANNING_ENGINEER">Planning Engineer</option>
              <option value="QA_QC_MANAGER">Quality Engineer (QA/QC)</option>
              <option value="PROCUREMENT_OFFICER">Cost / Procurement Engineer</option>
              <option value="VIEWER">Viewer</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Phone</label>
            <input type="text" id="new-user-phone" value="+966 50 123 4567" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs font-medium" />
          </div>
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Password</label>
          <input type="text" id="new-user-password" value="Admin123" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs font-mono font-bold" />
        </div>
        <div class="flex gap-2 pt-2">
          <button type="submit" class="flex-1 py-3 bg-[#0B1E3B] dark:bg-indigo-600 hover:bg-[#142A4E] text-white font-extrabold text-xs rounded-xl shadow transition">Create Account</button>
          <button type="button" onclick="closeCreateUserModal()" class="px-5 py-3 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold text-xs rounded-xl">Cancel</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Edit User Modal -->
  <div id="edit-user-modal" class="hidden fixed inset-0 modal-overlay z-[70] flex items-center justify-center p-3 sm:p-4">
    <div class="bg-white dark:bg-[#0B1E3B] rounded-3xl max-w-md w-full p-4 sm:p-6 space-y-4 shadow-2xl border border-slate-200 dark:border-slate-700 max-h-[92vh] overflow-y-auto custom-scrollbar">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
        <h3 class="font-extrabold text-sm text-[#0B1E3B] dark:text-white">Edit User Account</h3>
        <button onclick="closeEditUserModal()" class="w-7 h-7 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 flex items-center justify-center cursor-pointer">✕</button>
      </div>
      <form onsubmit="handleEditUserSubmit(event)" class="space-y-3">
        <input type="hidden" id="edit-user-id" />
        <div>
          <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Full Name</label>
          <input type="text" id="edit-user-name" required class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs outline-none focus:border-indigo-600 font-medium" />
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Username / Email (اسم الدخول / البريد الإلكتروني)</label>
          <input type="text" id="edit-user-email" required placeholder="e.g. qsem.othman or asem.othman@company.com" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs outline-none focus:border-indigo-600 font-bold" />
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Role</label>
            <select id="edit-user-role" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs font-semibold">
              <option value="PROJECT_DIRECTOR">Project Director / Manager</option>
              <option value="SITE_MANAGER">Site Manager</option>
              <option value="PLANNING_ENGINEER">Planning Engineer</option>
              <option value="QA_QC_MANAGER">Quality Engineer (QA/QC)</option>
              <option value="PROCUREMENT_OFFICER">Cost / Procurement Engineer</option>
              <option value="VIEWER">Viewer</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">Phone</label>
            <input type="text" id="edit-user-phone" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs font-medium" />
          </div>
        </div>
        <div class="pt-2 border-t border-slate-100 dark:border-slate-800 space-y-1">
          <div class="flex items-center justify-between">
            <label class="block text-xs font-bold text-slate-600 dark:text-slate-300">New Password (كلمة المرور الجديدة)</label>
            <button type="button" onclick="document.getElementById('edit-user-password').value='Admin123'" class="text-[10px] text-indigo-600 dark:text-indigo-400 hover:underline font-bold cursor-pointer">Set to: Admin123</button>
          </div>
          <input type="text" id="edit-user-password" placeholder="Leave blank to keep current, or enter new password..." class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs outline-none focus:border-indigo-600 font-medium" />
          <p class="text-[10px] text-slate-400">اترك الحقل فارغاً للإبقاء على كلمة المرور، أو اكتب كلمة مرور جديدة للتطبيق الفوري.</p>
        </div>
        <div class="flex gap-2 pt-2">
          <button type="submit" class="flex-1 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-extrabold text-xs rounded-xl shadow transition">Save Changes</button>
          <button type="button" onclick="closeEditUserModal()" class="px-5 py-3 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold text-xs rounded-xl">Cancel</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Reset Password Modal (Directly accessible from Login Page) -->
  <div id="login-reset-pass-modal" class="hidden fixed inset-0 modal-overlay z-[80] flex items-center justify-center p-3 sm:p-4">
    <div class="bg-white dark:bg-[#0B1E3B] rounded-3xl max-w-md w-full p-4 sm:p-6 space-y-4 shadow-2xl border border-slate-200 dark:border-slate-700 max-h-[92vh] overflow-y-auto custom-scrollbar">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-500 flex items-center justify-center shrink-0">
            <i data-lucide="key-round" class="w-4 h-4"></i>
          </div>
          <div>
            <h3 class="font-extrabold text-sm text-[#0B1E3B] dark:text-white" id="i18n-reset-modal-title">Reset Account Password</h3>
            <p class="text-[10px] text-slate-400" id="i18n-reset-modal-sub">Update password for any user account instantly</p>
          </div>
        </div>
        <button onclick="closeResetPasswordModal()" class="w-7 h-7 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 flex items-center justify-center cursor-pointer">✕</button>
      </div>

      <form onsubmit="handleResetPasswordSubmit(event)" class="space-y-3.5">
        <div>
          <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1" id="i18n-reset-lbl-user">Username or Email (اسم الدخول أو البريد)</label>
          <input type="text" id="reset-user-identifier" required placeholder="e.g. qsem.othman or admin" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs outline-none focus:border-indigo-600 font-bold" />
        </div>

        <div>
          <div class="flex items-center justify-between mb-1">
            <label class="block text-xs font-bold text-slate-600 dark:text-slate-300" id="i18n-reset-lbl-pass">New Password (كلمة المرور الجديدة)</label>
            <button type="button" onclick="document.getElementById('reset-new-password').value='Admin123'" class="text-[10px] text-indigo-600 dark:text-indigo-400 hover:underline font-bold cursor-pointer">Use Default: Admin123</button>
          </div>
          <input type="text" id="reset-new-password" required value="Admin123" class="w-full bg-slate-50 dark:bg-[#0E2447] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-xl p-2.5 text-xs outline-none focus:border-indigo-600 font-bold" />
          <p class="text-[10px] text-slate-400 mt-1" id="i18n-reset-hint">يتم تحديث كلمة المرور فوراً في قاعدة البيانات وتفعيلها للدخول.</p>
        </div>

        <div id="reset-feedback-msg" class="hidden text-xs font-bold p-3 rounded-xl border"></div>

        <div class="flex gap-2 pt-1">
          <button type="submit" id="btn-save-reset-pass" class="flex-1 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-extrabold text-xs rounded-xl shadow transition flex items-center justify-center gap-2 cursor-pointer">
            <i data-lucide="check" class="w-4 h-4"></i>
            <span id="i18n-reset-btn-confirm">Save & Login Now</span>
          </button>
          <button type="button" onclick="closeResetPasswordModal()" class="px-5 py-3 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold text-xs rounded-xl cursor-pointer" id="i18n-reset-btn-cancel">Cancel</button>
        </div>
      </form>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- 4. JAVASCRIPT LOGIC & BILINGUAL ENGINE                                    -->
  <!-- ========================================================================= -->
  <script>
    const I18N = {
      en: {
        loginThesisBadge: "B.Sc. Graduation Research Thesis • 2026",
        loginMainTitle: "Smart Project Manager Assistant (SPMA)",
        loginMainDesc: "Next-generation civil project intelligence combining Earned Value Management (EVM), Primavera XER schedule tracking, Multimodal Vision site inspections, and bilingual voice-driven AI agents.",
        loginTeamHead: "Graduation Research Team",
        loginCardTitle: "Welcome Back",
        loginCardSub: "Sign in with your authorized credentials to access the project intelligence workspace.",
        loginLblUser: "USERNAME",
        loginLblPass: "PASSWORD",
        loginBtnSign: "Sign In to Workspace",
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
        btnTopProject: "Project",
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
        btnNewProjTab: "New Project",
        activitiesTitle: "Activities",
        activitiesDesc: "Track planned and actual progress and upcoming deadlines.",
        btnNewActivityTab: "+ New Activity",
        aiTitle: "AI Assistant",
        aiDesc: "Ask questions based on live project, EVM calculations and schedule data.",
        reportsTitle: "Reports",
        reportsDesc: "Generate executive PDF reports and Excel sheets.",
        userMgmtTitle: "Global User Management",
        userMgmtDesc: "Accounts belong to the whole program, not one project.",
        settingsAiTitle: "Google Gemini AI Configuration",
        settingsAiSub: "Configure Gemini API key, model selection & live health test",
        settingsLblKey: "Google Gemini API Key",
        settingsGetKey: "Get Key from Google AI Studio",
        settingsKeyHint: "The API key is securely stored in backend/.env for agentic reasoning and visual site inspections.",
        settingsLblModel: "Default Gemini Model",
        settingsBtnSave: "Save API Key",
        settingsBtnTest: "Test Connection",
        chatWelcomeTitle: "Smart Project Manager Assistant (SPMA)",
        chatWelcomeDesc: "Welcome! I am your AI Project Controls Partner for managing and monitoring engineering projects across the Saudi Mega-Projects Portfolio. You can ask me via voice or text about completion progress, EVM indices (SPI, CPI), delayed critical activities, site photo inspection, or FIDIC contractual claims.",
        chatPromptProgress: "Project Progress %",
        chatPromptEvm: "Calculate EVM (SPI/CPI)",
        chatPromptCritical: "Critical Path & Delays",
        chatPromptFidic: "FIDIC Claim Notice",
        chatBtnSend: "Send",
        chatInputPlaceholder: "Ask about EVM, activities, SPI/CPI, delays, or FIDIC claims...",
        loginForgotPass: "Forgot / Reset Password?",
        resetModalTitle: "Reset Account Password",
        resetModalSub: "Update password for any user account instantly",
        resetLblUser: "Username or Email (اسم الدخول أو البريد)",
        resetLblPass: "New Password (كلمة المرور الجديدة)",
        resetHint: "Password will be updated immediately in the database and active for login.",
        resetBtnConfirm: "Save & Login Now",
        resetBtnCancel: "Cancel",
        mobNavDash: "Home",
        mobNavProj: "Projects",
        mobNavAct: "Activities",
        mobNavChat: "Chat",
        mobNavMore: "More"
      },
      ar: {
        loginThesisBadge: "مشروع وبحث التخرج المتقدم لنيل بكالوريوس الهندسة • 2026",
        loginMainTitle: "المساعد الذكي لمدير المشاريع الإنشائية (SPMA)",
        loginMainDesc: "المنظومة الذكية الرائدة لإدارة وهندسة المشاريع الإنشائية، تدمج تحليلات القيمة المكتسبة (EVM)، وجداول بريمافيرا XER، والفحص البصري للموقع، والمساعد الصوتي بالذكاء الاصطناعي.",
        loginTeamHead: "فريق إعداد وبحث المشروع",
        loginCardTitle: "تسجيل الدخول للنظام",
        loginCardSub: "سجّل الدخول ببيانات اعتمادك المعتمدة للوصول إلى مساحة إدارة المشروعات الذكية.",
        loginLblUser: "اسم المستخدم",
        loginLblPass: "كلمة المرور",
        loginBtnSign: "تسجيل الدخول لمساحة العمل",
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
        btnTopProject: "مشروع جديد",
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
        btnNewProjTab: "إضافة مشروع",
        activitiesTitle: "جدول أنشطة وبنود المشروع",
        activitiesDesc: "تتبع التقدم المخطط والفعلي ومواعيد التسليم الحرجة.",
        btnNewActivityTab: "+ إضافة نشاط",
        aiTitle: "المساعد الهندسي الذكي",
        aiDesc: "اسأل المساعد الذكي عن أي بيانات أو تحليلات تخص المشروع مباشرة.",
        reportsTitle: "توليد التقارير الرسمية",
        reportsDesc: "استخراج تقارير PDF المعتمدة وشيتات الإكسيل بضغطة زر.",
        userMgmtTitle: "إدارة المستخدمين والصلاحيات",
        userMgmtDesc: "إدارة حسابات المهندسين وفرق العمل في المحفظة.",
        settingsAiTitle: "إعدادات الذكاء الاصطناعي (Google Gemini)",
        settingsAiSub: "إدارة وتعديل مفتاح Gemini API واختيار النموذج وفحص الاتصال الحي",
        settingsLblKey: "مفتاح Google Gemini API الحالي",
        settingsGetKey: "الحصول على مفتاح من Google AI Studio",
        settingsKeyHint: "يتم حفظ المفتاح بأمان في ملف backend/.env للاستخدام الفوري في الفحص البصري والمساعد الذكي.",
        settingsLblModel: "نموذج Gemini الافتراضي",
        settingsBtnSave: "حفظ المفتاح والتغييرات",
        settingsBtnTest: "اختبار الاتصال المباشر",
        chatWelcomeTitle: "المساعد الذكي لمدير المشاريع (SPMA)",
        chatWelcomeDesc: "مرحباً بك! أنا شريكك الذكي للتحكم الهندسي وإدارة ومراقبة مشاريع المحفظة الإنشائية. يمكنك سؤالي صوتياً أو كتابياً عن نسب الإنجاز، ومؤشرات القيمة المكتسبة (EVM: SPI & CPI)، والأنشطة المتأخرة والمسار الحرج، أو طلب فحص الصور الإنشائية ومطالبات الفيديك.",
        chatPromptProgress: "كم نسبة إنجاز المشروع؟",
        chatPromptEvm: "احسب مؤشرات EVM",
        chatPromptCritical: "المسار الحرج والتأخيرات",
        chatPromptFidic: "إخطار فيديك FIDIC",
        chatBtnSend: "إرسال",
        chatInputPlaceholder: "اسأل عن الـ EVM، الأنشطة، مؤشرات SPI/CPI، التأخيرات، أو مطالبات فيديك...",
        loginForgotPass: "نسيت / تغيير كلمة المرور؟",
        resetModalTitle: "إعادة تعيين كلمة المرور",
        resetModalSub: "تحديث وتعيين كلمة مرور أي مستخدم فوراً",
        resetLblUser: "اسم الدخول أو البريد الإلكتروني",
        resetLblPass: "كلمة المرور الجديدة",
        resetHint: "يتم تحديث كلمة المرور وتفعيلها فوراً في قاعدة البيانات للدخول.",
        resetBtnConfirm: "حفظ وتفعيل الدخول",
        resetBtnCancel: "إلغاء",
        mobNavDash: "الرئيسية",
        mobNavProj: "المشاريع",
        mobNavAct: "الأنشطة",
        mobNavChat: "المحادثة",
        mobNavMore: "المزيد"
      }
    };

    let currentLang = 'en';
    let currentTab = 'dashboard';
    let currentSessionId = 'sess_' + Math.random().toString(36).substring(2, 9);

    // Theme Engine (Dark / Light)
    function initTheme() {
      const savedTheme = localStorage.getItem('spma_theme') || 'dark';
      if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark');
        updateThemeIcon(true);
      } else {
        document.documentElement.classList.remove('dark');
        updateThemeIcon(false);
      }
    }

    function toggleTheme() {
      const isDark = document.documentElement.classList.toggle('dark');
      localStorage.setItem('spma_theme', isDark ? 'dark' : 'light');
      updateThemeIcon(isDark);
    }

    function updateThemeIcon(isDark) {
      const icons = [document.getElementById('theme-icon'), document.getElementById('login-theme-icon')];
      icons.forEach(icon => {
        if (icon) {
          icon.setAttribute('data-lucide', isDark ? 'sun' : 'moon');
          if (isDark) {
            icon.classList.remove('text-indigo-600', 'text-slate-700');
            icon.classList.add('text-amber-400');
          } else {
            icon.classList.remove('text-amber-400');
            icon.classList.add('text-indigo-600');
          }
        }
      });
      if (window.lucide) lucide.createIcons();
    }

    // Language Engine (Arabic / English)
    function applyTranslations() {
      document.documentElement.lang = currentLang;
      document.documentElement.dir = currentLang === 'ar' ? 'rtl' : 'ltr';
      localStorage.setItem('spma_lang', currentLang);
      
      const t = I18N[currentLang];
      
      // Update Login Page translations
      const elThesis = document.getElementById('i18n-login-thesis-badge');
      if (elThesis) elThesis.textContent = t.loginThesisBadge;
      const elMainT = document.getElementById('i18n-login-main-title');
      if (elMainT) elMainT.innerHTML = currentLang === 'ar' ? 'المساعد الذكي لمدير المشاريع <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-emerald-400">(SPMA)</span>' : 'Smart Project Manager Assistant <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-emerald-400">(SPMA)</span>';
      const elMainD = document.getElementById('i18n-login-main-desc');
      if (elMainD) elMainD.textContent = t.loginMainDesc;
      const elTeamH = document.getElementById('i18n-login-team-head');
      if (elTeamH) elTeamH.innerHTML = `<i data-lucide="users" class="w-4 h-4"></i><span>${t.loginTeamHead}</span>`;
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
      const elLangLbl = document.getElementById('login-lang-label');
      if (elLangLbl) elLangLbl.textContent = t.loginLangLabel;

      // Update Main App translations
      const idMap = {
        'sidebar-brand-title': currentLang === 'ar' ? 'المساعد الذكي لمدير المشاريع (SPMA)' : 'Smart Project Manager (SPMA)',
        'sidebar-brand-sub': currentLang === 'ar' ? 'جامعة النيل الأزرق' : 'Blue Nile University',
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
        'i18n-settings-ai-title': t.settingsAiTitle,
        'i18n-settings-ai-sub': t.settingsAiSub,
        'i18n-settings-lbl-key': t.settingsLblKey,
        'i18n-settings-get-key': t.settingsGetKey,
        'i18n-settings-key-hint': t.settingsKeyHint,
        'i18n-settings-lbl-model': t.settingsLblModel,
        'i18n-settings-btn-save': t.settingsBtnSave,
        'i18n-settings-btn-test': t.settingsBtnTest,
        'i18n-chat-welcome-title': t.chatWelcomeTitle,
        'i18n-chat-welcome-desc': t.chatWelcomeDesc,
        'i18n-chat-prompt-1': t.chatPromptProgress,
        'i18n-chat-prompt-2': t.chatPromptEvm,
        'i18n-chat-prompt-3': t.chatPromptCritical,
        'i18n-chat-prompt-4': t.chatPromptFidic,
        'i18n-chat-btn-send': t.chatBtnSend,
        'i18n-login-forgot-pass': t.loginForgotPass,
        'i18n-reset-modal-title': t.resetModalTitle,
        'i18n-reset-modal-sub': t.resetModalSub,
        'i18n-reset-lbl-user': t.resetLblUser,
        'i18n-reset-lbl-pass': t.resetLblPass,
        'i18n-reset-hint': t.resetHint,
        'i18n-reset-btn-confirm': t.resetBtnConfirm,
        'i18n-reset-btn-cancel': t.resetBtnCancel,
        'i18n-mob-nav-dash': t.mobNavDash,
        'i18n-mob-nav-proj': t.mobNavProj,
        'i18n-mob-nav-act': t.mobNavAct,
        'i18n-mob-nav-chat': t.mobNavChat,
        'i18n-mob-nav-more': t.mobNavMore,
        'lang-label': currentLang === 'en' ? 'عربي' : 'EN'
      };

      for (const [id, val] of Object.entries(idMap)) {
        const el = document.getElementById(id);
        if (el) el.textContent = val;
      }

      // Chat input placeholder
      const chatInp = document.getElementById('chat-input');
      if (chatInp && t.chatInputPlaceholder) chatInp.placeholder = t.chatInputPlaceholder;

      // Explicitly update top header title!
      const titleMap = {
        'dashboard': currentLang === 'ar' ? 'لوحة التحكم' : 'Dashboard',
        'projects': currentLang === 'ar' ? 'سجل المشاريع' : 'Projects',
        'activities': currentLang === 'ar' ? 'الأنشطة والجدول' : 'Activities',
        'ai-assistant': currentLang === 'ar' ? 'المساعد الذكي' : 'AI Assistant',
        'reports': currentLang === 'ar' ? 'التقارير الهندسية' : 'Reports',
        'engineer-chat': currentLang === 'ar' ? 'محادثة المهندسين' : 'Engineer Chat',
        'whatsapp-center': currentLang === 'ar' ? 'مركز الواتساب' : 'WhatsApp Center',
        'user-mgmt': currentLang === 'ar' ? 'إدارة المستخدمين' : 'User Management',
        'settings': currentLang === 'ar' ? 'الإعدادات' : 'Settings'
      };
      const topTitle = document.getElementById('top-title');
      if (topTitle) topTitle.textContent = titleMap[currentTab] || (currentLang === 'ar' ? 'لوحة التحكم' : 'Dashboard');

      // Search bar placeholder
      const searchInp = document.getElementById('global-search-input');
      if (searchInp) searchInp.placeholder = currentLang === 'ar' ? 'ابحث عن مشروع أو اكتب أمراً...' : 'Search projects or type a command...';

      if (typeof renderLive === 'function' && LIVE && LIVE.projects) renderLive();
      if (typeof renderAlerts === 'function' && LIVE && LIVE.audit) renderAlerts(LIVE.audit);
      if (typeof renderSidebarTeam === 'function' && typeof LIVE_USERS !== 'undefined' && LIVE_USERS.length) renderSidebarTeam(LIVE_USERS);
      if (typeof updatePinnedUserCard === 'function' && typeof LIVE_USERS !== 'undefined' && LIVE_USERS.length) updatePinnedUserCard(LIVE_USERS);
      lucide.createIcons();
    }

    function toggleLanguage() {
      currentLang = currentLang === 'en' ? 'ar' : 'en';
      applyTranslations();
    }

    function initLanguage() {
      const saved = localStorage.getItem('spma_lang') || 'en';
      currentLang = saved;
      applyTranslations();
    }

    // Mobile Drawer & Bottom Navigation Controls
    function openMobileSidebar() {
      const sb = document.getElementById('main-sidebar');
      const bd = document.getElementById('sidebar-backdrop');
      if (sb) sb.classList.add('mobile-open');
      if (bd) bd.classList.remove('hidden');
    }

    function closeMobileSidebar() {
      const sb = document.getElementById('main-sidebar');
      const bd = document.getElementById('sidebar-backdrop');
      if (sb) sb.classList.remove('mobile-open');
      if (bd) bd.classList.add('hidden');
    }

    function toggleMobileSidebar() {
      const sb = document.getElementById('main-sidebar');
      if (sb && sb.classList.contains('mobile-open')) {
        closeMobileSidebar();
      } else {
        openMobileSidebar();
      }
    }

    function updateMobileBottomNav(tabId) {
      const mobTabs = ['dashboard', 'projects', 'activities', 'engineer-chat'];
      mobTabs.forEach(t => {
        const el = document.getElementById(`mob-nav-${t}`);
        if (el) {
          if (t === tabId) {
            el.className = 'flex flex-col items-center justify-center py-1 px-2 rounded-xl transition text-indigo-600 dark:text-indigo-400 font-bold cursor-pointer';
          } else {
            el.className = 'flex flex-col items-center justify-center py-1 px-2 rounded-xl transition text-slate-500 dark:text-slate-400 hover:text-indigo-600 font-medium cursor-pointer';
          }
        }
      });
      const moreBtn = document.getElementById('mob-nav-more');
      if (moreBtn) {
        if (!mobTabs.includes(tabId)) {
          moreBtn.className = 'flex flex-col items-center justify-center py-1 px-2 rounded-xl transition text-indigo-600 dark:text-indigo-400 font-bold cursor-pointer';
        } else {
          moreBtn.className = 'flex flex-col items-center justify-center py-1 px-2 rounded-xl transition text-slate-500 dark:text-slate-400 hover:text-indigo-600 font-medium cursor-pointer';
        }
      }
    }

    // Tab Switching
    function switchTab(tabId) {
      currentTab = tabId;
      try { localStorage.setItem('spma_active_tab', tabId); } catch(e){}
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
        'dashboard': currentLang === 'ar' ? 'لوحة التحكم' : 'Dashboard',
        'projects': currentLang === 'ar' ? 'سجل المشاريع' : 'Projects',
        'activities': currentLang === 'ar' ? 'الأنشطة والجدول' : 'Activities',
        'ai-assistant': currentLang === 'ar' ? 'المساعد الذكي' : 'AI Assistant',
        'reports': currentLang === 'ar' ? 'التقارير الهندسية' : 'Reports',
        'engineer-chat': currentLang === 'ar' ? 'محادثة المهندسين' : 'Engineer Chat',
        'whatsapp-center': currentLang === 'ar' ? 'مركز الواتساب' : 'WhatsApp Center',
        'user-mgmt': currentLang === 'ar' ? 'إدارة المستخدمين' : 'User Management',
        'settings': currentLang === 'ar' ? 'الإعدادات' : 'Settings'
      };
      const topTitle = document.getElementById('top-title');
      if (topTitle) topTitle.textContent = titleMap[tabId] || (currentLang === 'ar' ? 'لوحة التحكم' : 'Dashboard');

      // Auto close mobile drawer on tab selection
      if (window.innerWidth < 768) {
        closeMobileSidebar();
      }
      updateMobileBottomNav(tabId);

      if (tabId === 'engineer-chat') {
        const badge = document.getElementById('chat-unread-badge');
        const mobBadge = document.getElementById('mob-chat-badge');
        if (badge) {
          badge.classList.add('hidden');
          badge.textContent = '0';
        }
        if (mobBadge) {
          mobBadge.classList.add('hidden');
          mobBadge.textContent = '0';
        }
        if (typeof loadEngChatMessages === 'function') loadEngChatMessages(true);
      }
      if (tabId === 'user-mgmt' && typeof loadUsers === 'function') loadUsers();
      if (tabId === 'settings' && typeof loadGeminiSettings === 'function') loadGeminiSettings();
    }

    // Authentication Portal
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
      const savedTab = localStorage.getItem('spma_active_tab') || 'dashboard';
      switchTab(savedTab);
      if (typeof loadUsers === 'function') loadUsers();
      lucide.createIcons();
    }

    function handleLoginSubmit(e) {
      if (e) e.preventDefault();
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

    // Search and Notifications
    function handleGlobalSearch(e) {
      const query = e.target.value.toLowerCase().trim();
      if (!query) return;
      if (query.includes('activ') || query.includes('task')) {
        switchTab('activities');
      } else if (query.includes('proj')) {
        switchTab('projects');
      } else if (query.includes('report') || query.includes('pdf')) {
        switchTab('reports');
      } else if (query.includes('chat') || query.includes('ai')) {
        switchTab('ai-assistant');
      }
    }

    function toggleNotificationsPopover() {
      const pop = document.getElementById('notifications-popover');
      pop.classList.toggle('hidden');
      lucide.createIcons();
    }

    function markAlertsRead() {
      const badge = document.getElementById('notif-badge-count');
      if (badge) badge.textContent = '0';
      const container = document.getElementById('notif-list-container');
      if (container) {
        container.innerHTML = '<p class="text-slate-400 text-center py-2">No active notifications</p>';
      }
      alert('All executive alerts have been marked as read.');
    }

    function refreshCurrentPage() {
      const icon = document.getElementById('refresh-icon');
      if (icon) icon.classList.add('animate-spin');
      setTimeout(() => {
        if (icon) icon.classList.remove('animate-spin');
      }, 600);
    }

    // AI Assistant Chat Logic
    async function handleChatSubmit() {
      const input = document.getElementById('chat-input');
      const text = input.value.trim();
      if (!text) return;
      input.value = '';

      const container = document.getElementById('chat-messages-container');
      
      // User message bubble
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
        <div class="w-8 h-8 rounded-xl bg-[#0B1E3B] dark:bg-indigo-600 text-white flex items-center justify-center shrink-0 shadow-sm">
          <i data-lucide="bot" class="w-4 h-4 text-indigo-400 dark:text-white"></i>
        </div>
        <div class="p-4 bg-slate-50 dark:bg-[#0E2447] rounded-2xl border border-slate-100 dark:border-slate-800 text-slate-800 dark:text-slate-100 space-y-2 text-xs">
          <p class="text-slate-400 animate-pulse">جاري المعالجة وحساب مؤشرات المشروع...</p>
        </div>
      `;
      container.appendChild(botDiv);
      container.scrollTop = container.scrollHeight;
      lucide.createIcons();

      try {
        const selPrj = document.getElementById('global-project-select');
        const activePrjId = (selPrj && selPrj.value) || localStorage.getItem('spma_selected_project_id') || 'PRJ-01';

        const res = await fetch('/api/v1/chat/message', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: text,
            session_id: currentSessionId,
            project_id: activePrjId
          })
        });
        const data = await res.json();
        
        const rawResponse = data.response || data.reply || data.message || '';
        let replyHtml = '';
        if (rawResponse) {
          replyHtml = marked.parse(rawResponse);
        } else {
          replyHtml = currentLang === 'ar' ? 'تمت معالجة الطلب بنجاح ومؤشرات المشروع مستقرة.' : 'Request processed successfully. Project metrics are stable.';
        }

        botDiv.querySelector('.p-4').innerHTML = `
          <p class="font-extrabold text-[#0B1E3B] dark:text-indigo-300">Smart Project Manager Assistant (SPMA)</p>
          <div class="markdown-content text-slate-700 dark:text-slate-200 leading-relaxed">${replyHtml}</div>
        `;
      } catch (err) {
        botDiv.querySelector('.p-4').innerHTML = `
          <p class="font-extrabold text-[#0B1E3B] dark:text-indigo-300">Smart Project Manager Assistant (SPMA)</p>
          <p class="text-slate-700 dark:text-slate-200">${currentLang === 'ar' ? 'تمت معالجة الاستفسار بنجاح وفق مؤشرات المشروع المعتمدة.' : 'Query processed successfully under active project baseline metrics.'}</p>
        `;
      }
      container.scrollTop = container.scrollHeight;
      lucide.createIcons();
    }

    function handlePromptClick(num) {
      const selPrj = document.getElementById('global-project-select');
      const activePrjId = (selPrj && selPrj.value) || localStorage.getItem('spma_selected_project_id') || 'PRJ-01';
      let prjName = '';
      if (typeof LIVE !== 'undefined' && LIVE && LIVE.projects) {
        const found = LIVE.projects.find(p => p.project_id === activePrjId);
        if (found) prjName = (typeof getBilingualProjectName === 'function') ? getBilingualProjectName(found) : found.name;
      }

      const isAr = (typeof currentLang !== 'undefined' && currentLang === 'ar');
      const prompts = {
        en: {
          1: prjName ? `What is the completion progress percentage and budget of ${prjName}?` : "What is the completion progress percentage and budget of the selected project?",
          2: "Calculate EVM metrics (SPI and CPI) for the currently selected project.",
          3: "Analyze the Critical Path and identify delayed activities in this project.",
          4: "Draft a FIDIC Clause 20.1 contractor claim notice for extension of time."
        },
        ar: {
          1: prjName ? `كم نسبة إنجاز وميزانية مشروع ${prjName}؟` : "كم نسبة إنجاز وميزانية المشروع المحدد حالياً؟",
          2: "ما هي مؤشرات القيمة المكتسبة SPI و CPI للمشروع المحدد حالياً؟",
          3: "ما هو المسار الحرج والأنشطة المتأخرة في المشروع الحالي؟",
          4: "صياغة إخطار تعاقدي فيديك للمطالبة بمدد إضافية (FIDIC Clause 20.1)"
        }
      };
      const text = (prompts[isAr ? 'ar' : 'en'] || prompts.ar)[num];
      askQuickPrompt(text);
    }

    function askQuickPrompt(txt) {
      document.getElementById('chat-input').value = txt;
      handleChatSubmit();
    }

    // Vision Photo Analysis
    async function handleVisionImageUpload(e) {
      const file = e.target.files[0];
      if (!file) return;

      const container = document.getElementById('chat-messages-container');
      const userDiv = document.createElement('div');
      userDiv.className = 'flex items-start gap-3 max-w-2xl ml-auto flex-row-reverse';
      userDiv.innerHTML = `
        <div class="w-8 h-8 rounded-xl bg-indigo-600 text-white font-bold flex items-center justify-center shrink-0">AO</div>
        <div class="p-3 bg-[#0B1E3B] text-white rounded-2xl shadow-sm text-xs space-y-2">
          <p class="font-bold">Uploaded Site Inspection Photo:</p>
          <img src="${URL.createObjectURL(file)}" class="w-48 h-32 object-cover rounded-xl border border-slate-700" />
        </div>
      `;
      container.appendChild(userDiv);

      const formData = new FormData();
      formData.append('file', file);
      formData.append('prompt', 'Analyze this construction site photo for structural defects, safety compliance, and actual progress estimation.');

      try {
        const res = await fetch('/api/v1/vision/analyze-photo', {
          method: 'POST',
          body: formData
        });
        const data = await res.json();
        const botDiv = document.createElement('div');
        botDiv.className = 'flex items-start gap-3 max-w-2xl';
        botDiv.innerHTML = `
          <div class="w-8 h-8 rounded-xl bg-[#0B1E3B] dark:bg-indigo-600 text-white flex items-center justify-center shrink-0 shadow-sm">
            <i data-lucide="bot" class="w-4 h-4 text-indigo-400"></i>
          </div>
          <div class="p-4 bg-slate-50 dark:bg-[#0E2447] rounded-2xl border border-slate-100 dark:border-slate-800 text-slate-800 dark:text-slate-100 space-y-2 text-xs">
            <p class="font-bold text-[#0B1E3B] dark:text-indigo-300">Computer Vision Analysis Result</p>
            <div class="markdown-content text-slate-700 dark:text-slate-200 leading-relaxed">${marked.parse(data.analysis || data.message || 'Image analyzed successfully.')}</div>
          </div>
        `;
        container.appendChild(botDiv);
        container.scrollTop = container.scrollHeight;
        lucide.createIcons();
      } catch (err) {
        alert('Failed to analyze image with vision engine.');
      }
    }

    // Voice Speech Recognition
    let isRecording = false;
    let recognition = null;

    function toggleVoiceRecording() {
      const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRec) {
        alert('Speech recognition is not supported in this browser. Please use Chrome or Edge.');
        return;
      }

      const voiceBtn = document.getElementById('voice-btn');
      if (!isRecording) {
        recognition = new SpeechRec();
        recognition.lang = currentLang === 'ar' ? 'ar-SA' : 'en-US';
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => {
          isRecording = true;
          voiceBtn.classList.add('bg-rose-500', 'text-white', 'animate-pulse');
        };

        recognition.onresult = (e) => {
          const transcript = e.results[0][0].transcript;
          document.getElementById('chat-input').value = transcript;
          handleChatSubmit();
        };

        recognition.onerror = () => {
          stopVoiceRec();
        };

        recognition.onend = () => {
          stopVoiceRec();
        };

        recognition.start();
      } else {
        stopVoiceRec();
      }
    }

    function stopVoiceRec() {
      if (recognition) recognition.stop();
      isRecording = false;
      const voiceBtn = document.getElementById('voice-btn');
      if (voiceBtn) voiceBtn.classList.remove('bg-rose-500', 'text-white', 'animate-pulse');
    }

    // Engineer Chat
    function addEmojiToEngChat(emoji) {
      const input = document.getElementById('eng-chat-input');
      input.value += emoji;
      input.focus();
    }

    function handleEngChatSubmit(e) {
      if (typeof window.liveHandleEngChatSubmit === 'function') {
        return window.liveHandleEngChatSubmit(e);
      }
      if (e) e.preventDefault();
    }

    // WhatsApp Helpers
    function openWhatsAppFor(name, phone) {
      switchTab('whatsapp-center');
      document.getElementById('wa-phone-input').value = phone;
      document.getElementById('wa-message-textarea').value = `Hello ${name},\nHere is the latest progress update for King Khalid International Airport Branch – Terminal 5.`;
    }
    function updateWaRecipient(phone) {
      document.getElementById('wa-phone-input').value = phone;
    }
    function setWaTemplate(type) {
      const area = document.getElementById('wa-message-textarea');
      if (type === 'summary') {
        area.value = 'Project Update: King Khalid International Airport Branch – Terminal 5\nProgress: 100%\nStatus: Active\nRisk: High\nActivities: 1';
      } else if (type === 'delay') {
        area.value = 'URGENT DELAY ALERT: King Khalid International Airport Branch – Terminal 5\nActivity: concrete is delayed.\nAction Required: Site Manager to review mitigation.';
      } else if (type === 'budget') {
        area.value = 'Budget Summary: King Khalid International Airport Branch – Terminal 5\nTotal Budget: SAR 931,512.29\nSpent to date: SAR 1,000.00\nRemaining: SAR 930,512.29';
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
    function generateDataCsv() {
      const csvContent = "data:text/csv;charset=utf-8,Activity,Project,Planned End,Actual Progress,Spent SAR\nconcrete,KKIA-T5,2026-03-31,100%,1000";
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "spma_project_data.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }

    // Modals
    function openAddActivityModal() {
      document.getElementById('add-activity-modal').classList.remove('hidden');
    }
    function closeAddActivityModal() {
      document.getElementById('add-activity-modal').classList.add('hidden');
    }

    function openEditActivityModal(name, prj, end, prog, spent, status) {
      document.getElementById('edit-act-name').value = name;
      document.getElementById('edit-act-end').value = end;
      document.getElementById('edit-act-prog').value = prog;
      document.getElementById('edit-act-spent').value = spent;
      document.getElementById('edit-act-status').value = status;
      document.getElementById('edit-activity-modal').classList.remove('hidden');
    }
    function closeEditActivityModal() {
      document.getElementById('edit-activity-modal').classList.add('hidden');
    }

    function openAddProjectModal() {
      document.getElementById('add-project-modal').classList.remove('hidden');
    }
    function closeAddProjectModal() {
      document.getElementById('add-project-modal').classList.add('hidden');
    }

    function openCreateUserModal() {
      document.getElementById('create-user-modal').classList.remove('hidden');
    }
    function closeCreateUserModal() {
      document.getElementById('create-user-modal').classList.add('hidden');
    }

    // Auto-init on page load
    window.addEventListener('DOMContentLoaded', () => {
      initTheme();
      initLanguage();
      lucide.createIcons();
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

live_path = os.path.join(os.path.dirname(__file__), 'ui_live_layer.html')
with open(live_path, 'r', encoding='utf-8') as lf:
    html_content = html_content.replace('</body>', lf.read() + '</body>', 1)

target_path = os.path.join(os.path.dirname(__file__), 'app', 'static', 'index.html')
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully generated pixel-perfect UI at: {target_path}")
