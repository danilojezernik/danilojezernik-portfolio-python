def write_fields_to_txt(models):
    """
    Writes (documents) the field names and their types for each Pydantic model to a text file for frontend usage.

    This function takes a list of Pydantic model classes, extracts the field names and their corresponding types,
    and writes this information to a file named 'output.txt'. Each model's fields are listed under the model's name.

    Args:
        models (list): A list of Pydantic model classes to process.

    The output file format:
    ModelName:
      field_name: field_type
      ...

    Example:
        Blog:
          id: str
          naslov: str
          kategorija: str
          ...

        Experiences:
          id: str
          title: str
          stack: str
          ...
    """
    with open('output.txt', 'w') as f:
        for model in models:
            model_name = model.__name__  # Get the name of the model class
            f.write(f"{model_name}:\n")  # Write the model name to the file
            for field_name, field_info in model.__fields__.items():
                field_type = field_info.type_  # Get the type of the field
                # Convert the type to a readable string format
                type_name = str(field_type).replace("<class '", "").replace("'>", "")
                f.write(f"  {field_name}: {type_name}\n")  # Write the field name and type to the file
            f.write("\n")  # Add a newline for separation between models
