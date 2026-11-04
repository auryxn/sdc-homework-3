/*
	HomeTask #1 - ETL
	Move gym visits from Staging_Gym_visit into the DWH (Dim_Date + Fact_Visit).

	Run order:
		1. HT1_part1.sql   - creates the DWH and the staging table, loads the first data set
		2. etl.sql         - creates the error table and the procedure, runs the load
		3. HT1_part2.sql   - adds the second data set
		4. call run_etl(); - load the new rows
*/

-- ---------------------------------------------------------------
-- Rows that cannot be loaded are moved here instead of the DWH
-- ---------------------------------------------------------------
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

-- ---------------------------------------------------------------
-- ETL procedure
-- ---------------------------------------------------------------
create or replace procedure run_etl()
language plpgsql
as $$
declare
	v_rejected   int;
	v_duplicates int;
	v_loaded     int;
begin
	-- Step 1. Add every new date from staging to Dim_Date
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

	-- Step 2. Find rows that cannot be trusted and move them to the error table
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

	-- Step 3. Build one row per visit.
	-- Duplicates (same member, gym, date, time_in, time_out) are counted first
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

	-- 3a. Visits that already have both times in one row (Gym_1, and complete Gym_2 rows)
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

	-- 3b. Gym_2 visits split over two rows: first row has time_in, second has time_out.
	-- Rows are paired in chronological order inside the same gym/member/date.
	insert into tmp_etl_visits (gym_code, personal_code, gym_id, member_id,
	                            visit_date, time_in, time_out, src_ids)
	select o.gym_code, o.personal_code, o.gym_id, o.member_id,
	       o.visit_date, o.time_in, c.time_out, array[o.v_id, c.v_id]
	from (
		select s.v_id, s.gym_code, s.personal_code, g.gym_id, m.member_id, s.visit_date, s.time_in,
		       row_number() over (partition by s.gym_code, s.personal_code, s.visit_date
		                          order by s.time_in) as rn
		from Staging_Gym_visit s
		join Dim_Member m on m.personal_code = s.personal_code
		join Dim_Gym g on g.gym_code = s.gym_code
		where s.time_in is not null and s.time_out is null
	) o
	join (
		select s.v_id, s.gym_code, s.personal_code, s.visit_date, s.time_out,
		       row_number() over (partition by s.gym_code, s.personal_code, s.visit_date
		                          order by s.time_out) as rn
		from Staging_Gym_visit s
		where s.time_in is null and s.time_out is not null
	) c
	  on c.gym_code = o.gym_code
	 and c.personal_code = o.personal_code
	 and c.visit_date = o.visit_date
	 and c.rn = o.rn
	 and c.time_out > o.time_in;

	-- Step 4. Load the visits into the fact table
	insert into Fact_Visit (gym_id, member_id, visit_date_key, visit_duration, day_part)
	select v.gym_id,
	       v.member_id,
	       v.visit_date,
	       (extract(epoch from (v.time_out - v.time_in)) / 60)::int,
	       (case
	            when v.time_in < time '10:01' then 'Morning'
	            when v.time_in < time '17:01' then 'Day'
	            else 'Evening'
	        end)::day_part_enum
	from tmp_etl_visits v;

	get diagnostics v_loaded = row_count;

	-- Step 5. Remove what was loaded from staging
	delete from Staging_Gym_visit s
	where s.v_id in (select unnest(v.src_ids) from tmp_etl_visits v);

	-- Half-rows that were completed by a full row in this run are not needed any more
	delete from Staging_Gym_visit s
	using tmp_etl_visits v
	where s.gym_code = v.gym_code
	  and s.personal_code = v.personal_code
	  and s.visit_date = v.visit_date
	  and ((s.time_in = v.time_in and s.time_out is null)
	    or (s.time_in is null and s.time_out = v.time_out));

	drop table if exists tmp_etl_visits;

	raise notice 'ETL finished: % visits loaded, % rows rejected, % duplicates collapsed, % rows left in staging',
		v_loaded, v_rejected, v_duplicates, (select count(*) from Staging_Gym_visit);
end;
$$;

call run_etl();
