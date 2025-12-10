-- Enable INSERT access for the Knowledge Base tables
-- WARNING: This allows anonymous inserts. In production, restrict this to authenticated users or service role only.

-- 1. Specialties
create policy "Allow public insert" on specialties for insert with check (true);
create policy "Allow public update" on specialties for update using (true);

-- 2. Hospitals
create policy "Allow public insert" on hospitals for insert with check (true);
create policy "Allow public update" on hospitals for update using (true);

-- 3. Doctors
create policy "Allow public insert" on doctors for insert with check (true);
create policy "Allow public update" on doctors for update using (true);

-- 4. Medical Conditions
create policy "Allow public insert" on medical_conditions for insert with check (true);
create policy "Allow public update" on medical_conditions for update using (true);

-- 5. Linking Table
create policy "Allow public insert" on hospital_conditions for insert with check (true);
create policy "Allow public update" on hospital_conditions for update using (true);
