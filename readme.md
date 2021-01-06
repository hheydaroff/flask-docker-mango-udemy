# Rest-ful API

API is just an intermediary that let's two applications to talk to each other
Restful API is just an architectural style of building API that uses HTTP requests. The request types can be as following:

    -GET
    -POST
    -PUT
    -DELETE
    -etc.

## Resource Method Chart
Resource Method Chart helps to organize how the API architecture will look like.
As an example, we can build an API that uses the mathematical operators to return the output to user.

| Resource      | Method        | Path  | Used for      | Param        | Status on Error | 
| ------------- |:-------------:| -----:| --------------| -----------  | --------------- |
| -             | POST          | /subtract| subtracting 2 nums | x:int, y:int | 200 OK, 301 Missing |
| /             | POST          | /divide  | dividing 2 nums | x:int, y:int | 200 OK, 301 Missing, 302 y is 0 |
| +             | POST          | /add  | adding 2 nums | x:int, y:int | 200 OK, 301 Missing |




