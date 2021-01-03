import json

settings_json = json.dumps([
    {'type': 'title',
     'title': 'Tutorial'},
    {'type': 'title',
     'title': '***APP WILL CLOSE ON CONFIG CHANGE***'},
    {'type': 'bool',
     'title': 'Enable Tutorial',
     'desc': 'Enables a text version of tutorials.',
     'section': 'tutorial',
     'key': 'tutorial_status'}])


####################
# Later implementations
    # {'type': 'numeric',
    #  'title': 'A numeric setting',
    #  'desc': 'Numeric description text',
    #  'section': 'example',
    #  'key': 'numericexample'},
    # {'type': 'options',
    #  'title': 'An options setting',
    #  'desc': 'Options description text',
    #  'section': 'example',
    #  'key': 'optionsexample',
    #  'options': ['option1', 'option2', 'option3']},
    # {'type': 'string',
    #  'title': 'A string setting',
    #  'desc': 'String description text',
    #  'section': 'example',
    #  'key': 'stringexample'},
    # {'type': 'path',
    #  'title': 'A path setting',
    #  'desc': 'Path description text',
    #  'section': 'example',
    #  'key': 'pathexample'}])
