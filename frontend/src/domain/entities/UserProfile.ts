export default interface UserProfile {
  user_id: number;
  username: string | null;
  first_name: string;
  last_name: string | null;
  language_code: string | null;
  photo_url: string | null;
}
