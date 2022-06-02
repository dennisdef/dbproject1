drop schema if exists dbproject;
create schema dbproject;
use dbproject;

create table executive(
	ex_id INT unsigned not null auto_increment,
	name varchar(45) not null,
	primary key (ex_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table program(
	program_id INT unsigned not null auto_increment,
	name varchar(55) not null,
	address varchar(55) not null,
	primary key (program_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table organisation(
	organisation_id INT unsigned not null auto_increment,
	name varchar(45) not null,
	abbr varchar(10) not null,
	postal_code varchar(45) default null,
	street varchar(45) not null,
	city varchar(45) not null,
	street_number varchar(45) not null,
	primary key (organisation_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table researcher(
	r_id INT unsigned not null auto_increment,
	first_name varchar(45) not null,
	last_name varchar(45) not null,
	birth_date date not null,
	sex varchar(45) not null,
	start_date timestamp not null DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	organisation_id int unsigned not null,
	primary key (r_id),
	constraint fk_er foreign key (organisation_id) references organisation (organisation_id) ON DELETE RESTRICT ON UPDATE CASCADE 
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table science_field(
	field_id INT unsigned not null auto_increment,
	en_name varchar(45) not null,
	name varchar(45) not null,
	primary key (field_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table phone(
	organisation_id int unsigned not null,
	phone varchar(13) not null,
	primary key (organisation_id,phone),
	constraint fk_organisation foreign key (organisation_id) references organisation (organisation_id) ON DELETE RESTRICT ON UPDATE CASCADE 
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table company(
	c_id INT unsigned not null auto_increment,
	equity decimal(9,2) not null,
	organisation_id int unsigned not null,
	primary key (c_id),
	constraint fk_organisation_company foreign key (organisation_id) references organisation (organisation_id) ON DELETE RESTRICT ON UPDATE CASCADE 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table university(
	university_id INT unsigned not null auto_increment,
	budget_me decimal(9,2) not null,
	organisation_id int unsigned not null,
	primary key (university_id),
	constraint fk_organisation_university foreign key (organisation_id) references organisation (organisation_id) ON DELETE RESTRICT ON UPDATE CASCADE 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table research_center(
	r_center_id INT unsigned not null auto_increment,
	budget_me decimal(9,2) not null,
	budget_pa decimal(9,2) not null,
	organisation_id int unsigned not null,
	primary key (r_center_id),
	constraint fk_organisation_rc foreign key (organisation_id) references organisation (organisation_id) ON DELETE RESTRICT ON UPDATE CASCADE 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


create table project(
	project_id int unsigned not null auto_increment,
	title varchar(1000) not null,
	summary varchar(10000) not null,
	start_date timestamp not null DEFAULT CURRENT_TIMESTAMP,
	end_date timestamp not null,
	amount decimal(9,2) not null,
	grade decimal(2,1) null,
	check (grade<=10 and grade>=0),
	evaluation_date timestamp null DEFAULT CURRENT_TIMESTAMP,
	evaluator_id INT unsigned NOT null,
	ex_id int unsigned not null,
	program_id int unsigned not null,
	organisation_id int unsigned not null,
	r_id int unsigned null,
	primary key (project_id),
	constraint fk_organisation_project foreign key (organisation_id) references organisation (organisation_id) ON DELETE RESTRICT ON UPDATE cascade,
	constraint fk_researcher_project foreign key (r_id) references researcher (r_id) ON DELETE RESTRICT ON UPDATE cascade,
	constraint fk_evaluator_project foreign key (evaluator_id) references researcher (r_id) ON DELETE RESTRICT ON UPDATE cascade,
	constraint fk_program_project foreign key (program_id) references program (program_id) ON DELETE RESTRICT ON UPDATE cascade,
	constraint fk_executive_project foreign key (ex_id) references executive (ex_id) ON DELETE RESTRICT ON UPDATE cascade
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table deliverable(
	d_id INT unsigned not null auto_increment,
	title varchar(45) not null,
	summary varchar(1000) not null,
	delivery_date timestamp not null DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	project_id int unsigned not null,
	primary key (d_id),
	constraint fk_del_proj foreign key (project_id) references project (project_id) ON DELETE restrict on UPDATE cascade
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table works(
	project_id int unsigned not null,
	r_id int unsigned not null,
	primary key (project_id, r_id),
	constraint fk_researcher_project_w foreign key (r_id) references researcher (r_id) ON DELETE RESTRICT ON UPDATE cascade,
	constraint fk_project_r foreign key (project_id) references project (project_id) ON DELETE RESTRICT ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table project_science_field(
	project_id int unsigned not null,
	field_id int unsigned not null,
	primary key (project_id,field_id),
	constraint fk_project_sf foreign key (project_id) references project (project_id) ON DELETE RESTRICT ON UPDATE CASCADE,
	constraint fk_field_project foreign key (field_id) references science_field (field_id) ON DELETE RESTRICT ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE view projects_by_researcher as 
SELECT
CONCAT(r.first_name, " ", r.last_name) AS researcher,
COUNT(r.r_id) as number_of_projects
from researcher r 
inner join works w on r.r_id = w.r_id group by r.r_id ;



