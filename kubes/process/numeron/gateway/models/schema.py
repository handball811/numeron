import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .models import Service as ServiceModel, User as UserModel
from . import connection_base

handler = connection_base.mysql_handler_factory()

class Service(SQLAlchemyObjectType):
	class Meta:
		model = ServiceModel
		interfaces = (relay.Node, )
class ServiceConnection(relay.Connection):
	class Meta:
		node = Service
class CreateService(graphene.Mutation):
	uuid = graphene.String()
	name = graphene.String()

	class Arguments:
		name = graphene.String()

	def mutate(self, info, name):
		services = handler.get_session().\
			query(ServiceModel).\
			filter(ServiceModel.name == name).\
			all()
		if len(services) == 0:
			service = ServiceModel(name=name)
			handler.add(service)
			try:
				handler.commit()
			except:
				import traceback
				print("Error occured while SErvice")
				traceback.print_exc()
		else:
			service = services[0]
		return CreateService(
			uuid=service.uuid,
			name=service.name)

class User(SQLAlchemyObjectType):
	class Meta:
		model = UserModel
		interfaces = (relay.Node, )
class UsersConnection(relay.Connection):
	class Meta:
		node = User
class CreateUser(graphene.Mutation):
	uuid = graphene.String()
	name = graphene.String()
	service_name = graphene.String()
	service_user_id = graphene.String()

	class Arguments:
		name = graphene.String()
		service_name = graphene.String()
		service_user_id = graphene.String()

	def mutate(self, info, name, service_name, service_user_id):
		print("SERvice name", service_name)
		services = handler.get_session().\
			query(ServiceModel).\
			filter(ServiceModel.name == service_name).\
			all()
		if len(services) == 0:
			service = ServiceModel(name=service_name)
			handler.add(service)
		else:
			service = services[0]

		users = handler.get_session().\
			query(UserModel).\
			filter(UserModel.service==service, UserModel.service_user_id==service_user_id).\
			all()
		if len(users) == 0:
			user = UserModel(name=name, service=service, service_user_id=service_user_id)
			handler.add(user)
			try:
				handler.commit()
			except:
				import traceback
				print("Error occured while User")
				traceback.print_exc()
		else:
			print("User already exists")
			user = users[0]

		return CreateUser(
			uuid=user.uuid,
			name=user.name,
			service_name=service_name,
			service_user_id=user.service_user_id)


class Query(graphene.ObjectType):
	node = relay.Node.Field()
	all_services = SQLAlchemyConnectionField(ServiceConnection, sort=None)
	all_users    = SQLAlchemyConnectionField(UsersConnection)

class Mutation(graphene.ObjectType):
	node = relay.Node.Field()
	create_user = CreateUser.Field()
	create_service = CreateService.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)