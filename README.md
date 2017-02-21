# F1 Api Overview

Api Route : ``` /api/v1/ ```

## Version
*v1*

## Dependencies
-   Flask==0.10.1
-   Flask-RESTful==0.3.1
-   Jinja2==2.7.3
-   MarkupSafe==0.23
-   Werkzeug==0.9.6
-   itsdangerous==0.24
-   six==1.9.0


## Instruction
-   Clone the repo
-   Create virtualenv in the cloned project folder and name it :``` env ``` as below
-   ``` virtualenv env ```
-   Acitvate the virutal environment
-   ``` source env/bin/activate```
-   Install the dependencies
-   ``` pip install -r requirements.txt```
-   Run App
-   ``` python app.py ```
-   Browse it by entering. E.G ```localhost:500/api/v1/races ``` **'races'** being endpoint name
-   For endpoints, follow the Paths -> Parameter Sections


## Paths
### POST /races
#### Description
Create new races object
#### Parameters

| Type     | Name | Description |Schema|Response|Status|
| :------- | ----: | :---: | :---: | :---: | :---: |
| **json** | **races**<br>*required*| New Race|Races|200|Okay|

### GET /races

| Type     | Name | Description |Schema|Response|Status|
| :------- | ----: | :---: | :---: | :---: | :---: |
| **Query** | **name**<br>*optional*| Get All Races|Races|200|Okay|

### GET /races/number
| Type     | Name | Description |Schema|Response|Status|
| :------- | ----: | :---: | :---: | :---: | :---: |
| **Query** | **number**<br>*required*| Specific Race results and Driver Standings| **int32**|200|Okay|

### GET /races/number/team_standings
| Type     | Name | Description |Schema|Response|Status|
| :------- | ----: | :---: | :---: | :---: | :---: |
| **Query** | **None**<br>|Team Standings by Race Number|Races|200|Okay

### GET /teams
| Type     | Name | Description |Schema|Response|Status|
| :------- | ----: | :---: | :---: | :---: | :---: |
| **Query** | **None**| Team List|Teams|200|Okay|

### GET /teams/country
| Type     | Name | Description |Schema|Response|Status|
| :------- | ----: | :---: | :---: | :---: | :---: |
| **Query** | **country**<br>*required*| Teams by country|Teams,<br> **string**|200|Okay|

### GET /drivers

| Type     | Name | Description |Schema|Response|Status|
| :------- | ----: | :---: | :---: | :---: | :---: |
| **Query** | **None**| Driver List|DriverList|200|Okay|

### GET /drivers/id
| Type     | Name | Description |Schema|Response|Status|
| :------- | ----: | :---: | :---: | :---: | :---: |
| **Query** | **id **<br>required| Drivers by Team Id |DriversByTeamId ,<br>**int**|200|Okay|

### GET driver_country/country
| Type     | Name | Description |Schema|Response|Status|
| :------- | ----: | :---: | :---: | :---: | :---: |
| **Query** | **country**<br >required| Drivers by Country Name|DriverByCountry,**string**|200|Okay|


### GET /drivers/tname
| Type     | Name | Description |Schema|Response|Status|
| :------- | ----: | :---: | :---: | :---: | :---: |
| **Query** | **tname**<br> required|Driver By TeamName|DriverByTeamName,<br>**string**|200|Okay|


## Note : Code could be better