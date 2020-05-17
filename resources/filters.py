def normalize_path_params(	city=None,
							min_stars=0,
							max_stars=5,
							min_daily=0,
							max_daily=10000,
							limit=50,
							offset=0,
							**kwargs):
	if not city:	
		return {
			"min_stars": min_stars,
			"max_stars": max_stars,
			"min_daily": min_daily,
			"max_daily": max_daily,
			"limit": limit,
			"offset": offset
		}
	return { #**data
		"city": city,
		"min_stars": min_stars,
		"max_stars": max_stars,
		"min_daily": min_daily,
		"max_daily": max_daily,
		"limit": limit,
		"offset": offset
	}

query_off_city = """
					SELECT * FROM hotels
					WHERE (stars >= ? and stars <= ?)
					and (daily >= ? and daily <= ?)
					LIMIT ? OFFSET ?
				"""

query_on_city = """
					SELECT * FROM hotels
					WHERE (city = ?)
					and (stars >= ? and stars <= ?)
					and (daily >= ? and daily <= ?)
					LIMIT ? OFFSET ?
				"""