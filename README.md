## Catalogue

### What does it do ?

"X" is a platform for teachers to setup and sell their short online courses. 🛜 👩‍🏫 
*Ex Learn the fundamentals of Python in 10 days*

- A course has a fixed start and end date and runs as per the schedule. 
- It has a title and a description for the students to understand the curriculum better.
- A course is taught by a single teacher and has a price that the students have to pay for before registering.
- The courses can be searched by students

[TODO] Roadmap :
- Students can access study materials uploaded and shared by the teachers
- Students can be assessed via periodic assessments
- Freemium access for students (start for free and pay to continue)
- A frontend website to showcase the capabilities 🎉🎉
- <add your request here ?>

</br>
### Technical Capabilities

1. Ability to handle the following queries quickly and reliably:
	- **Free text search** 
	*Find me a course in "handicraft" *
	- **Free text search + filters** 
	*Find me a course in "baking" under INR 599 in October *
	- **Free text search + filters + sorting**
	*Find me a course in "baking" in October in decreasing order of price *
	- **Free text search + filters + sorting + pagination**
	*Find me 10 courses in "baking" under 500 in increasing order of total registrations so far*

2. Keep updating information in the searchable catalogue (updating sold out inventory, price, correction in description etc)

3. Register a student for a course and create access for the same

</br>

2. Being updated in real time as the catalogue is updated. The catalogue might need an update due to two main reasons:
	- **Company led** :* Price drop for a short time, stopping sale of certain items due to disruption, correction in features of a product, a new product is added to a category*

	- **User led** : *a product is sold out and is hence unavailable*

</br>
### System diagram and data models

</br>
### Troubleshooting

https://opster.com/guides/elasticsearch/security/elasticsearch-disable-ssl-securing-cluster-without-ssl-tls/

</br>
### 💡Key learnings
- Writing multiple search clients via inheritance
- Config management
- Building an asynchronous pipeline
- ABC
- ES
- CELERY
- DUMMY DATA (factory boy)

</br>
## 🔗 Resources for further learning