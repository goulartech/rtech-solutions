import { createContext, useContext, useState, useCallback } from 'react';
import type { ReactNode } from 'react';
import type { Student, StudentFormData, Grade, GradeFormData } from '../types';
import { generateId } from '../utils/helpers';

interface StudentsContextData {
  students: Student[];
  addStudent: (data: StudentFormData) => void;
  updateStudent: (id: string, data: StudentFormData) => void;
  deleteStudent: (id: string) => void;
  addGrade: (studentId: string, data: GradeFormData) => void;
  updateGrade: (studentId: string, gradeId: string, data: GradeFormData) => void;
  deleteGrade: (studentId: string, gradeId: string) => void;
  getStudentById: (id: string) => Student | undefined;
}

const StudentsContext = createContext<StudentsContextData | undefined>(undefined);

// Dados iniciais de exemplo
const initialStudents: Student[] = [
  {
    id: '1',
    name: 'Ana Silva',
    email: 'ana.silva@email.com',
    registrationNumber: '2024001',
    createdAt: new Date().toISOString(),
    grades: [
      { id: '1', subject: 'Matemática', grade: 8.5, date: '2024-03-15' },
      { id: '2', subject: 'Português', grade: 9.0, date: '2024-03-20' },
      { id: '3', subject: 'História', grade: 7.5, date: '2024-03-25' },
    ],
  },
  {
    id: '2',
    name: 'Carlos Oliveira',
    email: 'carlos.oliveira@email.com',
    registrationNumber: '2024002',
    createdAt: new Date().toISOString(),
    grades: [
      { id: '4', subject: 'Matemática', grade: 7.0, date: '2024-03-15' },
      { id: '5', subject: 'Física', grade: 8.0, date: '2024-03-18' },
    ],
  },
];

export function StudentsProvider({ children }: { children: ReactNode }) {
  const [students, setStudents] = useState<Student[]>(initialStudents);

  const addStudent = useCallback((data: StudentFormData) => {
    const newStudent: Student = {
      id: generateId(),
      ...data,
      grades: [],
      createdAt: new Date().toISOString(),
    };
    setStudents(prev => [...prev, newStudent]);
  }, []);

  const updateStudent = useCallback((id: string, data: StudentFormData) => {
    setStudents(prev =>
      prev.map(student =>
        student.id === id ? { ...student, ...data } : student
      )
    );
  }, []);

  const deleteStudent = useCallback((id: string) => {
    setStudents(prev => prev.filter(student => student.id !== id));
  }, []);

  const addGrade = useCallback((studentId: string, data: GradeFormData) => {
    const newGrade: Grade = {
      id: generateId(),
      ...data,
      date: new Date().toISOString().split('T')[0],
    };
    
    setStudents(prev =>
      prev.map(student =>
        student.id === studentId
          ? { ...student, grades: [...student.grades, newGrade] }
          : student
      )
    );
  }, []);

  const updateGrade = useCallback((studentId: string, gradeId: string, data: GradeFormData) => {
    setStudents(prev =>
      prev.map(student =>
        student.id === studentId
          ? {
              ...student,
              grades: student.grades.map(grade =>
                grade.id === gradeId ? { ...grade, ...data } : grade
              ),
            }
          : student
      )
    );
  }, []);

  const deleteGrade = useCallback((studentId: string, gradeId: string) => {
    setStudents(prev =>
      prev.map(student =>
        student.id === studentId
          ? {
              ...student,
              grades: student.grades.filter(grade => grade.id !== gradeId),
            }
          : student
      )
    );
  }, []);

  const getStudentById = useCallback((id: string) => {
    return students.find(student => student.id === id);
  }, [students]);

  return (
    <StudentsContext.Provider
      value={{
        students,
        addStudent,
        updateStudent,
        deleteStudent,
        addGrade,
        updateGrade,
        deleteGrade,
        getStudentById,
      }}
    >
      {children}
    </StudentsContext.Provider>
  );
}

export function useStudents() {
  const context = useContext(StudentsContext);
  if (!context) {
    throw new Error('useStudents must be used within a StudentsProvider');
  }
  return context;
}
