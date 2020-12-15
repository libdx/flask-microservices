from flask_restx import Namespace, Resource

namespace = Namespace("ping")


class Ping(Resource):
    """Represents health check"""

    def get(self):
        """GET /ping endpoint

        Returns:
            dict object representing health status

        """
        return {"status": "success", "message": "pong!"}


namespace.add_resource(Ping, "")
