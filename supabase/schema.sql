-- Run once in Supabase SQL editor.
create table if not exists app_state (
  key         text primary key,
  data        jsonb not null default '{}'::jsonb,
  updated_at  timestamptz not null default now()
);

create or replace function set_updated_at() returns trigger as $$
begin new.updated_at = now(); return new; end; $$ language plpgsql;

drop trigger if exists trg_app_state_updated on app_state;
create trigger trg_app_state_updated before update on app_state
  for each row execute function set_updated_at();
