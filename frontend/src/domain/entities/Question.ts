export interface UserAnswer {
  user_id: number;
  user_name: string;
  answer_text: string;
}

export default interface Question {
  question_id: number;
  question_text: string;
  answers: UserAnswer[];
}