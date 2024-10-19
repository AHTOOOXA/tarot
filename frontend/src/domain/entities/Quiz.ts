import Question from "./Question";
import User from "./User";

export default interface Quiz {
    question: Question;
    friends: User[];
  }
