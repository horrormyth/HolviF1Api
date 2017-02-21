# Imports
import os.path
import json
from flask import Flask, jsonify
from flask.ext.restful import Api, Resource, reqparse,abort
from datetime import datetime
from collections import defaultdict

# File Reader

SRC_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(SRC_DIR, 'data')
drivers_dat = os.path.join(DATA_DIR,'drivers.json')
teams_data = os.path.join(DATA_DIR,'teams.json')


def json_loader(path,charset='utf-8'):
    with open(path) as file:
        json_data =json.load(file,encoding='utf-8')
    return json_data

# Load Datas
drivers_data =json_loader(drivers_dat)
teams_data = json_loader(teams_data)

# avoid it doing the request
LIST_OF_DRIVERS = [driver['driver'] for driver in drivers_data]


# app initialization
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  #handle asccii errors
api = Api(app)

# data
races = [{
    "number": 15,
    "name": "Agp",
    "date": "2016-05-06",
    "drivers": [{"name": "Kimi Räikkönen", "point": 9},
                {"name": "Fernando Alonso", "point": 3},
                {"name": "Nico Rosberg", "point": 39},
                {"name": "Lewis Hamilton", "point": 10},
                {"name": "Sebastian Vettel", "point": 20},
                {"name": "Daniel Ricciardo", "point": 1},
                {"name": "Kevin Magnussen", "point": 30},
                {"name": "Felipe Massa", "point": 40},
                {"name": "Jenson Button", "point": 10},
                {"name": "Valtteri Botas", "point": 80}]
},
{
    "number": 16,
    "name": "MGP",
    "date": "2016-05-06",
    "drivers": [{"name": "Fernando ALONSO", "point": 9},
                {"name": "Kimi Räikkönen", "point": 3},
                {"name": "Lewis Hamilton", "point": 39},
                {"name": "Nico Rosberg", "point": 10},
                {"name": "Valtteri Botas", "point": 20},
                {"name": "Jenson Button", "point": 1},
                {"name": "Kevin Magnussen", "point": 30},
                {"name": "Felipe Massa", "point": 40},
                {"name": "Daniel Ricciardo", "point": 10},
                {"name": "Sebastian Vettel", "point": 80}]
}
]
# Args Grabber -- Done

def get_race_args():
    main_parser = reqparse.RequestParser()
    # parse first
    main_parser.add_argument('number', required = True, type = int, location = 'json')
    main_parser.add_argument('name', required = True, type =str, location = 'json')
    main_parser.add_argument('date',required=True, type  = str, location = 'json')
    main_parser.add_argument('drivers', required = True, type =list, location = 'json')
    main_args = main_parser.parse_args(strict = True)

    #parse drivers list
    for driver in main_args.get('drivers'):
        drivers_parser = reqparse.RequestParser()
        drivers_parser.add_argument('name',required = True, type= str, location = 'driver' )
        drivers_parser.add_argument('point', required =True, type= int, location = 'driver' )

        driver_arg = reqparse.Namespace()

        driver_arg.driver = driver
        drivers_parser.parse_args(req=driver_arg, strict = True)

    return main_args

# Usable Method for race reuslts based on nunber
def race_getter(number):
        results = [race for race in races if race['number'] == number]
        if len(results) == 0:
            abort(404, message={'Race number %d' % number: 'does not exist'})
        else:
            for result in results:
                sorted_by_points = sorted(result['drivers'], key=lambda k: k['point'])
                results[0]['drivers'] = sorted_by_points

            return results[0]
# Usable Method for driver list
def driver_lists():
    return drivers_data


