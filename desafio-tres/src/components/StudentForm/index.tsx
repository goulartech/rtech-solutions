import { useState, useEffect } from 'react';
import type { StudentFormData } from '../../types';
import { validateEmail } from '../../utils/helpers';

interface StudentFormProps {
  onSubmit: (data: StudentFormData) => void;
  onCancel: () => void;
  initialData?: StudentFormData;
  isEditing?: boolean;
}

export function StudentForm({ onSubmit, onCancel, initialData, isEditing = false }: StudentFormProps) {
  const [formData, setFormData] = useState<StudentFormData>({
    name: '',
    email: '',
    registrationNumber: '',
  });
  
  const [errors, setErrors] = useState<Partial<StudentFormData>>({});

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
    }
  }, [initialData]);

  const validate = (): boolean => {
    const newErrors: Partial<StudentFormData> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Nome é obrigatório';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email é obrigatório';
    } else if (!validateEmail(formData.email)) {
      newErrors.email = 'Email inválido';
    }

    if (!formData.registrationNumber.trim()) {
      newErrors.registrationNumber = 'Matrícula é obrigatória';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formData);
      setFormData({ name: '', email: '', registrationNumber: '' });
      setErrors({});
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
      <div className="flex items-center gap-3 mb-5 pb-4 border-b border-slate-100">
        <div className="w-10 h-10 bg-gradient-to-br from-teal-500 to-emerald-600 rounded-lg flex items-center justify-center shadow-md">
          <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            {isEditing ? 'Editar Aluno' : 'Novo Aluno'}
          </h2>
          <p className="text-xs text-slate-500">Preencha os dados do aluno</p>
        </div>
      </div>

      <div className="space-y-4">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-slate-700 mb-1.5">
            Nome completo
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <input
              type="text"
              id="name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className={`w-full pl-10 pr-3.5 py-2.5 text-sm border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none transition ${
                errors.name ? 'border-red-300 bg-red-50' : 'border-slate-200 bg-white'
              }`}
              placeholder="Nome do aluno"
            />
          </div>
          {errors.name && <p className="text-red-600 text-xs mt-1.5">{errors.name}</p>}
        </div>

        <div>
          <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-1.5">
            Email
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <input
              type="email"
              id="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className={`w-full pl-10 pr-3.5 py-2.5 text-sm border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none transition ${
                errors.email ? 'border-red-300 bg-red-50' : 'border-slate-200 bg-white'
              }`}
              placeholder="email@exemplo.com"
            />
          </div>
          {errors.email && <p className="text-red-600 text-xs mt-1.5">{errors.email}</p>}
        </div>

        <div>
          <label htmlFor="registrationNumber" className="block text-sm font-medium text-slate-700 mb-1.5">
            Matrícula
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
              </svg>
            </div>
            <input
              type="text"
              id="registrationNumber"
              value={formData.registrationNumber}
              onChange={(e) => setFormData({ ...formData, registrationNumber: e.target.value })}
              className={`w-full pl-10 pr-3.5 py-2.5 text-sm border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none transition ${
                errors.registrationNumber ? 'border-red-300 bg-red-50' : 'border-slate-200 bg-white'
              }`}
              placeholder="2024001"
            />
          </div>
          {errors.registrationNumber && (
            <p className="text-red-600 text-xs mt-1.5">{errors.registrationNumber}</p>
          )}
        </div>
      </div>

      <div className="flex gap-3 mt-6 pt-5 border-t border-slate-100">
        <button
          type="submit"
          className="flex-1 bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white text-sm font-medium py-2.5 rounded-lg transition-all shadow-lg shadow-teal-500/30 hover:shadow-xl hover:shadow-teal-500/40"
        >
          {isEditing ? 'Salvar alterações' : 'Cadastrar aluno'}
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="flex-1 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-sm font-medium py-2.5 rounded-lg transition-colors"
        >
          Cancelar
        </button>
      </div>
    </form>
  );
}
