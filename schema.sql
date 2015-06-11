drop table if exists marklist;
create table marklist(
  id integer primary key autoincrement,
  name text not null,
  mark integer not null
);
