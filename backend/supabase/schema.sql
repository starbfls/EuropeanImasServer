-- 在新 Supabase 项目的 SQL Editor 中运行。可重复运行，不覆盖已有投稿。
begin;

create table if not exists public.submissions (
    id bigint generated always as identity primary key,
    kind text not null check (kind in ('gallery', 'business_cards')),
    payload jsonb not null check (jsonb_typeof(payload) = 'object'),
    files jsonb not null check (jsonb_typeof(files) = 'object'),
    size_bytes bigint not null check (size_bytes > 0),
    approved boolean not null default false,
    deleting boolean not null default false,
    legacy_key text unique,
    submitted_at timestamptz not null default now()
);

create index if not exists submissions_listing_idx
    on public.submissions (kind, approved, submitted_at desc, id desc)
    where deleting = false;

-- 云端图片总量上限（原图/缩略图合计）。默认 512 MiB，预留桶/套餐空间。
-- 按需调整：update public.media_settings set max_bytes = 2147483648 where id = true;
create table if not exists public.media_settings (
    id boolean primary key default true check (id),
    max_bytes bigint not null check (max_bytes > 0)
);
insert into public.media_settings (id, max_bytes) values (true, 536870912)
    on conflict (id) do nothing;

create or replace function public.enforce_media_quota()
returns trigger language plpgsql security definer set search_path = '' as $$
declare
    used_bytes bigint;
    limit_bytes bigint;
begin
    -- 串行化容量检查，避免并发插入都通过同一个剩余空间检查。
    perform pg_catalog.pg_advisory_xact_lock(73315642);
    select max_bytes into strict limit_bytes from public.media_settings where id = true;
    select coalesce(sum(size_bytes), 0) into used_bytes from public.submissions;
    if tg_op = 'UPDATE' then
        used_bytes := used_bytes - old.size_bytes;
    end if;
    if used_bytes + new.size_bytes > limit_bytes then
        raise exception 'media_storage_quota_exceeded' using errcode = 'P0001';
    end if;
    return new;
end;
$$;
drop trigger if exists submissions_media_quota on public.submissions;
create trigger submissions_media_quota before insert or update of size_bytes
    on public.submissions for each row execute function public.enforce_media_quota();

-- 所有数据库操作经 Flask 完成；不向浏览器开放读写权限。
alter table public.submissions enable row level security;
alter table public.media_settings enable row level security;
revoke all on public.submissions, public.media_settings from anon, authenticated;
revoke all on sequence public.submissions_id_seq from anon, authenticated;
grant usage on schema public to service_role;
grant all on public.submissions, public.media_settings to service_role;
grant usage, select on sequence public.submissions_id_seq to service_role;
revoke all on function public.enforce_media_quota() from public;

-- 待审核桶绝不能设为 public。公开桶只存管理员已通过的图片。
-- 文件体积上限 16 MiB，覆盖输入 8 MiB 经重新编码后的体积。
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values
    ('imas-pending', 'imas-pending', false, 16777216,
     array['image/jpeg', 'image/png', 'image/webp', 'image/gif']),
    ('imas-public', 'imas-public', true, 16777216,
     array['image/jpeg', 'image/png', 'image/webp', 'image/gif'])
on conflict (id) do update set
    public = excluded.public,
    file_size_limit = excluded.file_size_limit,
    allowed_mime_types = excluded.allowed_mime_types;

-- 不要给这些桶创建 anon/authenticated 的 INSERT、UPDATE、DELETE 或 SELECT policy。
-- service_role 由受信任的后端使用，可绕过 RLS；公开桶的 URL 下载无需 SELECT policy。
commit;
