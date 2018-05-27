from flask import Flask
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource
from datatime import datatime
from models import MessageModel
import status
from pytz import utc




class MessageManager():
	last_id = 0							## it's a class attribute, and ititially this is set to 0

	def __init__(self):
		self.messages = {}

		def insert_message(self, message):
			"""This method receives a recently created MessageModel instance in the message argument"""
			self.__class__.last_id += 1
			message.id = self.__class__.last_id
			self.messages[self.__class__.last_id] = message


		def get_message(self, id):
			"""This method receives the id of the message that has to be retrieved from the self.messages dictionary."""
			return self.messages[id]


		def delete_message(self, id):
			"""This method receives the id of the message that has to be removed from the self.messages dictionary"""
			del self.messages[id]



## Now, create a dictionary object with the args of the constructor of Message Model,
## and, we need to declare the data types of each arg

message_fields = {
	'id': fields.Integer,
	'uri': fields.Url('message_endpoint'),
	'message': fields.String,
	'duration': fields.Integer,
	'creation_date': fields.DateTime,
	'message_category': fields.String,
	'printed_times': fields.Integer,
	'printed_once': fields.Boolean
}


## Now, create an object of Message Manager class
message_manager = MessageManager()



class Message(Resource):
	def abort_if_message_doesnt_exist(self, id):
		if id not in message_manager.messages:
			abort(status.HTTP_404_NOT_FOUND,
				message = "Message {0} doesnot exists".format(id)
			)


	@marshal_with(message_fields)
	def get(self, id):
		self.abort_if_message_doesnt_exist(id)
		return message_manager.get_message(id)



	def delete(self, id):
		self.abort_if_message_doesnt_exist(id)
		message_manager.delete_message(id)
		return '', status.HTTP_204_NO_CONTENT




	@marshal_with(message_fields)
	def patch(self, id):
		self.abort_if_message_doesnt_exist(id)
		message = message_manager.get_message(id)
		parser = reqparse.RequestParser()
		parser.add_argument('message', type=str)
		parser.add_argument('duration', type=int)
		parser.add_argument('printed_times', type=int)
		parser.add_argument('printed_once', type=bool)
		args = parser.parse_args()
		if 'message' in args:
		message.message = args['message']
		if 'duration' in args:
		message.duration = args['duration']
		if 'printed_times' in args:
		message.printed_times = args['printed_times']
		if 'printed_once' in args:
		message.printed_once = args['printed_once']
		return message




class MessageList(Resource):
	@marshal_with(message_fields)
	def get(self):
		return [v for v in message_manager.messages.values()]
	

	@marshal_with(message_fields)
	def post(self):
		parser = reqparse.RequestParser()

		parser.add_argument('message', 
							type=str, 
							required=True,
							help='Message cannot be blank!'
							)

		parser.add_argument('duration', 
							type=int, 
							required=True,
							help='Duration cannot be blank!'
							)

		parser.add_argument('message_category', 
							type=str, 
							required=True,
							help='Message category cannot be blank!'
							)
		
		args = parser.parse_args()
		message = MessageModel(message=args['message'],
							duration=args['duration'],		
							creation_date=datetime.now(utc),
							message_category=args['message_category']
							)
		message_manager.insert_message(message)
		return message, status.HTTP_201_CREATED






app = Flask(__name__)
api = Api(app)
api.add_resource(MessageList, "/api/message")
api.add_resource(Message, "/api/message/<int:id>", 
				endpoint = "message_endpoint"
				)


if __name__ == "__main__":
	app.run(debug = True)