# As a race managers we want to be able to post completed race results -- Done
class Races(Resource):
    def get(self):
        standing_parser = reqparse.RequestParser()
        standing_parser.add_argument('name', required=False, type=str, location='args')
        args = standing_parser.parse_args(strict=True)
        race_name = args.get('name')
        # check if name exists
        if race_name is not None:
            if race_name in [existing_race['name'] for existing_race in races]:
                return [existing_race for existing_race in races \
                        if existing_race['name'] == race_name]
            else:
                return {'Race %s' % race_name: 'Not Exists'}
        return jsonify({'races': races})

    def post(self):
        args = get_race_args()

        new_race = {
            'number':args['number'],
            'name' : args['name'],
            'date' :args['date'],
            'drivers':args['drivers']
        }

        # Name Check --Done
        posted_driver_list = [driver['name'] for driver in new_race['drivers']]
        non_listed_drivers = [driver for driver in posted_driver_list if driver not in LIST_OF_DRIVERS]
        if(non_listed_drivers):
            abort(404,message = {'Drivers %s'%non_listed_drivers:'Does not Exists'})

        # Date validation -- Done
        try:
            new_race['date'] = str(datetime.strptime(new_race['date'], '%Y-%m-%d'))

        except:
            return {'Data type or Length': 'Not Correct'}

        # Check if the race number exists if exists return null
        new_race_number = new_race['number']
        all_race_numbers = [f_race['number'] for f_race in races]
        if new_race_number in all_race_numbers or new_race in races:
            return {"Race Number %s"%new_race_number:'Already Exists'}

        races.append(new_race)

        # return last index the latest one
        return jsonify({new_race['name']:races})



# Get specific race results and driver standings -- Done
class RaceByNumber(Resource):
    def get(self,number):
        return jsonify({number:race_getter(number)})

# Driverlists only -- Done
class DriverList(Resource):
    def get(self):
        return jsonify({'drivers':drivers_data})

# Drivers by country -- Done
class DriverByCountry(Resource):
    def get(self,country):
        drivers_by_country = [driver for driver in drivers_data if driver['country'] == country]
        if drivers_by_country:
            return jsonify({country:drivers_by_country})
        else :
            abort(404, message={'Country : %s' % country: 'Not Found'})


# Driver list By Team -- Done
class DriverByTeamId(Resource):
    def get(self,id):
        drivers_by_team = [driver for driver in drivers_data if driver['team'] == id]
        if drivers_by_team:
            return jsonify({id:drivers_by_team})
        else:
            abort(404,message = {'Team Id %d'%id:'Not Found'})

# Team id based on the driver name given -- Done
class DriversByTeamName(Resource):
    def get(self,tname):
        team_ids = [team['id'] for team in teams_data if team['team'] == tname]
        if len(team_ids)==0:
            abort(404, message={'Team Name%s' %tname: 'does not exist !!'})
        driverlist = [driver for driver in drivers_data if driver['team'] == team_ids[0]]
        return jsonify({tname: driverlist})

# Teams only  -- Done
class Teams(Resource):
    def get(self):
        return jsonify({'teams':teams_data})

# Team Standings  by Race Number -- Done
class TeamStandings(Resource):
    def get(self,number):
        selected_race=race_getter(number)
        drivers_team=[]
        for driverid in drivers_data:
            for team in teams_data:
                if team['id'] == driverid['team']:
                    drivers_team.append(team['team'])
        updated_drivers = [dict(key, team=value) for key, value in zip(selected_race['drivers'], drivers_team)]
        defdict = defaultdict(int)

        for values in updated_drivers:
            defdict[values['team']] += values['point']

        sorted_standings = sorted([{'team': team, 'points': points} \
                for team, points in defdict.items()], key=lambda k: k['points'])

        return jsonify({'team_standings':sorted_standings})

# Team by Country -- Done
class TeamByCountry(Resource):
    def get(self,country):
        driver_ids = [driver['team'] for driver in drivers_data if driver['country'] == country]
        if len(driver_ids) == 0:
            abort(404, message={'Somebody overtook the country %s' % country: 'does not exist !!'})
        team_list = [team for team in teams_data if team['id'] in driver_ids]

        return jsonify({country:team_list})




# Resources URL
api.add_resource(DriversByTeamName, '/api/v1/drivers/<string:tname>' )
api.add_resource(DriverByTeamId,'/api/v1/drivers/<int:id>')
api.add_resource(DriverByCountry,'/api/v1/driver_country/<string:country>')
api.add_resource(RaceByNumber,'/api/v1/races/<int:number>')
api.add_resource(TeamStandings,'/api/v1/races/<int:number>/team_standings')
api.add_resource(TeamByCountry,'/api/v1/teams/<string:country>')
api.add_resource(DriverList,'/api/v1/drivers',endpoint ='drivers')
api.add_resource(Teams, '/api/v1/teams',endpoint = 'teams')
api.add_resource(Races, '/api/v1/races', endpoint = 'races')



if __name__ == '__main__':
    app.run(debug=True)



# TODO we want to be able to get specific race result