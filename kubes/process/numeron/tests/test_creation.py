import pytest
from gateway import local_api_connection

@pytest.fixture
def app():
    app = local_api_connection.activate({'TESTING': True})
    # 必要なら前処理を
    # yield app
    return app
    # 必要なら後処理を


@pytest.fixture
def client(app):
    return app.test_client()



def test_creation(client):
	with client:
		mutation = """
		{
		  createService(input: {
		  	name: "%s"
		  })
		  {
		    uuid
		    name
		  }
		  createUser(input: {
		  	name: "%s"
		  	service: {
		  	  name: "%s"
		  	}
		  	serviceUserId: "%s"
		  })
		  {
		  	edges {
		  	  node {
		  	    uuid
		  	    name
		  	    service {
		  	      uuid
		  	      name
		  	    }
		  	    serviceUserId
		  	  }
		  	}
		  }
		}
		""" % (service_name, user_name, service_name, user_id)
		query = """
		"""

		resp = client.post("/graphql", data=dict(
			mutation=mutation,
			query=query
		))

		print("response")
		print(resp)
