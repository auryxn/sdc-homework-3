create table if not exists Etl_Rejected_Visit (
	rejected_id   serial primary key,
	v_id          int,
	visit_date    date,
	gym_code      text,
	personal_code text,
	visitor_name  text,
	time_in       time,
	time_out      time,
	reject_reason text not null,
	rejected_at   timestamp not null default now()
);

create or replace procedure run_etl()
language plpgsql
as $$
declare
	v_rejected   int;
	v_duplicates int;
	v_loaded     int;
begin
	insert into Dim_Date (date_key, day_number_of_month, month_number_of_year, year_number, day_name, month_name)
	select s.visit_date,
	       extract(day from s.visit_date)::int,
	       extract(month from s.visit_date)::int,
	       extract(year from s.visit_date)::int,
	       to_char(s.visit_date, 'FMDay'),
	       to_char(s.visit_date, 'FMMonth')
	from Staging_Gym_visit s
	where s.visit_date is not null
	group by s.visit_date
	on conflict (date_key) do nothing;

	with checked as (
		select s.v_id,
		       case
		           when s.personal_code is null then 'Personal code is missing'
		           when m.member_id is null then 'Personal code is not found in Dim_Member'
		           when g.gym_id is null then 'Gym code is not found in Dim_Gym'
		           when s.visitor_name is null or trim(s.visitor_name) = '' then 'Visitor name is missing'
		           when lower(trim(s.visitor_name)) <> lower(
		                    case when s.gym_code = 'Gym_2'
		                         then m.first_name || ' ' || m.last_name
		                         else m.last_name || ' ' || m.first_name
		                    end) then 'Visitor name does not match personal code'
		           when s.time_in is null and s.time_out is null then 'Both time_in and time_out are missing'
		           when s.time_in is not null and s.time_out is not null and s.time_out <= s.time_in
		                then 'Time_out is not later than time_in'
		       end as reject_reason
		from Staging_Gym_visit s
		left join Dim_Member m on m.personal_code = s.personal_code
		left join Dim_Gym g on g.gym_code = s.gym_code
	)
	insert into Etl_Rejected_Visit (v_id, visit_date, gym_code, personal_code,
	                                visitor_name, time_in, time_out, reject_reason)
	select s.v_id, s.visit_date, s.gym_code, s.personal_code,
	       s.visitor_name, s.time_in, s.time_out, c.reject_reason
	from checked c
	join Staging_Gym_visit s on s.v_id = c.v_id
	where c.reject_reason is not null;

	get diagnostics v_rejected = row_count;

	delete from Staging_Gym_visit s
	using Etl_Rejected_Visit r
	where r.v_id = s.v_id;

	select count(*) - count(distinct (visit_date, gym_code, personal_code, time_in, time_out))
	into v_duplicates
	from Staging_Gym_visit
	where time_in is not null and time_out is not null;

	drop table if exists tmp_etl_visits;
	create temp table tmp_etl_visits (
		gym_code      text,
		personal_code text,
		gym_id        int,
		member_id     int,
		visit_date    date,
		time_in       time,
		time_out      time,
		src_ids       int[]
	);

	insert into tmp_etl_visits (gym_code, personal_code, gym_id, member_id,
	                            visit_date, time_in, time_out, src_ids)
	select s.gym_code, s.personal_code, g.gym_id, m.member_id,
	       s.visit_date, s.time_in, s.time_out, array_agg(s.v_id order by s.v_id)
	from Staging_Gym_visit s
	join Dim_Member m on m.personal_code = s.personal_code
	join Dim_Gym g on g.gym_code = s.gym_code
	where s.time_in is not null and s.time_out is not null
	group by s.gym_code, s.personal_code, g.gym_id, m.member_id,
	         s.visit_date, s.time_in, s.time_out;

	insert into tmp_etl_visits (gym_code, personal_code, gym_id, member_id,
