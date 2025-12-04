import { StudentsProvider } from './contexts/StudentsContext';
import { StudentList } from './components/StudentList';

function App() {
  return (
    <StudentsProvider>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-teal-50/30 to-slate-50">
        {/* Header com gradiente */}
        <header className="bg-white border-b border-slate-200 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-teal-600/5 via-emerald-600/5 to-teal-600/5"></div>
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 relative">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-gradient-to-br from-teal-600 to-emerald-600 rounded-xl flex items-center justify-center shadow-lg shadow-teal-500/20">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div>
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">Sistema de Notas</h1>
                  <p className="text-sm text-slate-500 mt-0.5">Gestão escolar simplificada</p>
                </div>
              </div>
              <div className="hidden sm:flex items-center gap-3 bg-slate-50 px-4 py-2 rounded-lg border border-slate-200">
                <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                <span className="text-sm text-slate-600 font-medium">2025.2</span>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <StudentList />
        </main>
      </div>
    </StudentsProvider>
  );
}

export default App;
