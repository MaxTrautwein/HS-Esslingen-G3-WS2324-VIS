insert into floor (floorname, floorplan, floorprefix) VALUES
    ('EG','/Some/Path/Plan.png','F1.0'),
    ('UG2','/Some/Path/Plan.png','F1.-2'),
    ('UG','/Some/Path/Plan.png','F1.-1'),
    ('Empore','/Some/Path/Plan.png','F1.0'),
    ('1','/Some/Path/Plan.png','F1.1'),
    ('2','/Some/Path/Plan.png','F1.2');

insert into room (number, name, path, pathaccess, floor) VALUES
    ('08','F1.405','/Some/Path/path.png','/Some/Path/path.png',2),
    ('07','F1.408','/Some/Path/path.png','/Some/Path/path.png',6),
    ('10','F1.411','/Some/Path/path.png','/Some/Path/path.png',3)