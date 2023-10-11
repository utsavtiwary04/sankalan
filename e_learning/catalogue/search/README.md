## /Catalogue ==> Search

### What does it do ?

"X" is a platform for teachers to setup and sell their short online courses. 🛜 👩‍🏫

- A course has a fixed start and end date and runs as per the schedule. 
- It has a title and a description for the students to understand the curriculum better.
- A course is taught by a single teacher and has a price that the students have to pay for before registering.
- The courses can be searched by students


Let's begin our journey by building a search & discovery system - starting from the most fundamental features that we need to more complex requirements that could come in.



* 1. Filtering, Sorting, Pagination

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

* 2. ++ Keyword exact-match

This works well when your corpus (set of documents to be searched) require an exact match. Example : Searching for electronic parts with exact labels, medicines with specific scientific names


* 3. ++ Dynamic filters

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



* 4. ++ Keyword partial match, Multi field matches and scoring 

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





* ++ Semantic search