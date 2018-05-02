from bizon.apps.fabric_utils.fabric_class import (
    add_class_methods_as_functions,
    DjangoFabric
)


class Fabric(DjangoFabric):
    host = '89.223.31.37'
    app_name = 'bizon'
    repository = 'git@github.com:jobsteam/bizon.git'
    remote_db_name = 'bizon'
    local_db_name = 'bizon'
    use_bower = True
    user = 'dimi'


__all__ = add_class_methods_as_functions(Fabric(), __name__)
