## /Catalogue ==> Search

### What does it do ?

"X" is a platform for teachers to setup and sell their short online courses. 🛜 👩‍🏫

- A course has a fixed start and end date and runs as per the schedule. 
- It has a title and a description for the students to understand the curriculum better.
- A course is taught by a single teacher and has a price that the students have to pay for before registering.
- The courses can be searched by students


Let's begin our journey by building a **search & discovery system** - starting from the most fundamental features that we need, to more complex requirements that could come in.


### Requirements

1. Ability to handle the following queries quickly and reliably:
	- **Free text search** 
	*Find me a course in "handicraft" *
	- **Free text search + filters** 
	*Find me a course in "baking" under INR 599 in October *
	- **Free text search + filters + sorting**
	*Find me a course in "baking" in October in decreasing order of price *
	- **Free text search + filters + sorting + pagination**
	*Find me 10 courses in "baking" under 500 in increasing order of total registrations so far*
	- **Image Search**
	- **Semantic Search**
	- **Search in video**

2. Keep updating the searchable catalogue with the latest information about the product - courses in this case (updating sold out inventory, price, correction in description, new course launched by a teacher etc)


### Versions of Search

<b><u>V1: Filtering, Sorting, Pagination</u></b>

Update mappings : {
	"properties": {
		"category": {
			"type": "text",
			"fields": {
				"raw": {
					"type": "keyword"
				}
			}
		}
	}
}

<b><u>++ V2: Search by keyword (exact match)</u></b>

This works well when your corpus (set of documents to be searched) require an exact match. Example : Searching for electronic parts with exact labels, medicines with specific scientific names


<b><u>++ V3: Dynamic Search & Sort Filters</u></b>

Situation : Let's say your catalogue has over 10k or 15k of products. When a user searches for something, the search results are narrowed down to a subset of 700 products. The filters that you wish to show for your search query should be calculated in this subset (and not the entire catalogue !)

Can we do this in memory ? Sure, but we will have to fetch the entire result set, calculate the stats and then return the paginated & sorted response. This means additional querying and code to calculate stats that needs to be maintained as the document structure evolves. Leveraging the database (ES in this case) makes more sense

      "aggs": {
        "prices": {
          "histogram": {
            "field": "amount",
            "interval": 500
          }
        },
        "categories": {
          "terms": {
            "field": "category.raw"
          }
        }
      }


</br>

<b><u> ++ V4: Keyword partial match, Multi field matches and scoring </u></b>

This is where we have to deep dive a little bit into text analysis.	
Analyzer = character filters + tokenizers + token filters

For the fields on which you want your "partial match" and some level of spell correction to happen, you need to specify and analyzer. There are standard analyzers available out of the box which are great t get started.
Soon enough as you fine tune it, you can build you own analyzers as a combination of filters and tokenizers.


1. Run this on your ES node
*PUT /elearning-index*
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom_analyzer": {
          "type": "custom",
          "tokenizer": "my_custom_tokenizer",
          "filter": ["lowercase", "asciifolding","stop"],
          "char_filter": ["html_strip"]
        }
      },
      "tokenizer": {
        "my_custom_tokenizer": { // Needed for partial match
          "type": "ngram",
          "min_gram": 4,
          "max_gram": 5,
          "token_chars": [
            "letter",
            "digit"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "heading": { // Needed for partial match
        "type": "text",
        "analyzer": "my_custom_analyzer",
        "search_analyzer": "my_custom_analyzer"
      },
      "description": { // Needed for partial match
        "type": "text",
        "analyzer": "my_custom_analyzer",
        "search_analyzer": "my_custom_analyzer"
      },
      "category": { // Needed for aggregation (dynamic filter)
        "type": "text",
        "fields": {
          "raw": {
            "type": "keyword"
          }
        }
      }
    }
  }
}

2. Hit http://localhost:8000/catalogue/search/reindex in your browser

3. Hit http://localhost:8000/catalogue/search/?keyword=master to search for results

https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html



<b><u> ++ V5: Semantic Search </u></b>

We can try and tackle a slightly more complex problem of semantic search. Understanding with the help of an example - 

You try to search "something sweet to eat" and the results that show up are "cake", "cookies", "sweet jaggery". Had semantic search not been enabled, you wouldn't have found "cake" or "cookie"

<b><u> ++ V5: Image Search </u></b>

<b><u> ++ V5: Video Search </u></b>

Taking example of online courses,too often what the description doesn't capture could be stored in the video of a course. 

How is that possible ?
A description for an online course on "Weekend Baking : 5 recipes" mentions 5 specific recipes. The teacher in the class ends up teaching two other bonus recipes which were never mentioned in the description. We could analyze the transcript of what was "spoken during the course by the teacher" as well as analyze the video to extract more information as to what exactly was taught.


Adding this information to the course document in the search database should make our search resultsmore relevant for the user.

A simple algorithm could be take a snapshot every 1, 2 or 3 seconds and extract objects from each set.
Post that... WIP