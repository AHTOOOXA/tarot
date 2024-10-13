export interface UserAnswer {
  user_id: number;
  user_name: string;
  answer_text: string;
}

export default interface Question {
  id: number;
  text: string;
  emoji: string;
  answers: UserAnswer[];
}
