export default interface Friend {
  user_id: number;
  username: string | null;
  first_name: string;
  last_name: string | null;
  photo_url: string | null;
  status: 'online' | 'offline';
}
