# Rest-ful API

API is just an intermediary that let's two applications to talk to each other
Restful API is just an architectural style of building API that uses HTTP requests. The request types can be as following:

    -GET
    -POST
    -PUT
    -DELETE
    -etc.
<br/>
<br/>

# Resource Method Chart
Resource Method Chart helps to organize how the API architecture will look like.
As an example, we can build an API that uses the mathematical operators to return the output to user.

| Resource      | Method        | Path  | Used for      | Param        | Status on Error | 
| ------------- |:-------------:| -----:| --------------| -----------  | --------------- |
| -             | POST          | /subtract| subtracting 2 nums | x:int, y:int | 200 OK, 301 Missing |
| /             | POST          | /divide  | dividing 2 nums | x:int, y:int | 200 OK, 301 Missing, 302 y is 0 |
| +             | POST          | /add  | adding 2 nums | x:int, y:int | 200 OK, 301 Missing |

<br/>
<br/>


# Database
Database stores the data for a future usage (i.e. login details, posts, purchase details, etc.).
There are two types of databases:

* SQL - relational, table based database
* No-SQL - non-relational, key-value based database

<br/>
<br/>

## MongoDB

MongoDB is a cross-platform, document oriented database that provides, high peformance, high availability, and easy scalability. 
* MongoDB works on concept of _collection_ and _document_
* **Collection** is a group of MongoDB docs. It is the equivalent of an RDBMS table. 
    * A collection exists within a single database
    * Collections do not enforce schema
    * Documents within a collection can have different fields
    * Typically, all docs in a collection are of similar or related purpose

* **Document** is a set of _key-value_ pairs. 
    * Documents have dynamic schema
    * Dynamic schema means that docs in thes ame collection do not need to have the same set of fields or structure, and common fields in a collection's doc may hold different types of data.

<br/>

### RDBM vs MongoDB
| RDBM          | MongoDB           | 
| ------------- |:-----------------:| 
| Database      | Database          | 
| Table         | Collection        |
| Row           | Document          | 
| Column        | Field             | 
| Table Join    | Embedded Docs     | 
| Primary Key   | Default key _id   | 

<br/>

### Advantages of MongoDB over RDBMS
* **Schemaless** - MongoDB is a document database in which one collection holds different docs. Number of fields, content and size of the doc can differe from one to another
* Structure of a single object is clear
* No complex joins
* Deep query-ability. MongoDB supports dynamic queries on docs using a doc-based query language that's nearly as powerful as SQL. 

<br/>

> Data in MongoDB has a flexible schema. Documents in the same collection. They do not need to have the same set of fields or structure, and common fields in a collection's documents may hold different types of data.

<br/>

### Considerations on designing Schema in MongoDB
* Design your schema according to user requirements
* Combine objects into one document if you will use them together. Otherwise separate them.
* Duplicate the data because disk space is  cheap as compare to compute time
* Do joins while write, not on read.
* Optimize your schema for most frequent use cases.
* Do complex aggregation in the schema.

