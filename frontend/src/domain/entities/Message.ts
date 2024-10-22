import type User from "./User";
import type Question from "./Question";

export default interface Message {
  question: Question;
  taker: User;
  created_at: string; // ISO 8601 date string
}
