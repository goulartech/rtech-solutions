export interface Grade {
  id: string;
  subject: string;
  grade: number;
  date: string;
}

export interface Student {
  id: string;
  name: string;
  email: string;
  registrationNumber: string;
  grades: Grade[];
  createdAt: string;
}

export interface StudentFormData {
  name: string;
  email: string;
  registrationNumber: string;
}

export interface GradeFormData {
  subject: string;
  grade: number;
}
