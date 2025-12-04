import { useState } from 'react';
import type { Student, GradeFormData } from '../../types';
import { calculateAverage, formatDate, validateGrade } from '../../utils/helpers';
import { useStudents } from '../../contexts/StudentsContext';

interface StudentCardProps {
  student: Student;
  onEdit: () => void;
}

export function StudentCard({ student, onEdit }: StudentCardProps) {
  const { deleteStudent, addGrade, deleteGrade, updateGrade } = useStudents();
  const [showGradeForm, setShowGradeForm] = useState(false);
  const [editingGradeId, setEditingGradeId] = useState<string | null>(null);
  const [gradeFormData, setGradeFormData] = useState<GradeFormData>({
    subject: '',
    grade: 0,
  });
  const [gradeError, setGradeError] = useState('');

  const average = calculateAverage(student.grades.map(g => g.grade));

  const getAverageColor = (avg: number) => {
    if (avg >= 7) return 'text-emerald-600';
    if (avg >= 5) return 'text-amber-600';
    return 'text-red-600';
  };

  const handleDeleteStudent = () => {
    if (window.confirm(`Tem certeza que deseja excluir o aluno ${student.name}?`)) {
      deleteStudent(student.id);
    }
  };

  const handleGradeSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!gradeFormData.subject.trim()) {
      setGradeError('Disciplina é obrigatória');
      return;
    }
    
    if (!validateGrade(gradeFormData.grade)) {
      setGradeError('Nota deve estar entre 0 e 10');
      return;
    }

    if (editingGradeId) {
      updateGrade(student.id, editingGradeId, gradeFormData);
      setEditingGradeId(null);
    } else {
      addGrade(student.id, gradeFormData);
    }
    
    setGradeFormData({ subject: '', grade: 0 });
    setShowGradeForm(false);
    setGradeError('');
  };

  const handleEditGrade = (gradeId: string, subject: string, grade: number) => {
    setEditingGradeId(gradeId);
    setGradeFormData({ subject, grade });
    setShowGradeForm(true);
  };

  const handleCancelGradeForm = () => {
    setShowGradeForm(false);
    setEditingGradeId(null);
    setGradeFormData({ subject: '', grade: 0 });
    setGradeError('');
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 hover:shadow-lg hover:border-slate-300 transition-all group">
      {/* Header do Card */}
      <div className="flex justify-between items-start mb-4">
        <div className="flex items-start gap-3 flex-1 min-w-0">
          <div className="w-10 h-10 bg-gradient-to-br from-teal-500 to-emerald-600 rounded-lg flex items-center justify-center flex-shrink-0 shadow-md">
            <span className="text-white font-bold text-sm">{student.name.charAt(0).toUpperCase()}</span>
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-base font-semibold text-slate-900 truncate">{student.name}</h3>
            <p className="text-sm text-slate-500 truncate">{student.email}</p>
            <div className="flex items-center gap-2 mt-1">
              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-600">
                #{student.registrationNumber}
              </span>
            </div>
          </div>
        </div>
        <div className="flex gap-1 ml-3 opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            onClick={onEdit}
            className="p-1.5 text-slate-400 hover:text-teal-600 hover:bg-teal-50 rounded-md transition-colors"
            title="Editar"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
            </svg>
          </button>
          <button
            onClick={handleDeleteStudent}
            className="p-1.5 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors"
            title="Excluir"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>

      {/* Média com barra de progresso */}
      <div className="bg-gradient-to-br from-slate-50 to-slate-100 rounded-lg p-3 mb-4 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-teal-500/5 to-emerald-500/5"></div>
        <div className="relative flex justify-between items-center">
          <div>
            <span className="text-xs font-medium text-slate-600 uppercase tracking-wider">Média</span>
            <div className="flex items-baseline gap-1 mt-1">
              <span className={`text-2xl font-bold ${getAverageColor(average)}`}>
                {average.toFixed(1)}
              </span>
              <span className="text-xs text-slate-400">/10</span>
            </div>
          </div>
          <div className="w-16 h-16 relative">
            <svg className="w-16 h-16 transform -rotate-90">
              <circle
                cx="32"
                cy="32"
                r="28"
                stroke="currentColor"
                strokeWidth="6"
                fill="none"
                className="text-slate-200"
              />
              <circle
                cx="32"
                cy="32"
                r="28"
                stroke="currentColor"
                strokeWidth="6"
                fill="none"
                strokeDasharray={`${(average / 10) * 176} 176`}
                className={average >= 7 ? 'text-emerald-500' : average >= 5 ? 'text-amber-500' : 'text-red-500'}
                strokeLinecap="round"
              />
            </svg>
          </div>
        </div>
      </div>

      {/* Lista de Notas */}
      <div>
        <div className="flex justify-between items-center mb-3">
          <h4 className="text-xs font-semibold text-slate-700 uppercase tracking-wider">Notas</h4>
          <button
            onClick={() => setShowGradeForm(!showGradeForm)}
            className="text-xs text-teal-600 hover:text-teal-700 font-medium flex items-center gap-1"
          >
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Adicionar
          </button>
        </div>

        {/* Formulário de Nota */}
        {showGradeForm && (
          <form onSubmit={handleGradeSubmit} className="bg-teal-50 rounded-lg p-3 mb-3 space-y-2">
            <input
              type="text"
              value={gradeFormData.subject}
              onChange={(e) => setGradeFormData({ ...gradeFormData, subject: e.target.value })}
              placeholder="Disciplina"
              className="w-full px-3 py-2 text-sm border border-teal-200 rounded-md focus:ring-1 focus:ring-teal-500 focus:border-teal-500 outline-none bg-white"
            />
            <input
              type="number"
              step="0.1"
              min="0"
              max="10"
              value={gradeFormData.grade}
              onChange={(e) => setGradeFormData({ ...gradeFormData, grade: parseFloat(e.target.value) || 0 })}
              placeholder="Nota (0-10)"
              className="w-full px-3 py-2 text-sm border border-teal-200 rounded-md focus:ring-1 focus:ring-teal-500 focus:border-teal-500 outline-none bg-white"
            />
            {gradeError && <p className="text-red-600 text-xs">{gradeError}</p>}
            <div className="flex gap-2 pt-1">
              <button
                type="submit"
                className="flex-1 bg-teal-600 hover:bg-teal-700 text-white text-xs font-medium py-2 rounded-md transition-colors"
              >
                {editingGradeId ? 'Atualizar' : 'Salvar'}
              </button>
              <button
                type="button"
                onClick={handleCancelGradeForm}
                className="flex-1 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-medium py-2 rounded-md transition-colors"
              >
                Cancelar
              </button>
            </div>
          </form>
        )}

        {/* Lista de Notas */}
        {student.grades.length === 0 ? (
          <p className="text-xs text-slate-400 text-center py-6">Sem notas</p>
        ) : (
          <div className="space-y-2">
            {student.grades.map((grade) => (
              <div
                key={grade.id}
                className="flex justify-between items-center bg-slate-50 rounded-lg p-2.5 group hover:bg-slate-100 transition-colors"
              >
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-sm text-slate-900 truncate">{grade.subject}</p>
                  <p className="text-xs text-slate-400">{formatDate(grade.date)}</p>
                </div>
                <div className="flex items-center gap-2 ml-2">
                  <span className={`text-base font-bold ${getAverageColor(grade.grade)} min-w-[2.5rem] text-right`}>
                    {grade.grade.toFixed(1)}
                  </span>
                  <div className="flex gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={() => handleEditGrade(grade.id, grade.subject, grade.grade)}
                      className="p-1 text-slate-400 hover:text-teal-600 hover:bg-teal-50 rounded transition-colors"
                      title="Editar"
                    >
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                      </svg>
                    </button>
                    <button
                      onClick={() => {
                        if (window.confirm('Deseja excluir esta nota?')) {
                          deleteGrade(student.id, grade.id);
                        }
                      }}
                      className="p-1 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
                      title="Excluir"
                    >
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
