from feast import Entity

# TODO: définir l'entité principale "user"
user = Entity(
    name="user",               # TODO
    join_keys=["user_id"],        # TODO
    description="clef utilisée pour reconnaître l'identité de l'utilisateur",        # TODO (en français)
)
    