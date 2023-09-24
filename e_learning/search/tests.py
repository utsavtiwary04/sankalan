from django.test import TestCase

# Create your tests here.


############# indexer ##############

/************CREATE INDEX***************/
PUT /elearning-search


/************INDEX A DOCUMENT***************/
POST /elearning-search/_doc
 {
  "course_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "heading": "Summer Baking : 15 Recipes",
  "description": "Le Cordon Bleu has a large variety of cookery courses available every summer. From classes of just a few hours to formally accredited 6/7 week courses, you should be able to find the cooking course that would suit you best. Our culinary courses are a wonderful way to learn more about the fundamental techniques in cuisine, pâtisserie or wine in entertaining and informal classes. Whether you are preparing for a professional cooking career or just wish to study over the summer for your own interest you should be able to find a summer programme for you.",
  "amount": 5699,
  "currency": "INR",
  "status": "accepting_registrations""category": [
    "baking",
    "recreational",
    "adults",
    "kids"
  ],
  "seats_available": 20,
  "teacher": {
    "full_name": "Amisha Jain",
    "courses_taken": 12
  },
  "schedule": {
    "start_date": "24 August, 2021",
    "end_date": "29 August, 2021",
    "duration": "60 mins",
    "sessions": 4,
    "session_start_timings": [
      1695571696,
      1695571800,
      1695572696,
      1695573696
    ]
  }
}

{
  "course_id": "9b1deb4d-3b7d-4bad-6bdd-2b0d7b3dcb6d",
  "heading": "Dance your heart out !",
  "description": "Well, if you're looking to also become the center of attention at the next music festival, then I've created this Shuffle Dance Masterclass for you!",
  "amount": 7999,
  "currency": "INR",
  "status": "accepting_registrations",
  "category": [
    "dance",
    "recreational",
    "adults"
  ],
  "seats_available": 40,
  "teacher": {
    "full_name": "Vijay Patel",
    "courses_taken": 3
  },
  "schedule": {
    "start_date": "24 October, 2024",
    "end_date": "24 December, 2024",
    "duration": "60 mins",
    "sessions": 10,
    "session_start_timings": [
      1695571696,
      1695571800,
      1695578696,
      1695573696,
      1695571696,
      1695571800,
      1695572396,
      1695573696,
      1695572676,
      1695571803
    ]
  }
}


/************SEARCH (paginate, search, sort, filter)***************/
POST /elearning-search/_search
{
    "from": 0,
    "size": 2,
    "sort": { "amount" : "asc" }
	"query": {
		"bool": {
			"must": [
				{
					"match": {
						"heading": "baking classes"
					}
				}
			],
			"filter": [ 
                { "term":  { "status": "accepting_registrations" }},
                { "range": { "amount": { "lte": "7699" }}}
              ]
		}
	}
}
