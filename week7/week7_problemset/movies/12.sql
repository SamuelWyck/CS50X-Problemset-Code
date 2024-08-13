SELECT movies.title FROM movies, stars WHERE movies.id = stars.movie_id AND stars.person_id = (SELECT id FROM people WHERE name = 'Jennifer Lawrence') INTERSECT SELECT movies.title FROM movies, stars WHERE movies.id = stars.movie_id AND stars.person_id = (SELECT id FROM people WHERE name = 'Bradley Cooper') ORDER BY title;



