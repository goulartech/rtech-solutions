import { useState } from 'react';
import { useStudents } from '../../contexts/StudentsContext';
import { StudentCard } from '../StudentCard';
import { StudentForm } from '../StudentForm';
import type { StudentFormData } from '../../types';

export function StudentList() {
  const { students, addStudent, updateStudent } = useStudents();
  const [showForm, setShowForm] = useState(false);
  const [editingStudentId, setEditingStudentId] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  const filteredStudents = students.filter(
    (student) =>
      student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      student.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      student.registrationNumber.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const totalGrades = students.reduce((acc, student) => acc + student.grades.length, 0);
  const averageOfAll = students.length > 0
    ? students.reduce((acc, student) => {
        const studentAvg = student.grades.length > 0
          ? student.grades.reduce((sum, g) => sum + g.grade, 0) / student.grades.length
          : 0;
        return acc + studentAvg;
      }, 0) / students.length
    : 0;

  const handleAddStudent = (data: StudentFormData) => {
    addStudent(data);
    setShowForm(false);
  };

  const handleUpdateStudent = (data: StudentFormData) => {
    if (editingStudentId) {
      updateStudent(editingStudentId, data);
      setEditingStudentId(null);
      setShowForm(false);
    }
  };

  const handleEditStudent = (studentId: string) => {
    setEditingStudentId(studentId);
    setShowForm(true);
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingStudentId(null);
  };

  const editingStudent = editingStudentId
    ? students.find((s) => s.id === editingStudentId)
    : null;

  return (
    <div className="space-y-6">
      {/* Cards de Estatísticas */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl border border-slate-200 p-4 hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-slate-500 uppercase tracking-wider">Total de Alunos</p>
              <p className="text-2xl font-bold text-slate-900 mt-1">{students.length}</p>
            </div>
            <div className="w-12 h-12 bg-teal-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-xl border border-slate-200 p-4 hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-slate-500 uppercase tracking-wider">Notas Lançadas</p>
              <p className="text-2xl font-bold text-slate-900 mt-1">{totalGrades}</p>
            </div>
            <div className="w-12 h-12 bg-cyan-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-cyan-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-xl border border-slate-200 p-4 hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-slate-500 uppercase tracking-wider">Média Geral</p>
              <p className="text-2xl font-bold text-slate-900 mt-1">{averageOfAll.toFixed(1)}</p>
            </div>
            <div className="w-12 h-12 bg-emerald-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      {/* Header e Barra de Busca */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">Alunos</h2>
            <p className="text-slate-500 text-sm mt-0.5">
              {students.length} {students.length === 1 ? 'cadastrado' : 'cadastrados'}
            </p>
          </div>
          <button
            onClick={() => setShowForm(!showForm)}
            className="bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white text-sm font-medium py-2.5 px-5 rounded-lg transition-all flex items-center justify-center gap-2 shadow-lg shadow-teal-500/30 hover:shadow-xl hover:shadow-teal-500/40"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Novo Aluno
          </button>
        </div>

        {/* Barra de Busca */}
        <div className="relative">
          <input
            type="text"
            placeholder="Buscar aluno..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-4 py-2.5 pl-10 text-sm border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition bg-slate-50"
          />
          <svg
            className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 transform -translate-y-1/2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </div>
      </div>

      {/* Formulário */}
      {showForm && (
        <StudentForm
          onSubmit={editingStudentId ? handleUpdateStudent : handleAddStudent}
          onCancel={handleCancelForm}
          initialData={
            editingStudent
              ? {
                  name: editingStudent.name,
                  email: editingStudent.email,
                  registrationNumber: editingStudent.registrationNumber,
                }
              : undefined
          }
          isEditing={!!editingStudentId}
        />
      )}

      {/* Lista de Cards */}
      {filteredStudents.length === 0 ? (
        <div className="bg-gradient-to-br from-white to-slate-50 rounded-xl border-2 border-dashed border-slate-200 p-16 text-center">
          <div className="w-20 h-20 bg-gradient-to-br from-slate-100 to-slate-200 rounded-2xl flex items-center justify-center mx-auto mb-5 shadow-inner">
            <svg
              className="w-10 h-10 text-slate-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
              />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-slate-900 mb-2">
            {searchTerm ? 'Nenhum resultado encontrado' : 'Nenhum aluno cadastrado'}
          </h3>
          <p className="text-sm text-slate-500 mb-6">
            {searchTerm
              ? 'Tente ajustar os termos da sua busca'
              : 'Comece adicionando um novo aluno ao sistema'}
          </p>
          {!searchTerm && (
            <button
              onClick={() => setShowForm(true)}
              className="inline-flex items-center gap-2 bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white text-sm font-medium py-2.5 px-6 rounded-lg transition-all shadow-lg shadow-teal-500/30"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              Adicionar Primeiro Aluno
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-5">
          {filteredStudents.map((student) => (
            <StudentCard
              key={student.id}
              student={student}
              onEdit={() => handleEditStudent(student.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
