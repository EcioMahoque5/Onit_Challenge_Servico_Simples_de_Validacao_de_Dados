from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Email
import datetime
import json


def validate_schema_field_type(field_type):
    """Validar os tipos de dados aceitaveis"""
    valid_types = ["number", "string", "email", "datetime", "date", "time", "dictionary", "array", "boolean"]
    if field_type not in valid_types:
        raise ValueError(f"Unsupported field type: {field_type}. Allowed types are: {', '.join(valid_types)}")


def parse_numeric_value(value, field_name, parameter_name):
    """Para o caso dos numeros min and max forem passados como string, temos que verificar se sao
        numeros validos"""
    if isinstance(value, str):
        try:
            return int(value) if '.' not in value else float(value)
        except ValueError:
             raise ValueError(f"Invalid numeric value '{value}' for '{parameter_name}' in field '{field_name}'.")
    return value


def create_dynamic_form(schema):
    """Cria dinamicamente um flask form com base no schema passado no request."""
    class DynamicForm(FlaskForm):
        pass

    for field_name, rules in schema.items():
        field_type = rules.get("type")
        validators = []

        
        validate_schema_field_type(field_type)

        # Handle required fields. By default all fields are not required!!!!
        if rules.get("required", False):
            validators.append(DataRequired(message=rules.get("required_message", f"{field_name} is required.")))

        # Handle string fields
        if field_type == "string":
            max_length = parse_numeric_value(rules.get("max_length"), field_name, 'max_length')
            min_length = parse_numeric_value(rules.get("min_length"), field_name, 'min_length')

            if max_length is not None and min_length is not None:
                validators.append(Length(
                    max=max_length,
                    min=min_length,
                    message=rules.get("length_message", f"{field_name} must be between {min_length} and {max_length} characters!")
                ))
            elif max_length is not None:
                validators.append(Length(
                    max=max_length,
                    message=rules.get("length_message", f"{field_name} must not exceed {max_length} characters!")
                ))
            elif min_length is not None:
                validators.append(Length(
                    min=min_length,
                    message=rules.get("length_message", f"{field_name} must have at least {min_length} characters!")
                ))
            setattr(DynamicForm, field_name, StringField(field_name, validators=validators))

        # Handle number fields
        elif field_type == "number":
            min_value = parse_numeric_value(rules.get("min"), field_name, 'min')
            max_value = parse_numeric_value(rules.get("max"),field_name, 'max')

            if min_value is not None and max_value is not None:
                validators.append(NumberRange(
                    min=min_value,
                    max=max_value,
                    message=rules.get("range_message", f"{field_name} must be between {min_value} and {max_value}!")
                ))
            elif min_value is not None:
                validators.append(NumberRange(
                    min=min_value,
                    message=rules.get("range_message", f"{field_name} must be at least {min_value}!")
                ))
            elif max_value is not None:
                validators.append(NumberRange(
                    max=max_value,
                    message=rules.get("range_message", f"{field_name} must be no greater than {max_value}!")
                ))
            setattr(DynamicForm, field_name, IntegerField(field_name, validators=validators))

        # Handle email fields
        elif field_type == "email":
            max_length = parse_numeric_value(rules.get("max_length"), field_name, 'max_length')
            min_length = parse_numeric_value(rules.get("min_length"), field_name, 'min_length')

            if max_length is not None and min_length is not None:
                validators.append(Length(
                    max=max_length,
                    min=min_length,
                    message=rules.get("length_message", f"{field_name} must be between {min_length} and {max_length} characters!")
                ))
            elif max_length is not None:
                validators.append(Length(
                    max=max_length,
                    message=rules.get("length_message", f"{field_name} must not exceed {max_length} characters!")
                ))
            elif min_length is not None:
                validators.append(Length(
                    min=min_length,
                    message=rules.get("length_message", f"{field_name} must have at least {min_length} characters!")
                ))

            validators.append(Email(message="Email must be a valid email!"))
            setattr(DynamicForm, field_name, StringField(field_name, validators=validators))

        # Handle datetime fields
        elif field_type == "datetime":
            def validate_datetime(form, field):
                try:
                    datetime.datetime.strptime(field.data, "%Y-%m-%d %H:%M")
                except ValueError:
                    raise ValidationError(f"{field_name} must be in the format YYYY-MM-DD HH:MM.")

            validators.append(validate_datetime)
            setattr(DynamicForm, field_name, StringField(field_name, validators=validators))

        # Handle date fields
        elif field_type == "date":
            def validate_date(form, field):
                try:
                    datetime.datetime.strptime(field.data, "%Y-%m-%d")
                except ValueError:
                    raise ValidationError(f"{field_name} must be in the format YYYY-MM-DD.")

            validators.append(validate_date)
            setattr(DynamicForm, field_name, StringField(field_name, validators=validators))

        # Handle time fields
        elif field_type == "time":
            def validate_time(form, field):
                try:
                    datetime.datetime.strptime(field.data, "%H:%M")
                except ValueError:
                    raise ValidationError(f"{field_name} must be in the format HH:MM.")

            validators.append(validate_time)
            setattr(DynamicForm, field_name, StringField(field_name, validators=validators))

        # Handle dictionary fields
        elif field_type == "dictionary":
            def validate_dictionary(form, field, name=field_name):
                try:
                    json.loads(field.data)
                except json.JSONDecodeError:
                    raise ValidationError(f"{name} must be a valid JSON object.")

            validators.append(validate_dictionary)
            setattr(DynamicForm, field_name, StringField(field_name, validators=validators))

        # Handle array fields
        elif field_type == "array":
            def validate_array(form, field, name=field_name):
                try:
                    data = json.loads(field.data)
                    if not isinstance(data, list):
                        raise ValidationError(f"{name} must be a valid JSON array.")
                except json.JSONDecodeError:
                    raise ValidationError(f"{name} must be a valid JSON array.")

            validators.append(validate_array)
            setattr(DynamicForm, field_name, StringField(field_name, validators=validators))

        # Handle boolean fields
        elif field_type == "boolean":
            def validate_boolean(form, field, name=field_name):
                valid_values = {True, False, "true", "false", "1", "0", 1, 0}
                if field.data not in valid_values:
                    raise ValidationError(f"{name} must be a valid boolean value (true/false).")

                # Convert to Python boolean for consistency
                if field.data in {"true", "1", 1}:
                    field.data = True
                elif field.data in {"false", "0", 0}:
                    field.data = False

            validators.append(validate_boolean)
            setattr(DynamicForm, field_name, StringField(field_name, validators=validators))

    return DynamicForm
