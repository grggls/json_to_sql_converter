# Challenge

- Inside `request-data.json` you have two properties `nodes` and `edges`, `nodes` contains all the required information to apply the transformation into Table/Query and `edges` represents how they are linked together. In each node there is a property `transformObject` which is different for each `type`
There are 5 different types of nodes used in this request
  - INPUT  -> it contains information about table and which fields to select from original table. 
  - FILTER -> contains SQL "where" settings 
  - SORT		-> contains SQL "order by" settings 
  - TEXT_TRANSFORMATION	    -> contains information about applying some text SQL function on any column. For example UPPER, LOWER (see the digram for actual use case)
  - OUTPUT	-> contains SQL "limit" settings
