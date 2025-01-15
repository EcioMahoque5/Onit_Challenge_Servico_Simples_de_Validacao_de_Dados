from flask import Blueprint, request, make_response
import logging
from .validators import create_dynamic_form
from wtforms.validators import ValidationError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

api_bp = Blueprint('api', __name__)


@api_bp.route('/schema_validation', methods=['POST'])
def schema_validation():
    try:
        request_data = request.get_json()
        schema = request_data.get("schema")
        data = request_data.get("data")
        
        logger.info(f"schema_validation request received: {request_data}")
        
        if not schema and not data:
            logger.error(f"schema_validation error: data and schema are required fields!")
            return make_response({
                "success": False,
                "message": "Validations errors",
                "errors": {
                    "schema": ["schema is a required field!"],
                    "data": ["data is a required field!"]
                }
            }, 400)
            
        if not data:
            logger.error(f"schema_validation error: data is a required field!")
            return make_response({
                "success": False,
                "message": "Validations errors",
                "errors": {
                    "data": ["data is a required field!"]
                }
            }, 400)
            
        if not schema:
            logger.error(f"schema_validation error: schema is a required field!")
            return make_response({
                "success": False,
                "message": "Validations errors",
                "errors": {
                    "schema": ["schema is a required field!"]
                }
            }, 400)
        
            
        # Dynamically create the form class
        DynamicForm = create_dynamic_form(schema)
        
        form = DynamicForm(data=data)
        
        if form.validate():
            logger.info("schema_validation response: Data is valid!")
            
            return make_response({
                "success": True,
                "message": "Data is valid!"
            }, 200)
            
        else:
            logger.error({
                "message": "Validations errors",
                "errors": form.errors,
            })
            return make_response({
                "success": False,
                "message": "Validations errors",
                "errors": form.errors
            }, 400)
    
    except ValueError as e:
        return make_response({
            "success": False,
            "message": str(e)
        },400)
        
    except Exception as e:
        logger.error(e, exc_info=True)
        logger.info(f"error {e} occured on schema_validation api")
        return make_response({
            "success": True,
            "message": "An unexpected error occurred. Please try again later!",
        }, 500)
